"""把 rot_z 的旋转过程画出来 —— D14 检查点 2。

题目：让单位向量 [1, 0, 0] 绕 z 轴转一整圈，把"旋转"这个抽象操作变成图。

    t = np.linspace(0, 2*np.pi, 200)
    v(t) = rot_z(t) @ [1, 0, 0]

    子图 1：x(t) 和 y(t) 两条曲线 —— 应该正好是 cos / sin
    子图 2：x-y 平面上的轨迹 —— 应该是一个单位圆

为什么值得单独产一张图：
    D9 的测试只能证明 rot_z "数学上没写错"，但看不出它"物理上在干什么"。
    README 里放一张旋转圆，比贴一堆 assert 输出有说服力得多。

三个必须记住的点（都在下面代码里标了）：
    1. rot_z 只接受标量角度，直接传数组会崩，而且报错信息完全看不懂
       -> 只能逐个算，再用 np.array 摞起来
    2. 画圆必须 set_aspect("equal")，否则会被拉成椭圆
       -> 实测 subplots(2,1,figsize=(10,8)) 不设时横纵比是 2.768，圆会变成 3:1 的扁饼
    3. rot_z(2π) 不等于单位阵，终点和起点差 2.45e-16
       -> 视觉闭合、数值不闭合，这正是 D9 里 is_rotation 要用容差判断的原因
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# notes/ 下的脚本被直接运行时，sys.path[0] 是 notes/ 而不是仓库根，
# 所以 import src.xxx 会失败。手动把仓库根塞进搜索路径。
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.transform import rot_z

# 中文与负号。单文件脚本用顶层 rcParams 没问题（做成可 import 的模块才要用 rc_context）
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

# ========== 1. 生成数据 ==========
N = 200
t = np.linspace(0.0, 2 * np.pi, N)   # 从 0 转到 2π，正好一整圈
v0 = np.array([1.0, 0.0, 0.0])       # 初始向量：指向 +x

# 陷阱 1：rot_z 内部写的是 np.cos(t) 放进 3x3 矩阵，
# 传数组进去会得到一个残缺的矩阵，然后 numpy 报
#   ValueError: ... inhomogeneous shape after 2 dimensions
# 这个报错完全看不出真正原因，所以必须逐个标量算。
V = np.array([rot_z(ti) @ v0 for ti in t])   # (N, 3)，每行是一个时刻的向量

x = V[:, 0]
y = V[:, 1]

# ========== 2. 自检（跑不过就说明哪一步错了）==========
assert V.shape == (N, 3), f"V 形状不对：{V.shape}"
assert np.allclose(x, np.cos(t), atol=1e-12), "x 分量不等于 cos(t)"
assert np.allclose(y, np.sin(t), atol=1e-12), "y 分量不等于 sin(t)"
assert np.allclose(V[:, 2], 0.0, atol=1e-15), "z 分量不恒为 0，向量跑出 xy 平面了"

# 起点与终点的距离：看"转一圈有没有回到原位"
gap = np.linalg.norm(V[-1] - V[0])

print("=" * 66)
print("[1] 形状与自检")
print(f"    V.shape = {V.shape}   (200 个时刻 x 3 个分量)")
print(f"    x 是否等于 cos(t) : {np.allclose(x, np.cos(t), atol=1e-12)}")
print(f"    y 是否等于 sin(t) : {np.allclose(y, np.sin(t), atol=1e-12)}")
print(f"    z 是否恒为 0      : {np.allclose(V[:, 2], 0.0, atol=1e-15)}")

print()
print("[2] 抽几个角度看向量指向哪里")
print("       t(rad)        x          y          z")
for i in (0, 25, 50, 100, 150, 199):
    print(f"    {t[i]:9.4f}  {x[i]:10.6f} {y[i]:10.6f} {V[i, 2]:10.6f}")

print()
print("[3] 转一整圈回到起点了吗")
print(f"    t=0   的向量 : [{x[0]:.6f}, {y[0]:.6f}, {V[0, 2]:.6f}]")
print(f"    t=2pi 的向量 : [{x[-1]:.6f}, {y[-1]:.6f}, {V[-1, 2]:.6f}]")
print(f"    两点距离     : {gap:.3e}   <- 视觉重合，数值不严格相等")

# ========== 3. 画图 ==========
# height_ratios 让下面那张（画圆的）分到更多高度，圆才不显小
fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(8.5, 10.5), gridspec_kw={"height_ratios": [1, 1.35]}
)

# ---------- 子图 1：两个分量随时间 ----------
ax1.plot(t, x, color="#1f77b4", linewidth=2.2, label=r"$x(t) = \cos t$")
ax1.plot(t, y, color="#d62728", linewidth=2.2, label=r"$y(t) = \sin t$")
ax1.axhline(0.0, color="gray", linewidth=0.7, linestyle=":")

# x 轴刻度换成 π 的倍数，比 0/1.57/3.14 好读
ax1.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
ax1.set_xticklabels(["0", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
ax1.set_xlim(0, 2 * np.pi)
ax1.set_ylim(-1.5, 1.62)
ax1.set_yticks([-1, -0.5, 0, 0.5, 1])
ax1.set_xlabel(r"旋转角 $t$  (rad)")
ax1.set_ylabel("分量值")
ax1.set_title(
    r"子图 1：向量的两个分量随角度变化 —— $x$ 走余弦、$y$ 走正弦",
    fontsize=12.5, loc="left",
)
ax1.grid(linestyle="--", alpha=0.4)
ax1.legend(loc="upper right", fontsize=11, framealpha=0.92)

# 标出 t=0 那一刻 x=1、y=0，帮读者对上子图 2 的起点
ax1.annotate(
    r"$t=0$：向量指向 $+x$，所以 $x=1,\ y=0$",
    xy=(0, 1), xytext=(0.5, 1.3),
    fontsize=9.5, color="#444444",
    arrowprops=dict(arrowstyle="->", color="#888888", lw=0.9),
    bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=2.5),
)

# ---------- 子图 2：xy 平面上的轨迹 ----------
ax2.plot(x, y, color="#1f77b4", linewidth=2.2, zorder=3)
ax2.axhline(0.0, color="gray", linewidth=0.7, linestyle=":")
ax2.axvline(0.0, color="gray", linewidth=0.7, linestyle=":")

# 陷阱 2：不写这一行，圆会被拉伸成椭圆。
# 实测 subplots(2,1,figsize=(10,8)) 不设时横纵比 2.768，设了是 1.000。
ax2.set_aspect("equal")

ax2.set_xlim(-1.4, 1.4)
ax2.set_ylim(-1.42, 1.5)
# 刻度只标到 ±1（圆的范围内），避免出现 1.5 这种和圆无关的刻度
ax2.set_xticks([-1, -0.5, 0, 0.5, 1])
ax2.set_yticks([-1, -0.5, 0, 0.5, 1])
ax2.set_xlabel(r"$x$")
ax2.set_ylabel(r"$y$")
ax2.set_title(
    r"子图 2：$x$-$y$ 平面上的轨迹 —— 一个半径 1 的正圆",
    fontsize=12.5, loc="left",
)
ax2.grid(linestyle="--", alpha=0.4)

# 起点：故意画成空心圈，避免和轨迹线混在一起
ax2.plot([1.0], [0.0], marker="o", markersize=9, markerfacecolor="white",
         markeredgecolor="#2ca02c", markeredgewidth=2.2, zorder=6)
ax2.annotate(
    "起点 = 终点\n" + r"$t=0$ 与 $t=2\pi$",
    xy=(1.0, 0.0), xytext=(1.03, -0.66),
    fontsize=9.5, color="#2ca02c", ha="left",
    arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=1.0),
    bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=2.5),
)

# 旋转方向：沿圆周【切线】画箭头，不要用两点连线（连线会切进圆内）
# 逆时针的切线方向 = d/dt (cos t, sin t) = (-sin t, cos t) = (-y, x)
i_arrow = 120
tx, ty = -y[i_arrow], x[i_arrow]      # 单位切线
L = 0.30                              # 箭头总长（数据坐标）
ax2.annotate(
    "",
    xy=(x[i_arrow] + L * tx, y[i_arrow] + L * ty),
    xytext=(x[i_arrow] - L * tx, y[i_arrow] - L * ty),
    arrowprops=dict(arrowstyle="-|>", color="#ff7f0e",
                    lw=2.6, mutation_scale=26),
    zorder=7,
)
ax2.text(
    -1.36, 1.27, "逆时针旋转（右手定则，从 +z 方向看）",
    fontsize=9.5, color="#ff7f0e", ha="left",
)

# 标注 90° 位置，让读者能把子图 2 的点对回子图 1 的曲线
# （轴线已经由上面的 axvline 画好，这里不再重复画半径线）
ax2.annotate(
    r"$t=\pi/2$：" + "\n" + r"向量转到 $+y$",
    xy=(0.04, 1.0), xytext=(1.05, 1.12),
    fontsize=9.5, color="#555555", ha="left",
    arrowprops=dict(arrowstyle="->", color="#888888", lw=0.9),
    bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=2.5),
)

# 把"转一圈没严格闭合"这件事写在图上 —— 这是这张图最有信息量的一点
ax2.text(
    0.02, 0.03,
    "终点与起点的距离 = %.2e\n视觉重合，数值不严格相等" % gap,
    transform=ax2.transAxes, fontsize=9.5, color="#444444",
    bbox=dict(facecolor="white", edgecolor="none", alpha=0.88, pad=3),
)

fig.suptitle(
    r"$\mathrm{rot\_z}(t)$ 把单位向量 $[1,0,0]$ 转一整圈",
    fontsize=15,
)
fig.tight_layout(h_pad=2.4)

# ========== 4. 保存 ==========
# 放在 media/ 而不是 results/：
# .gitignore 里 results/* 会把图全部忽略掉，README 引用就成了裂图。
out = Path(__file__).resolve().parents[1] / "media" / "rot_z_circle.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=130)

print()
print("=" * 66)
print(f"[4] 已保存：{out}")
print(f"    文件存在 = {out.exists()} | 大小 = {out.stat().st_size} B")
plt.close(fig)
