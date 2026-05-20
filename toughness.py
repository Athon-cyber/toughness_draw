import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

# --- 1. 设置学术风格 ---
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.unicode_minus'] = False

# --- 2. 生成模拟数据 (调整部分) ---
np.random.seed(42)
# 增加采样密度 (从15改到25)，使表面看起来更连续，不那么"离散"
x = np.linspace(0, 750, 15) 
y = np.linspace(0, 750, 15)
X, Y = np.meshgrid(x, y)

# 关键调整：大幅减小波动幅度
# 原系数是 0.5，现在改为 0.1；噪声从 0.2 改为 0.05
# 这样点云就会非常靠近基准面
Z_base = 10000*(0.005 * np.sin(X) + 0.005 * np.cos(Y))
Z_noise = np.random.normal(0, 0.005, X.shape)
Z = Z_base + Z_noise

# 拟合基准平面 (均值面)
Z_plane = np.mean(Z) * np.ones_like(Z)

# --- 3. 绘图设置 ---
fig = plt.figure(figsize=(10, 7), dpi=150)
ax = fig.add_subplot(111, projection='3d')

# --- 4. 绘制元素 ---

# (A) 绘制点云
# 使用更小的点 (s=15) 和稍微深一点的蓝色，看起来更精致
ax.scatter(X, Y, Z, c='#1f77b4', marker='o', s=15, alpha=0.7, edgecolors='none', label='Measurement Points')

# (B) 绘制拟合基准平面
# 使用浅灰色，透明度适中
ax.plot_surface(X, Y, Z_plane, color='#bdc3c7', alpha=0.3, shade=False)
# 加一个边缘框，增强平面的立体感
ax.plot_wireframe(X, Y, Z_plane, color='gray', alpha=0.2, rstride=25, cstride=25)

z_center = np.mean(Z)
z_range = np.max(Z) - np.min(Z)
ax.set_zlim(z_center - z_range, z_center + z_range)

ax.set_xlabel('X (μm)', labelpad=10, ha='center')
ax.set_ylabel('Y (μm)', labelpad=10, ha='center')
ax.set_zlabel('Z (μm)', labelpad=10, ha='center')


# 去除背景色，纯白背景适合论文
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.grid(False) # 去掉默认网格，更干净

# --- 6. 自定义图例 ---
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#1f77b4', label='Surface points'),
    Line2D([0], [0], color='#bdc3c7', lw=4, label='Fitted plane'),
    # Line2D([0], [0], color='#d62728', lw=2, label=r'Vertical Deviation $d_i$'),
]
ax.legend(handles=legend_elements, loc='upper left', frameon=True, fancybox=False, edgecolor='black')

# 调整视角：稍微俯视一点，看清平面关系
ax.view_init(elev=25, azim=-60)

plt.tight_layout()
plt.show()
plt.savefig("surface_3d.png")