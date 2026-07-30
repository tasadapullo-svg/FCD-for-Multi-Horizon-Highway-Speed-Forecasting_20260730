"""Phase 13 strong-baseline runner.  It never mutates inputs or locked outputs."""
from __future__ import annotations

import argparse
import hashlib
import logging
import random
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import yaml


METRIC_COLUMNS = ["phase", "model", "horizon", "seed", "train_n", "val_n", "test_n", "node_count", "feature_set", "MAE", "RMSE", "MAPE", "sMAPE", "R2", "fit_time_sec", "inference_time_sec", "config_hash", "data_hash"]


def read_config(path: Path) -> tuple[dict, str]:
    raw = path.read_text(encoding="utf-8")
    return yaml.safe_load(raw), hashlib.sha256(raw.encode()).hexdigest()


def file_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.name.encode())
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
    return digest.hexdigest()


def setup_logger(path: Path) -> logging.Logger:
    logger = logging.getLogger("phase13")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    for handler in (logging.FileHandler(path, encoding="utf-8"), logging.StreamHandler()):
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def set_seed(seed: int) -> None:
    random.seed(seed); np.random.seed(seed)
    import torch
    torch.manual_seed(seed)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True; torch.backends.cudnn.benchmark = False


def standardize_panel(panel: pd.DataFrame) -> pd.DataFrame:
    panel = panel.copy()
    if "point_id" not in panel and "node_id" in panel: panel["point_id"] = panel["node_id"]
    if "timestamp" not in panel and "time_bin" in panel: panel["timestamp"] = panel["time_bin"]
    panel["timestamp"] = pd.to_datetime(panel["timestamp"])
    if "hour_of_day" not in panel and "hour" in panel: panel["hour_of_day"] = panel["hour"]
    if "weekend_flag" not in panel and "day_of_week" in panel: panel["weekend_flag"] = (pd.to_numeric(panel["day_of_week"], errors="coerce").fillna(0) >= 5).astype(int)
    return panel.sort_values(["point_id", "timestamp"]).reset_index(drop=True)


def load_panel(path: Path, cfg: dict) -> pd.DataFrame:
    panel = standardize_panel(pd.read_csv(path))
    required = {"point_id", "timestamp", cfg["task"]["target_column"], *cfg["data"]["input_features"]}
    missing = required - set(panel.columns)
    if missing: raise ValueError(f"Model-ready panel missing columns: {sorted(missing)}")
    return panel


def point_arrays(panel: pd.DataFrame, cfg: dict) -> dict[str, dict[str, np.ndarray]]:
    target, features = cfg["task"]["target_column"], cfg["data"]["input_features"]
    global_mean = float(pd.to_numeric(panel[target], errors="coerce").mean())
    output = {}
    for point_id, frame in panel.groupby("point_id", sort=True):
        frame = frame.sort_values("timestamp")
        mean = float(pd.to_numeric(frame[target], errors="coerce").mean())
        mean = global_mean if not np.isfinite(mean) else mean
        values = {"time": frame["timestamp"].to_numpy(), "target": pd.to_numeric(frame[target], errors="coerce").to_numpy(float)}
        for col in features:
            value = pd.to_numeric(frame[col], errors="coerce").to_numpy(float)
            if col == target: value = np.where(np.isfinite(value), value, mean)
            elif col == "missing_mask": value = np.where(np.isfinite(value), value, 1.0)
            else: value = np.where(np.isfinite(value), value, 0.0)
            if col == "hour_of_day": value /= 23.0
            if col == "day_of_week": value /= 6.0
            values[col] = value.astype(np.float32)
        values["raw_hour"] = pd.to_numeric(frame["hour_of_day"], errors="coerce").fillna(0).to_numpy(int)
        values["raw_dow"] = pd.to_numeric(frame["day_of_week"], errors="coerce").fillna(0).to_numpy(int)
        output[str(point_id)] = values
    return output


def index_of(times: np.ndarray, timestamp: pd.Timestamp) -> int:
    idx = np.searchsorted(times, np.datetime64(timestamp))
    if idx == len(times) or times[idx] != np.datetime64(timestamp): raise KeyError(f"Timestamp missing from node timeline: {timestamp}")
    return int(idx)


def load_windows(cfg: dict, horizon: int, caps: dict[str, int | None]) -> pd.DataFrame:
    cols = ["window_id", "point_id", "input_start_time", "input_end_time", "target_start_time", "target_end_time", "history_hours", "horizon_hours", "split", "target_variable", "input_observed_ratio", "target_observed_ratio", "is_main_forecast", "is_extended_horizon"]
    kept = {name: 0 for name in caps}; frames = []
    for chunk in pd.read_csv(cfg["paths"]["window_index"], usecols=cols, parse_dates=cols[2:6], chunksize=cfg["data"]["window_chunksize"]):
        valid = chunk[(chunk.target_variable == "speed") & (chunk.history_hours == cfg["task"]["history_hours"]) & (chunk.horizon_hours == horizon) & (chunk.is_main_forecast == 1) & (chunk.is_extended_horizon == 0) & (chunk.input_observed_ratio >= cfg["task"]["min_input_observed_ratio"]) & (chunk.target_observed_ratio >= cfg["task"]["min_target_observed_ratio"])]
        for split, cap in caps.items():
            part = valid[valid.split == split]
            if cap is not None: part = part.head(max(0, cap - kept[split]))
            if not part.empty: frames.append(part); kept[split] += len(part)
        if all(caps[s] is not None and kept[s] >= caps[s] for s in caps): break
    if not frames: raise ValueError(f"No feasible Phase 2 windows for horizon {horizon}")
    return pd.concat(frames, ignore_index=True)


@dataclass
class Samples:
    x: np.ndarray; y: np.ndarray; split: np.ndarray; sample_id: np.ndarray; timestamp: np.ndarray; node_id: np.ndarray
    node_code: np.ndarray; ha: np.ndarray; seasonal: np.ndarray


def build_samples(windows: pd.DataFrame, arrays: dict[str, dict[str, np.ndarray]], panel: pd.DataFrame, cfg: dict) -> Samples:
    target = cfg["task"]["target_column"]; features = cfg["data"]["input_features"]
    train_end = windows.loc[windows.split == "train", "target_end_time"].max()
    train_panel = panel[panel.timestamp <= train_end]
    point_mean = train_panel.groupby("point_id")[target].mean().to_dict(); global_mean = float(train_panel[target].mean())
    seasonal = train_panel.groupby(["point_id", "hour_of_day", "day_of_week"])[target].mean().to_dict(); seasonal_hour = train_panel.groupby(["point_id", "hour_of_day"])[target].mean().to_dict()
    rows = []
    for row in windows.itertuples(index=False):
        a = arrays[str(row.point_id)]; start, end = index_of(a["time"], row.input_start_time), index_of(a["time"], row.input_end_time)
        ts, te = index_of(a["time"], row.target_start_time), index_of(a["time"], row.target_end_time)
        if end - start + 1 != cfg["task"]["history_hours"]: continue
        truth = a["target"][ts:te + 1]; truth = truth[np.isfinite(truth)]
        if not len(truth): continue
        season_values = []
        for idx in range(ts, te + 1):
            key = (str(row.point_id), int(a["raw_hour"][idx]), int(a["raw_dow"][idx]))
            season_values.append(seasonal.get(key, seasonal_hour.get(key[:2], point_mean.get(row.point_id, global_mean))))
        x = np.stack([a[col][start:end + 1] for col in features], axis=1)
        rows.append((x, float(truth.mean()), row.split, str(row.window_id), row.target_start_time, str(row.point_id), float(point_mean.get(row.point_id, global_mean)), float(np.mean(season_values))))
    if not rows: raise ValueError("No valid samples were created from Phase 2 windows")
    cols = list(zip(*rows)); node_ids = np.asarray(cols[5])
    node_code = pd.factorize(node_ids, sort=True)[0].astype("int64")
    return Samples(np.stack(cols[0]).astype("float32"), np.asarray(cols[1], "float32"), np.asarray(cols[2]), np.asarray(cols[3]), np.asarray(cols[4]), node_ids, node_code, np.asarray(cols[6], "float32"), np.asarray(cols[7], "float32"))


@dataclass
class Scaler:
    x_mean: np.ndarray; x_std: np.ndarray; y_mean: float; y_std: float
    def x(self, value): return ((value-self.x_mean.reshape(1,1,-1))/self.x_std.reshape(1,1,-1)).astype("float32")
    def y(self, value): return ((value-self.y_mean)/self.y_std).astype("float32")
    def inverse(self, value): return value*self.y_std+self.y_mean


def fit_scaler(samples: Samples) -> Scaler:
    train = samples.split == "train"; value = samples.x[train]
    mean, std = value.reshape(-1, value.shape[-1]).mean(0), value.reshape(-1, value.shape[-1]).std(0)
    std = np.where(std < 1e-6, 1.0, std); y_std = float(samples.y[train].std())
    return Scaler(mean.astype("float32"), std.astype("float32"), float(samples.y[train].mean()), y_std if y_std >= 1e-6 else 1.0)


def metrics(y: np.ndarray, pred: np.ndarray) -> dict:
    error = pred.astype(float)-y.astype(float); denom = np.abs(y)+np.abs(pred); variance = float(np.square(y-y.mean()).sum())
    return {"MAE": float(np.abs(error).mean()), "RMSE": float(np.sqrt(np.square(error).mean())), "MAPE": float((np.abs(error)/np.maximum(np.abs(y), 1e-6)).mean()), "sMAPE": float((2*np.abs(error)/np.maximum(denom, 1e-6)).mean()), "R2": float(1-np.square(error).sum()/variance) if variance else np.nan}


def neural_model(name: str, features: int, nodes: int, cfg: dict):
    import torch.nn as nn
    if name == "GRU":
        m = cfg["models"]["gru"]
        class GRU(nn.Module):
            def __init__(self): super().__init__(); self.net=nn.GRU(features, m["hidden_size"], m["num_layers"], batch_first=True, dropout=m["dropout"] if m["num_layers"] > 1 else 0); self.head=nn.Linear(m["hidden_size"],1)
            def forward(self,x,node): return self.head(self.net(x)[0][:,-1])
        return GRU()
    if name == "TCN":
        import torch
        m=cfg["models"]["tcn"]
        class Block(nn.Module):
            def __init__(self, i,o,d): super().__init__(); p=(m["kernel_size"]-1)*d; self.c1=nn.Conv1d(i,o,m["kernel_size"],padding=p,dilation=d); self.c2=nn.Conv1d(o,o,m["kernel_size"],padding=p,dilation=d); self.drop=nn.Dropout(m["dropout"]); self.skip=nn.Conv1d(i,o,1) if i!=o else nn.Identity(); self.p=p
            def forward(self,x):
                z=self.c1(x); z=z[:,:,:-self.p] if self.p else z; z=self.drop(torch.relu(z)); z=self.c2(z); z=z[:,:,:-self.p] if self.p else z
                return torch.relu(z+self.skip(x))
        class TCN(nn.Module):
            def __init__(self):
                super().__init__(); layers=[]; i=features
                for k,o in enumerate(m["channels"]): layers.append(Block(i,o,2**k)); i=o
                self.net=nn.Sequential(*layers); self.head=nn.Linear(i,1)
            def forward(self,x,node): return self.head(self.net(x.transpose(1,2))[:,:,-1])
        return TCN()
    m=cfg["models"]["st_transformer_lite"]
    import torch
    class Transformer(nn.Module):
        def __init__(self):
            super().__init__(); self.embed=nn.Linear(features,m["d_model"]); self.node_embed=nn.Embedding(nodes,m["d_model"]); self.position=nn.Parameter(torch.zeros(1,cfg["task"]["history_hours"],m["d_model"])); layer=nn.TransformerEncoderLayer(m["d_model"],m["nhead"],m["dim_feedforward"],m["dropout"],batch_first=True); self.encoder=nn.TransformerEncoder(layer,m["num_layers"]); self.head=nn.Linear(m["d_model"],1)
        def forward(self,x,node): return self.head(self.encoder(self.embed(x)+self.node_embed(node).unsqueeze(1)+self.position)[:,-1])
    return Transformer()


def train_neural(name: str, samples: Samples, scaler: Scaler, cfg: dict, seed: int) -> tuple[np.ndarray, float, float]:
    import torch
    from torch.utils.data import DataLoader, TensorDataset
    set_seed(seed); device = "cuda" if cfg["training"]["device"] == "auto" and torch.cuda.is_available() else cfg["training"]["device"]
    if device == "auto": device = "cpu"
    use_cuda = str(device).startswith("cuda")
    num_workers = int(cfg["training"].get("num_workers", 0) or 0)
    pin_memory = bool(cfg["training"].get("pin_memory", False)) and use_cuda
    use_amp = bool(cfg["training"].get("amp", False)) and use_cuda
    gpu_resident = bool(cfg["training"].get("gpu_resident", False)) and use_cuda
    x, y = scaler.x(samples.x), scaler.y(samples.y); tr, va, te = samples.split=="train", samples.split=="val", samples.split=="test"
    model=neural_model(name,x.shape[-1],len(np.unique(samples.node_code)),cfg).to(device); opt=torch.optim.AdamW(model.parameters(),lr=cfg["training"]["learning_rate"],weight_decay=cfg["training"]["weight_decay"]); loss=torch.nn.MSELoss(); best=None; best_mae=np.inf; stale=0; start=time.perf_counter()
    amp_scaler = torch.amp.GradScaler("cuda", enabled=use_amp)
    if gpu_resident:
        batch_size = int(cfg["training"]["batch_size"])
        xtr=torch.from_numpy(x[tr]).to(device); ytr=torch.from_numpy(y[tr].reshape(-1,1)).to(device); ntr=torch.from_numpy(samples.node_code[tr]).to(device)
        xva=torch.from_numpy(x[va]).to(device); nva=torch.from_numpy(samples.node_code[va]).to(device)
        xte=torch.from_numpy(x[te]).to(device); nte=torch.from_numpy(samples.node_code[te]).to(device)
        def predict_tensor(xs, ns):
            out=[]
            with torch.no_grad():
                for start_idx in range(0, xs.shape[0], batch_size):
                    with torch.amp.autocast("cuda", enabled=use_amp):
                        out.append(model(xs[start_idx:start_idx+batch_size], ns[start_idx:start_idx+batch_size]).float().cpu().numpy().reshape(-1))
            return np.concatenate(out)
        for _ in range(cfg["active"]["epochs"]):
            model.train(); order=torch.randperm(xtr.shape[0], device=device)
            for start_idx in range(0, xtr.shape[0], batch_size):
                idx=order[start_idx:start_idx+batch_size]
                opt.zero_grad(set_to_none=True)
                with torch.amp.autocast("cuda", enabled=use_amp):
                    value=loss(model(xtr.index_select(0,idx),ntr.index_select(0,idx)),ytr.index_select(0,idx))
                amp_scaler.scale(value).backward(); amp_scaler.unscale_(opt); torch.nn.utils.clip_grad_norm_(model.parameters(),cfg["training"]["gradient_clip_norm"]); amp_scaler.step(opt); amp_scaler.update()
            model.eval(); pred=predict_tensor(xva,nva); mae=metrics(samples.y[va],scaler.inverse(pred))["MAE"]
            if mae < best_mae: best_mae=mae; best={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}; stale=0
            else: stale += 1
            if stale >= cfg["active"]["early_stopping_patience"]: break
        fit=time.perf_counter()-start; model.load_state_dict(best); model.eval(); start=time.perf_counter()
        pred=predict_tensor(xte,nte)
        return scaler.inverse(pred), fit, time.perf_counter()-start
    def loader(a,b,n,shuffle):
        kwargs = {
            "batch_size": cfg["training"]["batch_size"],
            "shuffle": shuffle,
            "num_workers": num_workers,
            "pin_memory": pin_memory,
        }
        if num_workers > 0:
            kwargs["persistent_workers"] = True
        return DataLoader(TensorDataset(torch.from_numpy(a),torch.from_numpy(b.reshape(-1,1)),torch.from_numpy(n)), **kwargs)
    train, val, test=loader(x[tr],y[tr],samples.node_code[tr],True),loader(x[va],y[va],samples.node_code[va],False),loader(x[te],y[te],samples.node_code[te],False)
    for _ in range(cfg["active"]["epochs"]):
        model.train()
        for xb,yb,nb in train:
            xb=xb.to(device, non_blocking=pin_memory); yb=yb.to(device, non_blocking=pin_memory); nb=nb.to(device, non_blocking=pin_memory)
            opt.zero_grad(set_to_none=True)
            with torch.amp.autocast("cuda", enabled=use_amp):
                value=loss(model(xb,nb),yb)
            amp_scaler.scale(value).backward(); amp_scaler.unscale_(opt); torch.nn.utils.clip_grad_norm_(model.parameters(),cfg["training"]["gradient_clip_norm"]); amp_scaler.step(opt); amp_scaler.update()
        model.eval(); pred=[]
        with torch.no_grad():
            for xb,_,nb in val:
                xb=xb.to(device, non_blocking=pin_memory); nb=nb.to(device, non_blocking=pin_memory)
                with torch.amp.autocast("cuda", enabled=use_amp):
                    pred.append(model(xb,nb).cpu().numpy().reshape(-1))
        mae=metrics(samples.y[va],scaler.inverse(np.concatenate(pred)))["MAE"]
        if mae < best_mae: best_mae=mae; best={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}; stale=0
        else: stale += 1
        if stale >= cfg["active"]["early_stopping_patience"]: break
    fit=time.perf_counter()-start; model.load_state_dict(best); model.eval(); start=time.perf_counter(); pred=[]
    with torch.no_grad():
        for xb,_,nb in test:
            xb=xb.to(device, non_blocking=pin_memory); nb=nb.to(device, non_blocking=pin_memory)
            with torch.amp.autocast("cuda", enabled=use_amp):
                pred.append(model(xb,nb).cpu().numpy().reshape(-1))
    return scaler.inverse(np.concatenate(pred)), fit, time.perf_counter()-start


def xgb_predict(samples: Samples, cfg: dict, seed: int) -> tuple[np.ndarray, float, float]:
    from xgboost import XGBRegressor
    train, test = samples.split == "train", samples.split == "test"; params = cfg["models"]["xgboost"]
    model=XGBRegressor(**params, random_state=seed, objective="reg:squarederror"); start=time.perf_counter(); model.fit(samples.x[train].reshape(train.sum(),-1),samples.y[train]); fit=time.perf_counter()-start; start=time.perf_counter(); pred=model.predict(samples.x[test].reshape(test.sum(),-1)); return pred,fit,time.perf_counter()-start


def save_result(model: str, horizon: int, seed: int, samples: Samples, prediction: np.ndarray, fit: float, infer: float, cfg: dict, config_hash: str, data_hash: str) -> dict:
    test=samples.split=="test"; truth=samples.y[test]; node_count=int(cfg["task"]["expected_node_count"]); values=metrics(truth,prediction)
    out=Path(cfg["paths"]["predictions"]); out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame({"sample_id":samples.sample_id[test],"timestamp":samples.timestamp[test],"node_id":samples.node_id[test],"horizon":horizon,"model":model,"seed":seed,"y_true":truth,"y_pred":prediction,"abs_error":np.abs(truth-prediction),"squared_error":np.square(truth-prediction)}).to_parquet(out/f"{model}_h{horizon}_seed{seed}.parquet",index=False)
    return {"phase":"phase13","model":model,"horizon":horizon,"seed":seed,"train_n":int((samples.split=="train").sum()),"val_n":int((samples.split=="val").sum()),"test_n":int(test.sum()),"node_count":node_count,"feature_set":"|".join(cfg["data"]["input_features"]),**values,"fit_time_sec":fit,"inference_time_sec":infer,"config_hash":config_hash,"data_hash":data_hash}


def main() -> None:
    parser=argparse.ArgumentParser(description="Phase 13 strong baseline experiments"); parser.add_argument("--config",default="configs/phase13_strong_baselines.yaml"); parser.add_argument("--mode",choices=["smoke","full"],default="smoke"); args=parser.parse_args()
    cfg,config_hash=read_config(Path(args.config)); cfg["active"]=cfg["training"][args.mode]; log_dir=Path(cfg["paths"]["output_logs"]); log_dir.mkdir(parents=True,exist_ok=True); logger=setup_logger(log_dir/f"phase13_strong_baselines_{args.mode}.log")
    panel_path,window_path=Path(cfg["paths"]["panel_1h"]),Path(cfg["paths"]["window_index"])
    if not panel_path.exists() or not window_path.exists(): raise FileNotFoundError("Phase 13 requires existing Phase 2 panel and window index.")
    data_hash=file_hash([panel_path,window_path]); panel=load_panel(panel_path,cfg); arrays=point_arrays(panel,cfg)
    expected_nodes = int(cfg["task"]["expected_node_count"])
    if len(arrays) != expected_nodes: raise ValueError(f"Expected {expected_nodes} stable nodes, found {len(arrays)} in the cleaned panel.")
    logger.info("mode=%s nodes=%s config_hash=%s data_hash=%s",args.mode,len(arrays),config_hash[:12],data_hash[:12])
    rows=[]; caps={s:cfg["active"][f"max_{s}_samples"] for s in ("train","val","test")}
    for horizon in cfg["task"]["horizons_hours"]:
        samples=build_samples(load_windows(cfg,horizon,caps),arrays,panel,cfg); scaler=fit_scaler(samples)
        reference={"HA":samples.ha[samples.split=="test"],"SeasonalHA":samples.seasonal[samples.split=="test"],"Persistence":samples.x[samples.split=="test",-1,0]}
        for seed in cfg["training"]["seeds"]:
            for name in cfg["models"]["enabled"]:
                if name in reference: prediction,fit,infer=reference[name],0.0,0.0
                elif name == "XGBoost": prediction,fit,infer=xgb_predict(samples,cfg,seed)
                else: prediction,fit,infer=train_neural(name,samples,scaler,cfg,seed)
                rows.append(save_result(name,horizon,seed,samples,prediction,fit,infer,cfg,config_hash,data_hash)); logger.info("model=%s horizon=%s seed=%s MAE=%.5f",name,horizon,seed,rows[-1]["MAE"])
    table=Path(cfg["paths"]["output_tables"]); table.mkdir(parents=True,exist_ok=True); pd.DataFrame(rows)[METRIC_COLUMNS].to_csv(table/"phase13_strong_baseline_metrics.csv",index=False,encoding="utf-8-sig")
    logger.info("Completed Phase 13 %s run with %s metric rows",args.mode,len(rows))


if __name__ == "__main__": main()
