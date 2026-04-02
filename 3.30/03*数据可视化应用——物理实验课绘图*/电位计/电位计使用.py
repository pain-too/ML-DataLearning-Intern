import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.interpolate import make_interp_spline
from matplotlib import rcParams
# ---------------------- 你的数据 ----------------------
rcParams['font.family'] = 'Songti SC'
data = {
    "温度 t/°C": [40, 50, 60, 70, 80, 90],
    "均值/mV": [1.481, 2.074, 2.456, 2.857, 3.208, 3.625]
}
df = pd.DataFrame(data)

# ---------------------- 线性拟合 ----------------------
t = df["温度 t/°C"].values.reshape(-1, 1)
E_mean = df["均值/mV"].values
model = LinearRegression()
model.fit(t, E_mean)
k = model.coef_[0]
b = model.intercept_

# ---------------------- 平滑曲线插值 ----------------------
t_raw = df["温度 t/°C"].values
E_raw = df["均值/mV"].values
t_smooth = np.linspace(t_raw.min(), t_raw.max(), 300)
spl = make_interp_spline(t_raw, E_raw, k=3)
E_smooth = spl(t_smooth)

# ---------------------- 绘图 ----------------------
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(8, 5))

# 1. 原始散点
plt.scatter(t_raw, E_raw, color='blue', s=50, label='实验均值数据', zorder=5)
# 2. 平滑连接散点的曲线
plt.plot(t_smooth, E_smooth, color='blue', linestyle='-', label='原始数据平滑曲线', zorder=4)
# 3. 拟合直线
t_fit = np.linspace(40, 90, 100)
E_fit = k * t_fit + b
plt.plot(t_fit, E_fit, color='red', linestyle='--', label=f'拟合直线: E = {k:.4f}t + {b:.4f}', zorder=3)

# 图表美化
plt.title('数学2402罗文凡 2024014498', fontsize=15)
plt.xlabel('温度 t / °C', fontsize=12)
plt.ylabel('温差电动势 E / mV', fontsize=12)
plt.grid(alpha=0.3)
plt.legend()
plt.xlim(35, 95)
plt.ylim(1.2, 3.9)

plt.show()