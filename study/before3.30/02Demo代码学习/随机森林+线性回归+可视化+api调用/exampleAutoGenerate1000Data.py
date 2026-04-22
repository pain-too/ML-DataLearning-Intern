import pandas as pd
import numpy as np

# 设置随机种子，保证结果可重复
np.random.seed(42)

# 生成1000条实验数据
n_samples = 1000

# 温度：22-28度之间，符合正态分布
temperature = np.random.normal(25, 1.5, n_samples)
temperature = np.clip(temperature, 22, 28)

# pH值：6.5-7.5之间
ph = np.random.normal(7.0, 0.3, n_samples)
ph = np.clip(ph, 6.5, 7.5)

# 构建关系：酶活性与温度、pH的关系（添加一些噪声）
# 最佳温度25度，最佳pH 7.0
optimal_temp = 25
optimal_ph = 7.0

# 计算酶活性（使用二次函数模拟，越接近最佳条件活性越高）
temp_effect = -0.5 * (temperature - optimal_temp)**2
ph_effect = -100 * (ph - optimal_ph)**2
noise = np.random.normal(0, 15, n_samples)  # 随机误差

enzyme_activity = 150 + temp_effect + ph_effect + noise
enzyme_activity = np.clip(enzyme_activity, 50, 200)  # 限制在合理范围

# 吸光度与酶活性正相关（加噪声）
od450 = 0.002 * enzyme_activity + np.random.normal(0, 0.03, n_samples)
od450 = np.clip(od450, 0.1, 0.8)

# 创建DataFrame
df_large = pd.DataFrame({
    '样本编号': range(1, n_samples + 1),
    '温度(℃)': np.round(temperature, 1),
    'pH值': np.round(ph, 2),
    '酶活性(U/mL)': np.round(enzyme_activity, 1),
    '吸光度OD450': np.round(od450, 3)
})

# 保存
df_large.to_csv('实验数据_1000条.csv', index=False, encoding='utf-8-sig')
print(f"已生成 {n_samples} 条数据，保存为 '实验数据_1000条.csv'")
print(df_large.head())