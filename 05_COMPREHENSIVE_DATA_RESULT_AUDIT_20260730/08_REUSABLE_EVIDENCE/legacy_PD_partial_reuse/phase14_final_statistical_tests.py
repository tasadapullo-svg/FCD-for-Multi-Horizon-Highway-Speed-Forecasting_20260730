"""Phase 14 final statistics. Reads completed phase outputs; never retrains or mutates them."""
from __future__ import annotations
import argparse, math
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from scipy.stats import kruskal, rankdata, wilcoxon

PAIR_COLS=["phase_source","comparison_type","horizon","seed_scope","reference_model_or_condition","compared_model_or_condition","n_pairs","reference_MAE_mean","compared_MAE_mean","relative_improvement_or_degradation_percent","test_name","statistic","p_value","p_value_corrected","effect_size","effect_size_type","significance_label"]
STRAT_COLS=["phase_source","stratification_type","horizon","strata_compared","n_groups","total_n","test_name","statistic","p_value","p_value_corrected","effect_size","effect_size_type","significance_label"]

def load(path:Path)->dict:return yaml.safe_load(path.read_text(encoding="utf-8"))
def holm(rows:list[dict])->None:
    order=sorted(range(len(rows)),key=lambda i:rows[i]["p_value"]); prev=0.;m=len(rows)
    for rank,i in enumerate(order):
        value=min(1.,max(prev,(m-rank)*rows[i]["p_value"]));rows[i]["p_value_corrected"]=value;prev=value
    for r in rows:r["significance_label"]="***" if r["p_value_corrected"]<.001 else "**" if r["p_value_corrected"]<.01 else "*" if r["p_value_corrected"]<.05 else "ns"
def rbc(diff:np.ndarray)->float:
    diff=diff[np.isfinite(diff)&(diff!=0)]
    if not len(diff):return 0.
    ranks=rankdata(np.abs(diff));return float((ranks[diff>0].sum()-ranks[diff<0].sum())/ranks.sum())
def paired(source,kind,horizon,reference,compared,ref,cmp,scope)->dict:
    diff=np.asarray(cmp,float)-np.asarray(ref,float); nonzero=diff[diff!=0]
    if not len(nonzero):stat,p=0.,1.
    else: stat,p=wilcoxon(nonzero,alternative="two-sided",zero_method="wilcox")
    ref_mean=float(np.mean(ref));cmp_mean=float(np.mean(cmp));return {"phase_source":source,"comparison_type":kind,"horizon":horizon,"seed_scope":scope,"reference_model_or_condition":reference,"compared_model_or_condition":compared,"n_pairs":len(diff),"reference_MAE_mean":ref_mean,"compared_MAE_mean":cmp_mean,"relative_improvement_or_degradation_percent":100*(cmp_mean-ref_mean)/ref_mean,"test_name":"Wilcoxon signed-rank","statistic":float(stat),"p_value":float(p),"p_value_corrected":np.nan,"effect_size":rbc(diff),"effect_size_type":"rank-biserial correlation","significance_label":""}
def prediction_errors(path:Path)->pd.DataFrame:
    x=pd.read_parquet(path);return x[["sample_id","abs_error"]].rename(columns={"abs_error":"error"})
def phase13(cfg:dict,root:Path)->tuple[pd.DataFrame,Path]:
    lock=root/cfg["paths"]["phase13_locked"]; metrics=lock/"tables/phase13_strong_baseline_metrics.csv";pred=lock/"predictions"
    if not metrics.is_file(): metrics=root/cfg["paths"]["phase13_working_tables"];pred=root/cfg["paths"]["phase13_working_predictions"]
    if not metrics.is_file() or not pred.is_dir():raise FileNotFoundError("Phase 13 locked or working outputs are unavailable")
    return pd.read_csv(metrics),pred
def main()->None:
    parser=argparse.ArgumentParser();parser.add_argument("--config",default="configs/phase14_final_statistical_tests.yaml");args=parser.parse_args();root=Path(__file__).resolve().parents[1];cfg=load(root/args.config);out=root/cfg["paths"]["output_tables"];out.mkdir(parents=True,exist_ok=True)
    p13,pred_dir=phase13(cfg,root);main_model=cfg["main_model"]; main_rows=[]
    for h in cfg["horizons"]:
        for model in sorted(set(p13.model)-{main_model}):
            refs=[];cmps=[]
            for seed in cfg["seeds"]:
                ref=prediction_errors(pred_dir/f"{main_model}_h{h}_seed{seed}.parquet");cmp=prediction_errors(pred_dir/f"{model}_h{h}_seed{seed}.parquet");merged=ref.merge(cmp,on="sample_id",suffixes=("_ref","_cmp"),validate="one_to_one");refs.extend(merged.error_ref);cmps.extend(merged.error_cmp)
            main_rows.append(paired("phase13","proposed_vs_baseline",h,main_model,model,refs,cmps,"sample_level_pooled_5_seeds"))
    holm(main_rows);pd.DataFrame(main_rows)[PAIR_COLS].to_csv(out/"phase14_main_model_statistical_tests.csv",index=False,encoding="utf-8-sig")
    p15=pd.read_csv(root/cfg["paths"]["phase15_metrics"]);ablation=[]
    for h in cfg["horizons"]:
        ref=p15[(p15.horizon==h)&p15.feature_group.eq("speed_only")].set_index("seed").MAE
        for group in sorted(set(p15.feature_group)-{"speed_only"}):
            cmp=p15[(p15.horizon==h)&p15.feature_group.eq(group)].set_index("seed").MAE;common=ref.index.intersection(cmp.index);ablation.append(paired("phase15","feature_group_vs_speed_only",h,"speed_only",group,ref[common],cmp[common],"seed_level"))
    holm(ablation);pd.DataFrame(ablation)[PAIR_COLS].to_csv(out/"phase14_feature_ablation_statistical_tests.csv",index=False,encoding="utf-8-sig")
    robust=[]
    for source,key,path,reference in [("phase16_missingness","level",root/cfg["paths"]["phase16_missingness"],"0"),("phase16_noise","level",root/cfg["paths"]["phase16_noise"],"clean"),("phase16_small_sample","ratio_percent",root/cfg["paths"]["phase16_small_sample"],100)]:
        table=pd.read_csv(path)
        for h in cfg["horizons"]:
            ref=table[(table.horizon==h)&(table[key].astype(str)==str(reference))].set_index("seed").MAE
            for level in sorted(set(table[key].astype(str))-{str(reference)}):
                cmp=table[(table.horizon==h)&(table[key].astype(str)==level)].set_index("seed").MAE;common=ref.index.intersection(cmp.index);robust.append(paired(source,"condition_vs_reference",h,str(reference),level,ref[common],cmp[common],"seed_level"))
    holm(robust);pd.DataFrame(robust)[PAIR_COLS].to_csv(out/"phase14_robustness_statistical_tests.csv",index=False,encoding="utf-8-sig")
    strat=[]
    for typ in ["reliability","coverage","volatility","traffic_state"]:
        table=pd.read_csv(root/cfg["paths"]["phase17_tables"]/f"phase17_{typ}_stratified_metrics.csv")
        for h in cfg["horizons"]:
            groups=[g.MAE.to_numpy(float) for _,g in table[table.horizon.eq(h)].groupby("stratum")]; labels=sorted(table[table.horizon.eq(h)].stratum.unique());stat,p=kruskal(*groups);n=sum(map(len,groups));eps=max(0.,(stat-len(groups)+1)/(n-len(groups))) if n>len(groups) else 0.;strat.append({"phase_source":"phase17","stratification_type":typ,"horizon":h,"strata_compared":" | ".join(labels),"n_groups":len(groups),"total_n":n,"test_name":"Kruskal-Wallis H","statistic":float(stat),"p_value":float(p),"p_value_corrected":np.nan,"effect_size":float(eps),"effect_size_type":"epsilon-squared","significance_label":""})
    holm(strat);pd.DataFrame(strat)[STRAT_COLS].to_csv(out/"phase14_stratified_statistical_tests.csv",index=False,encoding="utf-8-sig")
    summaries=[]
    for source,table,name in [("phase13",p13,"model"),("phase15",p15,"feature_group")]:
        for (condition,h),g in table.groupby([name,"horizon"]):summaries.append({"phase_source":source,"model_or_condition":condition,"horizon":h,"metric":"MAE","mean":g.MAE.mean(),"std":g.MAE.std(ddof=1),"n_seeds":g.seed.nunique(),"formatted_mean_std":f"{g.MAE.mean():.4f} +/- {g.MAE.std(ddof=1):.4f}"})
    summary=pd.DataFrame(summaries)
    summary.to_csv(out/"phase14_final_mean_std_summary.csv",index=False,encoding="utf-8-sig")
    effects=pd.concat([pd.DataFrame(main_rows),pd.DataFrame(ablation),pd.DataFrame(robust),pd.DataFrame(strat)],ignore_index=True)
    if "n_pairs" in effects.columns and "total_n" in effects.columns:
        effects["n_pairs"]=effects["n_pairs"].fillna(effects["total_n"])
        effects["total_n"]=effects["total_n"].fillna(effects["n_pairs"])
    numeric_effect_columns=effects.select_dtypes(include=np.number).columns
    effects[numeric_effect_columns]=effects[numeric_effect_columns].fillna(0)
    effects.to_csv(out/"phase14_final_effect_size_summary.csv",index=False,encoding="utf-8-sig")
    report=root/cfg["paths"]["reports"]/"phase14_final_statistical_tests_report.md"
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text("\n".join(["# Phase 14 Final Statistical Tests","","- Phase 13 proposed-vs-baseline comparisons: paired sample-level Wilcoxon tests using locked prediction parquet files.","- Phase 15/16 comparisons: paired seed-level Wilcoxon tests on matched seed MAE values.","- Phase 17 strata: independent Kruskal-Wallis tests across stratum seed-level MAEs.","- Holm correction is applied within each output test family; effect sizes are rank-biserial correlation or epsilon-squared.","","See the Phase 14 CSV tables for n_pairs/total_n, raw and corrected p-values, effects, and mean +/- std.",""]),encoding="utf-8")
if __name__=='__main__':main()
