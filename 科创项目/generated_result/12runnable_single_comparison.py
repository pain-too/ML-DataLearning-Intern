import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
import warnings

warnings.filterwarnings('ignore')

# ====================== 顶刊绘图配置 ======================
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.linewidth'] = 0.8

# ====================== 路径（匹配你的文件） ======================
STROOP_PATH = "/Users/pc/Desktop/longtitudinal_comparison/stroop_多次对比.xlsx"
SCHULTE_PATH = "/Users/pc/Desktop/longtitudinal_comparison/schulte_多次对比.xlsx"
OUTPUT_DIR = "/Users/pc/Desktop/longtitudinal_comparison/前后测配对t检验_顶刊版"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ====================== 顶刊配色 ======================
COLOR_PRE = "#4A7CAD"
COLOR_POST = "#E67E22"
COLOR个体 = "#E0E0E0"
GROUP_NAMES = {1: "丁香组", 2: "薰衣草组", 3: "雪松组"}

# ====================== 读取数据 ======================
def load_data(path):
    df = pd.read_excel(path)
    long_data = []
    for _, row in df.iterrows():
        sid = str(row['id']).strip()
        if len(sid) < 1:
            continue
        g = int(sid[0])
        if g not in [1, 2, 3]:
            continue
        pre = row.get(0, np.nan)
        post1 = row.get(1, np.nan)
        if np.isnan(pre) or np.isnan(post1):
            continue
        if pre <= 0 or post1 <= 0:
            continue
        long_data.append({
            "id": sid, "group": g, "pre": pre, "post": post1
        })
    return pd.DataFrame(long_data)

# ====================== 配对t检验 ======================
def paired_analysis(data, group_id):
    d = data[data['group'] == group_id].copy()
    if len(d) < 3:
        return None
    pre = d['pre'].values
    post = d['post'].values
    t_stat, p_val = stats.ttest_rel(pre, post)
    diff = pre - post
    d_mean = np.mean(diff)
    sd_diff = np.std(diff, ddof=1)
    se_pre = np.std(pre, ddof=1) / np.sqrt(len(pre))
    se_post = np.std(post, ddof=1) / np.sqrt(len(post))
    cohen = d_mean / np.sqrt((np.var(pre, ddof=1) + np.var(post, ddof=1)) / 2)
    return {
        "data": d, "n": len(d),
        "pre_mean": np.mean(pre), "se_pre": se_pre,
        "post_mean": np.mean(post), "se_post": se_post,
        "t": t_stat, "p": p_val, "d": cohen
    }

# ====================== 顶刊绘图 ======================
def plot_top_journal(res, group_id, task_name):
    group_name = GROUP_NAMES[group_id]
    n = res['n']
    t = res['t']
    p = res['p']
    d_cohen = res['d']
    m_pre = res['pre_mean']
    m_post = res['post_mean']
    se_pre = res['se_pre']
    se_post = res['se_post']

    if p < 0.001:
        sig = "***"
    elif p < 0.01:
        sig = "**"
    elif p < 0.05:
        sig = "*"
    else:
        sig = "ns"

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), dpi=300)

    # 左图：配对连线图
    for i in range(len(res['data'])):
        ax1.plot([0, 1],
                [res['data']['pre'].iloc[i], res['data']['post'].iloc[i]],
                color=COLOR个体, linewidth=0.8, alpha=0.3)

    ax1.errorbar(0, m_pre, yerr=se_pre, color=COLOR_PRE,
                marker='o', markersize=10, linewidth=3, capsize=8)
    ax1.errorbar(1, m_post, yerr=se_post, color=COLOR_POST,
                marker='o', markersize=10, linewidth=3, capsize=8)
    ax1.set_xticks([0, 1])
    ax1.set_xticklabels(['前测', '第一次后测'])
    ax1.set_ylabel('完成时间（秒）\n数值越小 → 注意力越好')
    ax1.set_title(f'{group_name}｜{task_name}\n配对连线图', fontweight='bold')

    # 右图：误差棒图
    ax2.bar([0, 1], [m_pre, m_post], yerr=[se_pre, se_post],
            color=[COLOR_PRE, COLOR_POST], alpha=0.8, width=0.6, capsize=8)
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(['前测', '第一次后测'])
    ax2.set_title('均值±标准误', fontweight='bold')

    stat_text = f"t({n-1}) = {t:.2f}\np = {p:.3f}\nd = {d_cohen:.2f}\n{sig}"
    ax1.text(0.5, 0.92, stat_text, transform=ax1.transAxes,
            fontsize=11, ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.4', fc='white', alpha=0.85))

    plt.tight_layout()
    filename = f"{group_id}_{group_name}_{task_name}.png"
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=300, bbox_inches='tight')
    plt.close()

# ====================== 【核心新增】顶刊标准文字报告 ======================
def generate_standard_report(results):
    report = []
    report.append("=" * 80)
    report.append("植物香气对注意力影响研究——前后测配对t检验分析报告")
    report.append("（顶刊标准格式｜中期报告可直接使用）")
    report.append("=" * 80 + "\n")

    for r in results:
        group = r['组别']
        task = r['任务']
        n = r['n']
        m_pre = r['前测均值']
        se_pre = r['前测标准误']
        m_post = r['后测均值']
        se_post = r['后测标准误']
        t = r['t值']
        p = r['p值']
        d = r['Cohen\'s d']
        sig = r['显著']

        report.append(f"【{group} - {task}】")
        if sig:
            line = (f"前后测差异显著，前测 M±SE = {m_pre:.2f}±{se_pre:.2f}，"
                    f"后测 M±SE = {m_post:.2f}±{se_post:.2f}，"
                    f"t({n-1}) = {t:.2f}，p = {p:.3f}，Cohen’s d = {d:.2f}。")
        else:
            line = (f"前后测差异不显著，前测 M±SE = {m_pre:.2f}±{se_pre:.2f}，"
                    f"后测 M±SE = {m_post:.2f}±{se_post:.2f}，"
                    f"t({n-1}) = {t:.2f}，p = {p:.3f}，Cohen’s d = {d:.2f}。")
        report.append(line)
        report.append("")

    report_str = "\n".join(report)
    print("\n" + "="*80)
    print("📝 顶刊标准文字报告（可直接复制到中期报告）")
    print("="*80)
    print(report_str)

    with open(os.path.join(OUTPUT_DIR, "顶刊标准文字报告.txt"), "w", encoding="utf-8") as f:
        f.write(report_str)
    print(f"\n✅ 报告已保存：{OUTPUT_DIR}/顶刊标准文字报告.txt")

# ====================== 主程序 ======================
def main():
    print("="*70)
    print("植物香气对注意力影响 —— 前后测配对t检验（图+文字报告 一键生成）")
    print("="*70)

    stroop = load_data(STROOP_PATH)
    schulte = load_data(SCHULTE_PATH)
    all_results = []

    for g in [1,2,3]:
        for task, data, task_cn in [
            ("Stroop", stroop, "Stroop任务"),
            ("舒尔特", schulte, "舒尔特方格")
        ]:
            res = paired_analysis(data, g)
            if res:
                plot_top_journal(res, g, task_cn)
                print(f"✅ {GROUP_NAMES[g]} {task_cn} —— 绘图完成")
                all_results.append({
                    "组别": GROUP_NAMES[g],
                    "任务": task_cn,
                    "n": res['n'],
                    "前测均值": res['pre_mean'],
                    "前测标准误": res['se_pre'],
                    "后测均值": res['post_mean'],
                    "后测标准误": res['se_post'],
                    "t值": res['t'],
                    "p值": res['p'],
                    "Cohen's d": res['d'],
                    "显著": res['p'] < 0.05
                })
            else:
                print(f"⚠️ {GROUP_NAMES[g]} {task_cn} —— 样本不足")

    if all_results:
        generate_standard_report(all_results)
    print("\n🎉 全部完成：6张图 + 1份顶刊文字报告")

if __name__ == "__main__":
    main()