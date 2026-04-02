import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.signal import find_peaks

# 配置中文显示
rcParams['font.family'] = 'Songti SC'
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 读取数据
dataframe = pd.read_excel('yzs.xlsx')

# 定义 x 和 y（必须在使用前赋值）
x = dataframe['U_G2K (V)']
y = dataframe['I_A (×10⁻⁶A)']

# 创建画布
plt.figure(figsize=(10, 6))

# 绘制曲线

plt.plot(x, y, linewidth=1.5, label='实验曲线')

# 自动找峰值（峰）
peaks, _ = find_peaks(y, distance=10)
peak_x = x.iloc[peaks]
peak_y = y.iloc[peaks]

# 自动找谷值（谷：对-y找峰，就是原数据的谷）
valleys, _ = find_peaks(-y, distance=10)
valley_x = x.iloc[valleys]
valley_y = y.iloc[valleys]

# 标注峰值
plt.scatter(peak_x, peak_y, color='red', s=50, zorder=5)
for px, py in zip(peak_x, peak_y):
    plt.text(px, py+0.3, f'({px:.1f}, {py:.1f})', fontsize=8, color='red', ha='center')

# 标注谷值
plt.scatter(valley_x, valley_y, color='blue', s=50, zorder=5)
for vx, vy in zip(valley_x, valley_y):
    plt.text(vx, vy-0.5, f'({vx:.1f}, {vy:.1f})', fontsize=8, color='blue', ha='center')

# 添加标题和坐标轴
plt.xlim(0,82)
plt.ylim(0,7.5)
plt.title('于泽深数据', fontsize=17, color='black')
plt.xlabel('电压G2k/V', fontsize=10)
plt.ylabel('测试电流/×10⁻⁶A', fontsize=10)
plt.grid(alpha=0.5)
plt.legend()

# 显示图表
plt.show()