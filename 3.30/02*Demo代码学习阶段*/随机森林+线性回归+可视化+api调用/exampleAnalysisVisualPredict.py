import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import requests
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False






# ========== 配置 ==========
API_KEY = "sk-238347cfc1034459b8a4378c26325298"  # 换成你的Key

def ask_ai(prompt):
    """调用DeepSeek API"""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return f"错误: {response.status_code}"






# ========== 1. 读取数据 ==========
print("="*60)
print("1. 读取数据")
print("="*60)

# 改成你的文件名
df = pd.read_csv('实验数据_1000条.csv')  # 如果用原数据就改成 '你的文件名.csv'
print(f"数据形状: {df.shape}")
print(f"列名: {df.columns.tolist()}")
print(f"\n数据统计描述:")
print(df.describe())






# ========== 2. 数据可视化 ==========
print("\n" + "="*60)
print("2. 生成可视化图表")
print("="*60)

# 创建图表布局                ？？？？？
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# 图1：酶活性分布
axes[0, 0].hist(df['酶活性(U/mL)'], bins=30, edgecolor='black', alpha=0.7)
axes[0, 0].set_title('酶活性分布直方图')
axes[0, 0].set_xlabel('酶活性 (U/mL)')
axes[0, 0].set_ylabel('频数')

# 图2：酶活性 vs 温度
axes[0, 1].scatter(df['温度(℃)'], df['酶活性(U/mL)'], alpha=0.5, s=10)
axes[0, 1].set_title('酶活性与温度的关系')
axes[0, 1].set_xlabel('温度 (℃)')
axes[0, 1].set_ylabel('酶活性 (U/mL)')

# 图3：酶活性 vs pH
axes[0, 2].scatter(df['pH值'], df['酶活性(U/mL)'], alpha=0.5, s=10)
axes[0, 2].set_title('酶活性与pH的关系')
axes[0, 2].set_xlabel('pH值')
axes[0, 2].set_ylabel('酶活性 (U/mL)')

# 图4：吸光度 vs 酶活性
axes[1, 0].scatter(df['酶活性(U/mL)'], df['吸光度OD450'], alpha=0.5, s=10)
axes[1, 0].set_title('吸光度与酶活性的关系')
axes[1, 0].set_xlabel('酶活性 (U/mL)')
axes[1, 0].set_ylabel('吸光度 OD450')

# 图5：相关性热力图 ————————————————暂时略过不研究
correlation = df[['温度(℃)', 'pH值', '酶活性(U/mL)', '吸光度OD450']].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, ax=axes[1, 1])
axes[1, 1].set_title('特征相关性热力图')

# 图6：温度和pH的等高线图（双因素影响）——————————————略过不研究
from scipy.interpolate import griddata
xi = np.linspace(df['温度(℃)'].min(), df['温度(℃)'].max(), 50)
yi = np.linspace(df['pH值'].min(), df['pH值'].max(), 50)
xi, yi = np.meshgrid(xi, yi)
zi = griddata((df['温度(℃)'], df['pH值']), df['酶活性(U/mL)'], (xi, yi), method='cubic')
contour = axes[1, 2].contourf(xi, yi, zi, levels=20, cmap='viridis')
axes[1, 2].set_title('温度与pH对酶活性的联合影响')
axes[1, 2].set_xlabel('温度 (℃)')
axes[1, 2].set_ylabel('pH值')
plt.colorbar(contour, ax=axes[1, 2], label='酶活性 (U/mL)')

plt.tight_layout()
plt.savefig('数据分析可视化.png', dpi=150, bbox_inches='tight')
print("✓ 图表已保存为 '数据分析可视化.png'")
plt.show()






# ========== 3. 机器学习预测 ==========
print("\n" + "="*60)
print("3. 机器学习预测模型")
print("="*60)

# 准备数据
X = df[['温度(℃)', 'pH值', '吸光度OD450']]
y = df['酶活性(U/mL)']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 模型1：线性回归
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
r2_lr = r2_score(y_test, y_pred_lr)
rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))

# 模型2：随机森林
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
r2_rf = r2_score(y_test, y_pred_rf)
rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
#mean_squared_error()是一个固定函数，不是拼起来的函数，用于计算均方误差MSE，再开方就是RMSE

# 特征重要性
feature_importance = pd.DataFrame({
    '特征': ['温度(℃)', 'pH值', '吸光度OD450'],
    '重要性': rf.feature_importances_
}).sort_values('重要性', ascending=False)

print(f"线性回归 - R²分数: {r2_lr:.4f}, RMSE: {rmse_lr:.2f}")
print(f"随机森林 - R²分数: {r2_rf:.4f}, RMSE: {rmse_rf:.2f}")
print(f"\n特征重要性:")
print(feature_importance)

# 可视化预测效果
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].scatter(y_test, y_pred_lr, alpha=0.5, s=20)
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[0].set_title(f'线性回归预测效果 (R²={r2_lr:.3f})')
axes[0].set_xlabel('真实值')
axes[0].set_ylabel('预测值')

axes[1].scatter(y_test, y_pred_rf, alpha=0.5, s=20)
axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[1].set_title(f'随机森林预测效果 (R²={r2_rf:.3f})')
axes[1].set_xlabel('真实值')
axes[1].set_ylabel('预测值')

plt.tight_layout()
plt.savefig('预测效果对比.png', dpi=150, bbox_inches='tight')
print("✓ 预测效果图已保存为 '预测效果对比.png'")
plt.show()






# ========== 4. 最优条件分析 ==========
print("\n" + "="*60)
print("4. 最优实验条件分析")
print("="*60)

# 找出酶活性最高的前10个条件
optimal_conditions = df.nlargest(10, '酶活性(U/mL)')[['温度(℃)', 'pH值', '酶活性(U/mL)', '吸光度OD450']]
print("酶活性最高的10个实验条件:")
print(optimal_conditions)

# 计算平均最优条件
avg_optimal_temp = optimal_conditions['温度(℃)'].mean()
avg_optimal_ph = optimal_conditions['pH值'].mean()
print(f"\n最优温度范围: {optimal_conditions['温度(℃)'].min():.1f} - {optimal_conditions['温度(℃)'].max():.1f} ℃")
print(f"最优pH范围: {optimal_conditions['pH值'].min():.2f} - {optimal_conditions['pH值'].max():.2f}")
print(f"平均最优温度: {avg_optimal_temp:.1f} ℃")
print(f"平均最优pH: {avg_optimal_ph:.2f}")






# ========== 5. AI智能分析报告 ==========
print("\n" + "="*60)
print("5. AI生成分析报告")
print("="*60)

# 准备给AI的数据摘要
stats_summary = df.describe().to_string()
correlation_summary = correlation.to_string()
model_performance = f"随机森林模型R²分数: {r2_rf:.4f}, RMSE: {rmse_rf:.2f}"

prompt = f"""
请根据以下实验数据分析报告，写一份专业的数据分析总结报告：

【数据概况】
数据量: {len(df)} 条实验记录
指标: 温度、pH值、酶活性、吸光度

【统计摘要】
{stats_summary}

【相关性分析】
{correlation_summary}

【预测模型效果】
{model_performance}

【最优条件】
温度: {avg_optimal_temp:.1f}℃, pH: {avg_optimal_ph:.2f}

请用专业的语言总结：
1. 数据质量评估
2. 关键发现（温度、pH对酶活性的影响）
3. 模型预测能力评价
4. 实验优化建议
5. 后续研究方向建议

要求：结构清晰，语言专业，用中文回答。
"""

print("正在调用AI生成分析报告...")
ai_report = ask_ai(prompt)
print("\n" + "="*60)
print("AI分析报告")
print("="*60)
print(ai_report)

# 保存报告
with open('数据分析报告.txt', 'w', encoding='utf-8') as f:
    f.write("="*60 + "\n")
    f.write("实验数据分析完整报告\n")
    f.write("="*60 + "\n\n")
    f.write(ai_report)
    f.write("\n\n" + "="*60 + "\n")
    f.write(f"最优实验条件: 温度 {avg_optimal_temp:.1f}℃, pH {avg_optimal_ph:.2f}\n")
    f.write(f"预测模型最佳R²分数: {r2_rf:.4f}\n")

print("\n✓ 完整报告已保存为 '数据分析报告.txt'")
print("\n" + "="*60)
print("分析完成！生成的文件:")
print("1. 数据分析可视化.png - 6张可视化图表")
print("2. 预测效果对比.png - 模型预测效果对比")
print("3. 数据分析报告.txt - AI生成的完整分析报告")
print("="*60)