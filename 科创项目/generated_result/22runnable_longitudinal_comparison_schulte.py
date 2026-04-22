#===============================绘制组合图片=========================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import warnings
from scipy import stats
import statsmodels.formula.api as smf

# -------------------------- 顶刊绘图配置（Mac 完美兼容） --------------------------
warnings.filterwarnings("ignore")
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# -------------------------- 路径 --------------------------
SCHULTE_FILE = "/Users/pc/Desktop/longtitudinal_comparison/schulte_多次对比.xlsx"
OUTPUT_DIR = "/Users/pc/Desktop/longtitudinal_comparison/Schulte_LMM_Results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------- 配色（顶刊色盲安全） --------------------------
COLORS = {
    "丁香组": "#4A7CAD",
    "薰衣草组": "#9B6AB9",
    "雪松组": "#6A9F75"
}

# -------------------------- 加载数据 --------------------------
def load_data(file_path):
    df = pd.read_excel(file_path)
    long = []
    for _, row in df.iterrows():
        sid = str(row["id"]).strip()
        g = {"1":"丁香组","2":"薰衣草组","3":"雪松组"}.get(sid[0], None)
        if not g: continue
        for t in range(9):
            if t not in df.columns: continue
            s = row[t]
            if pd.isna(s) or s <= 0: continue
            long.append({"id":sid, "group":g, "time":t, "score":float(s)})
    return pd.DataFrame(long)

# -------------------------- LMM 模型 --------------------------
def fit_lmm(df, group):
    d = df[df["group"]==group].copy()
    try:
        m = smf.mixedlm("score ~ time", data=d, groups=d["id"], re_formula="1+time")
        r = m.fit(method="lbfgs", maxiter=1000)
        b = r.params["time"]
        p = 2*(1-stats.norm.cdf(abs(b/r.bse_fe["time"])))
        return {"beta":b, "p":p, "data":d}
    except:
        return None

# -------------------------- 顶刊绘图：1×3 组合图 --------------------------
def plot_figure(results, df_all):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), dpi=300)
    axes = axes.flatten()

    for ax, (group, res) in zip(axes, results.items()):
        color = COLORS[group]
        data = res["data"]

        # 个体轨迹（顶刊 spaghetti 样式）
        for sid in data["id"].unique():
            sub = data[data["id"]==sid].sort_values("time")
            ax.plot(sub["time"], sub["score"], color="#E8E8E8", linewidth=0.8, alpha=0.25)

        # 群体均值 + 95% CI
        agg = data.groupby("time")["score"].agg(["mean","sem"]).reset_index()
        ax.plot(agg["time"], agg["mean"], color=color, linewidth=2.8, marker="o", markersize=4)
        ax.fill_between(agg["time"], agg["mean"]-1.96*agg["sem"], agg["mean"]+1.96*agg["sem"],
                        color=color, alpha=0.15)

        # 标注统计量（答辩加分）
        beta = res["beta"]
        p = res["p"]
        sig = "***显著下降" if p<0.001 else "**显著下降" if p<0.01 else "*显著下降" if p<0.05 else "不显著"
        ax.text(0.5, 0.92, f"β={beta:.3f}\np={p:.3f}\n{sig}",
                transform=ax.transAxes, fontsize=10, color=color, weight="bold",
                verticalalignment="top", bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=color, alpha=0.8))

        # 样式
        ax.set_title(f"{group}", fontsize=14, weight="bold", color=color)
        ax.set_xlabel("时间点", fontsize=12)
        ax.set_ylabel("舒尔特成绩（秒）", fontsize=12)
        ax.set_xticks(range(9))
        ax.set_ylim(agg["mean"].min()*0.8, agg["mean"].max()*1.1)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "Schulte_顶刊版_LMM趋势图.png"), dpi=300, bbox_inches="tight")
    plt.close()
    print("✅ 舒尔特顶刊版 LMM 趋势图已保存！")

# -------------------------- 主程序 --------------------------
def main():
    df = load_data(SCHULTE_FILE)
    groups = ["丁香组","薰衣草组","雪松组"]
    res = {g: fit_lmm(df, g) for g in groups if fit_lmm(df, g)}
    plot_figure(res, df)

if __name__ == "__main__":
    main()
