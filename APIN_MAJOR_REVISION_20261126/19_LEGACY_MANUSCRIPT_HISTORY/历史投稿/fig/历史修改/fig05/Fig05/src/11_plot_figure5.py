from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image


COLORS = {"XGBoost": "#0072B2", "SeasonalHA": "#D55E00"}


def style() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 8.5, "axes.titlesize": 10,
        "axes.labelsize": 9, "legend.fontsize": 8, "axes.spines.top": False,
        "axes.spines.right": False, "figure.facecolor": "white", "axes.facecolor": "white",
    })


def plot_a(out: Path, destination: Path, dpi: int) -> None:
    metrics = pd.read_csv(out / "03_FIG05A" / "Fig05a_reliability_stratified_metrics.csv")
    definitions = pd.read_csv(out / "03_FIG05A" / "Fig05a_reliability_bin_definitions.csv")
    variables = definitions.loc[definitions["bin_status"].eq("PASS"), "reliability_variable"].drop_duplicates().tolist()
    fig, axes = plt.subplots(len(variables), 3, figsize=(8.5, 6.5), squeeze=False, sharey=False)
    for row, variable in enumerate(variables):
        for col, horizon in enumerate([1, 3, 6]):
            ax = axes[row, col]
            defs = definitions.loc[(definitions["reliability_variable"].eq(variable)) & (definitions["horizon"].eq(horizon))].set_index("bin").loc[["Q1", "Q2", "Q3", "Q4"]]
            labels = [f"{q}\n({lo:.3g},{hi:.3g}]" if q != "Q1" else f"{q}\n[{lo:.3g},{hi:.3g}]" for q, lo, hi in zip(defs.index, defs["cutpoint_lower"], defs["cutpoint_upper"])]
            x = np.arange(4)
            for model in ["XGBoost", "SeasonalHA"]:
                subset = metrics.loc[(metrics["model"].eq(model)) & (metrics["horizon"].eq(horizon)) & (metrics["reliability_variable"].eq(variable))].set_index("bin").reindex(["Q1", "Q2", "Q3", "Q4"])
                ax.plot(x, subset["fold_macro_mae"], marker="o", linewidth=1.6, markersize=4, color=COLORS[model], label=model)
                if model == "XGBoost":
                    for xi, y, n in zip(x, subset["fold_macro_mae"], subset["n_unique_samples"]):
                        ax.annotate(f"n={int(n):,}", (xi, y), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=5.5, color=COLORS[model])
            ax.set_xticks(x, labels, fontsize=6.2)
            ax.grid(axis="y", color="#D9D9D9", linewidth=.5)
            ax.set_title(f"H{horizon}")
            if col == 0:
                label = "History coverage ratio" if variable == "history_coverage_ratio" else "History imputation ratio"
                ax.set_ylabel(f"{label}\nFold-macro MAE (km/h)")
            if row == 0 and col == 2:
                ax.legend(frameon=False, loc="best")
    fig.suptitle("(a) Reliability-conditioned out-of-fold errors", fontsize=12, fontweight="bold", y=.995)
    fig.text(.5, .01, "Error-blind horizon-specific quartiles; P90 is not shown as a confidence interval. Two tied-distribution variables are retained as blocked in the data package.", ha="center", fontsize=7)
    fig.tight_layout(rect=[0, .035, 1, .97])
    fig.savefig(destination, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def heatmap_panel(frame: pd.DataFrame, value: str, destination: Path, dpi: int, title: str, cmap: str) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(8.5, 7.0), sharey=True)
    image = None
    for ax, horizon in zip(axes, [1, 3, 6]):
        subset = frame.loc[frame["horizon"].eq(horizon)]
        pivot = subset.pivot(index="node_order_verified", columns="fold", values=value).reindex(index=range(1, 52), columns=range(1, 7))
        masked = np.ma.masked_invalid(pivot.to_numpy(dtype=float))
        image = ax.imshow(masked, aspect="auto", origin="lower", interpolation="nearest", cmap=cmap)
        ax.set_title(f"H{horizon}")
        ax.set_xticks(range(6), [f"F{i}" for i in range(1, 7)])
        ax.set_xlabel("Fold")
        ax.set_yticks(np.arange(0, 51, 5), [str(i) for i in range(1, 52, 5)])
        if ax is axes[0]:
            ax.set_ylabel("Node order from formal manifests")
    if image is not None:
        bar = fig.colorbar(image, ax=axes, fraction=.025, pad=.02)
        bar.set_label("MAE (km/h)" if value == "mae" else "Unique sample count")
    fig.suptitle(title, fontsize=12, fontweight="bold", y=.99)
    fig.subplots_adjust(left=.08, right=.89, bottom=.08, top=.93, wspace=.08)
    fig.savefig(destination, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_c(out: Path, destination: Path, dpi: int) -> None:
    risk = pd.read_csv(out / "05_FIG05C" / "Fig05c_XGBoost_node_risk_profile.csv")
    fig, axes = plt.subplots(3, 1, figsize=(8.5, 6.5), sharex=True)
    for ax, horizon in zip(axes, [1, 3, 6]):
        subset = risk.loc[risk["horizon"].eq(horizon)].sort_values("node_order_verified")
        x = subset["node_order_verified"]
        ax.plot(x, subset["median_absolute_error"], color="#009E73", linewidth=1.4, label="Median absolute error")
        ax.plot(x, subset["p90_absolute_error"], color="#E69F00", linewidth=1.4, label="P90 absolute error")
        ax.plot(x, subset["worst_fold_mae"], color="#CC79A7", linewidth=1.4, label="Worst-fold MAE")
        ax.set_ylabel(f"H{horizon}\nError (km/h)")
        ax.grid(axis="y", color="#D9D9D9", linewidth=.5)
    axes[0].legend(frameon=False, ncol=3, loc="upper right")
    axes[-1].set_xlabel("Node order from formal Phase 2A-1 manifests (verified distance mapping unavailable)")
    fig.suptitle("(c) Out-of-fold error profile along the formal node sequence", fontsize=12, fontweight="bold", y=.995)
    fig.text(.5, .008, "P90 is the 90th percentile of the absolute-error distribution, not a confidence interval. No stable-high-risk stars are assigned.", ha="center", fontsize=7)
    fig.tight_layout(rect=[0, .035, 1, .97])
    fig.savefig(destination, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def combine(paths: list[Path], destination: Path, dpi: int, tiff: bool = False) -> None:
    images = [Image.open(path).convert("RGB") for path in paths]
    width = max(image.width for image in images)
    resized = []
    for image in images:
        if image.width != width:
            height = round(image.height * width / image.width)
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        resized.append(image)
    canvas = Image.new("RGB", (width, sum(image.height for image in resized)), "white")
    y = 0
    for image in resized:
        canvas.paste(image, (0, y))
        y += image.height
    kwargs = {"dpi": (dpi, dpi)}
    if tiff:
        kwargs["compression"] = "tiff_lzw"
    canvas.save(destination, **kwargs)
    for image in images:
        image.close()


def build_figures(out: Path) -> None:
    style()
    figures = out / "08_FIGURES"
    temp = out / "tmp" / "figure_panels"
    temp.mkdir(parents=True, exist_ok=True)
    xgb = pd.read_csv(out / "04_FIG05B" / "Fig05b_XGBoost_node_fold_metrics.csv")
    counts = pd.read_csv(out / "04_FIG05B" / "Fig05b_node_fold_sample_count.csv")
    for dpi in [300, 600]:
        a = temp / f"a_{dpi}.png"
        b = temp / f"b_{dpi}.png"
        c = temp / f"c_{dpi}.png"
        plot_a(out, a, dpi)
        heatmap_panel(xgb, "mae", b, dpi, "(b) Node-by-fold MAE for XGBoost", "viridis")
        plot_c(out, c, dpi)
        combine([a, b, c], figures / f"Fig05_full_{dpi}dpi.png", dpi)
        combine([a, b, c], figures / f"Fig05_full_{dpi}dpi.tiff", dpi, tiff=True)
        if dpi == 300:
            a.replace(figures / "Fig05a_reliability.png")
            b.replace(figures / "Fig05b_node_fold_heatmap.png")
            c.replace(figures / "Fig05c_corridor_profile.png")
    heatmap_panel(counts, "n", figures / "Fig05b_node_fold_sample_count.png", 300, "Node-by-fold unique sample count", "cividis")
    caption = """Figure 5. Descriptive engineering-boundary diagnostics using the formal Phase 2A-1 common out-of-fold test samples. (a) Fold-macro MAE for XGBoost and SeasonalHA across error-blind, horizon-specific quartiles of history coverage and history imputation. Max-gap and hours-since-last-observation quartiles contained tied cutpoints and were not silently jittered; their blocked definitions remain in the data package. (b) XGBoost MAE by formal manifest node order and fold; empty cells, if present, are blank and sample counts are supplied separately. (c) XGBoost median absolute error, 90th-percentile absolute error, and worst-fold MAE by formal manifest node order. P90 is a distribution percentile, not a confidence interval. The verified approximately 95.69 km distance mapping and the minimum sample-size rule for stable-high-risk classification were unavailable, so no distance-axis claim or stable-high-risk marker is shown. Associations are descriptive within the studied corridor and period and are not causal."""
    (figures / "Fig05_caption.txt").write_text(caption, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    build_figures(args.out)


if __name__ == "__main__":
    main()
