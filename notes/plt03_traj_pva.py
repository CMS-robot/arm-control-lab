"""正弦轨迹的位置 / 速度 / 加速度 —— D13 交付物。

题目：给定关节角轨迹 p(t) = A·sin(ωt)，用 np.gradient 从【位置】数值求出
速度和加速度，和解析式逐点对比，画出 p / v / a 三条曲线。

    A     = 1.0 rad      振幅（关节转 ±1 弧度）
    ω     = 2π rad/s     一秒钟正好一个来回
    T     = 2.0 s        跑两个周期
    N     = 2001 点      ← 必须是 2001，见下面的"陷阱 1"

为什么值得单独做这件事：
    真机上只有编码器读数，拿不到解析的 p(t)，所以"从位置差分出速度和加速度"
    是绕不过去的一步。但差分到底准不准、什么时候会崩，光看公式看不出来，
    必须把误差量出来。这个脚本就是把这层"看不见的误差"变成桌子上的数字。

三个必须记住的坑（代码里都标了 [陷阱 x]）：
    1. N 取 2000 会让 dt = 0.0010005 而不是 0.001，误差表全部对不上
    2. np.gradient 的第二个参数是【采样间隔 spacing】，不是"求几阶导"
       不传 dt 时结果会小 1/dt 倍（本例 1000 倍），而且【不报错】
    3. 加速度曲线比速度曲线毛刺，不是画图的问题，是差分本身在放大噪声：
       两次求导把 σ=1e-4 的噪声放大到 218，比加速度本身的幅值 39.5 还大 5 倍

运行：
    cd D:\\arm-control-lab
    python notes/plt03_traj_pva.py
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# 中文字体 + 负号（SimHei 里没有 U+2212 数学减号，不关掉负号就变方框）
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

# ========== 0. 参数 ==========
A = 1.0              # 振幅 rad
OMEGA = 2 * np.pi    # 角频率 rad/s -> 周期 1 s
T_END = 2.0          # 总时长 s
N = 2001             # 采样点数

t = np.linspace(0.0, T_END, N)
dt = t[1] - t[0]

# [陷阱 1] 为什么是 2001 不是 2000：
#   2001 个点把 [0, 2] 切成 2000 段 -> dt 正好 0.001
#   2000 个点只切成 1999 段 -> dt = 2/1999 = 0.001000500...
#   差 5e-7 看着无所谓，但误差是 O(dt²)、还要乘 1000 倍放大，最后数字对不上
dt_if_2000 = T_END / (2000 - 1)

# 解析解（真值）
p_exact = A * np.sin(OMEGA * t)                 # 位置
v_exact = A * OMEGA * np.cos(OMEGA * t)         # 速度 = dp/dt
a_exact = -A * OMEGA ** 2 * np.sin(OMEGA * t)   # 加速度 = dv/dt

# 数值解：只给位置，其余靠差分
p_num = p_exact.copy()                          # 位置是"测到的"，本身就是真值
v_num = np.gradient(p_num, dt)                  # 一阶中心差分
a_num = np.gradient(v_num, dt)                  # 再差一次 = 二阶

# 误差（注意必须【先减再取绝对值】）
err_v = np.abs(v_num - v_exact)
err_a = np.abs(a_num - a_exact)

print("=" * 70)
print("[1] 参数与采样间隔")
print(f"    A = {A} rad   ω = 2π = {OMEGA:.6f} rad/s   T = {T_END} s")
print(f"    N = {N}        dt = {dt:.10f}")
print(f"    若改用 N=2000  dt = {dt_if_2000:.10f}   <- 不是整数毫秒，误差表会偏")
print(f"    位置幅值 {np.abs(p_exact).max():.3f} rad | "
      f"速度幅值 {np.abs(v_exact).max():.3f} rad/s | "
      f"加速度幅值 {np.abs(a_exact).max():.3f} rad/s²")

print()
print("[2] 抽点对比（看数值解贴不贴解析解）")
print("        t(s)      p_num       v_num       v_exact      a_num       a_exact")
for i in (0, 1, 500, 1000, 1500, 1999, 2000):
    print(f"    {t[i]:8.4f} {p_num[i]:11.6f} {v_num[i]:11.6f} {v_exact[i]:11.6f}"
          f" {a_num[i]:11.6f} {a_exact[i]:11.6f}")

print()
print("[3] 最大误差：内部 vs 首尾")
print(f"    速度误差  内部(1..-2) = {err_v[1:-1].max():.3e}   含首尾 = {err_v.max():.3e}")
print(f"    加速度误差 内部(1..-2) = {err_a[1:-1].max():.3e}   含首尾 = {err_a.max():.3e}")
print("    -> 首尾用的是单侧差分（只有一个邻居），精度从 O(dt²) 掉到 O(dt)，")
print("       所以加速度的首尾误差比内部大 200 多倍。真实数据里首尾两点不可信。")

# 理论值核对：中心差分误差 = -(dt²/6)·f'''
#   速度的 f''' = -Aω³cos  -> 最大 Aω³ = 248.05 -> dt²/6*248.05 = 4.134e-05
#   加速度是两次差分叠加，等效 stencil 更宽，系数变成 dt²/3 —— 正好 4 倍
print(f"    理论值：速度 {dt**2 / 6 * A * OMEGA**3:.3e}   加速度 {dt**2 / 3 * A * OMEGA**4:.3e}")

print()
print("[4] allclose 判定（rtol=1e-4, atol=1e-6）")
print(f"    速度  全体 = {np.allclose(v_num, v_exact, rtol=1e-4, atol=1e-6)}   "
      f"内部 = {np.allclose(v_num[1:-1], v_exact[1:-1], rtol=1e-4, atol=1e-6)}")
print(f"    加速度 全体 = {np.allclose(a_num, a_exact, rtol=1e-4, atol=1e-6)}  "
      f"内部 = {np.allclose(a_num[1:-1], a_exact[1:-1], rtol=1e-4, atol=1e-6)}")
print("    -> 加速度【全体 False 不是算错了】：内部完全吻合，只是首尾单侧差分超差。")
print("       所以验收数值微分必须写明「比哪一段」，否则 False 会骗人。")

print()
print("[5] [陷阱 2] 忘了传 dt 会怎样")
i_mid = N // 4                       # t = 0.5 s 处，速度取最大值
v_no_dt = np.gradient(p_num)         # 少写第二个参数
print(f"    gradient(p)          t=0.5s 处 = {v_no_dt[i_mid]:.9f}")
print(f"    gradient(p, dt)      t=0.5s 处 = {v_num[i_mid]:.9f}")
print(f"    解析值               t=0.5s 处 = {v_exact[i_mid]:.9f}")
print(f"    比值 = {v_no_dt[i_mid] / v_num[i_mid]:.6f}   ≈ 1/dt = {1 / dt:.1f}")
print("    -> 结果小了 1000 倍，但【全程不报错、图照样画得出来】，")
print("       这种错只能靠「和解析解比」或「看数量级」抓出来。")

print()
print("[6] 噪声放大实验（回答「为什么加速度比速度更毛刺」）")
print("    位置加 σ = 1e-4 rad 的高斯噪声（编码器量化误差就是这个量级）")
print(f"    {'N':>6} {'dt':>10} {'v误差':>11} {'a误差':>11} {'a噪声/幅值':>12}")
rng = np.random.default_rng(2026)
for n in (201, 2001, 50001):
    tt = np.linspace(0.0, T_END, n)
    h = tt[1] - tt[0]
    p_clean = A * np.sin(OMEGA * tt)
    p_noisy = p_clean + rng.normal(0.0, 1e-4, n)
    v_n = np.gradient(p_noisy, h)
    a_n = np.gradient(v_n, h)
    ev = np.abs(v_n[1:-1] - A * OMEGA * np.cos(OMEGA * tt)[1:-1]).max()
    ea = np.abs(a_n[1:-1] + A * OMEGA ** 2 * np.sin(OMEGA * tt)[1:-1]).max()
    print(f"    {n:>6} {h:>10.2e} {ev:>11.3e} {ea:>11.3e} {ea / (A * OMEGA ** 2):>12.1f}")
print("    规律：不加噪声时 dt 越小越准（O(dt²)）；加了噪声【反过来】，dt 越小越糟")
print("          一阶差分 ≈ σ√2/(2dt)、二阶差分 ≈ σ√6/dt²。采样率越高，噪声被放大得越狠。")

# ========== 画图 ==========
# 三条曲线量级差 40 倍（1 / 6.3 / 39.5），硬塞进一张图看不出细节 -> 上下三格
# sharex=True 让三格共用 x 轴：只保留最下面一格的刻度，缩放时同步
fig, axes = plt.subplots(
    3, 1, figsize=(9.5, 9.0), sharex=True,
    gridspec_kw={"height_ratios": [1, 1, 1.25]},
)

pairs = [
    (p_exact, p_num, r"$p = A\,\sin(\omega t)$", "位置", r"位置 $p$ (rad)", None),
    (v_exact, v_num, r"$v = A\omega\cos(\omega t)$", "速度",
     r"速度 $v$ ($\mathrm{rad\cdot s^{-1}}$)", err_v),
    (a_exact, a_num, r"$a = -A\omega^{2}\sin(\omega t)$", "加速度",
     r"加速度 $a$ ($\mathrm{rad\cdot s^{-2}}$)", err_a),
]

for k, (ax, (y_ex, y_nu, tex, name, ylabel, err)) in enumerate(zip(axes, pairs)):
    # 解析解用虚线画在后面，数值解用粗实线：重合 = 完全吻合
    ax.plot(t, y_ex, color="#888888", linewidth=2.6, linestyle="--",
            label="解析解（真值）", zorder=2)
    ax.plot(t, y_nu, color="#1f77b4", linewidth=1.6, label="数值差分", zorder=3)
    ax.axhline(0.0, color="gray", linewidth=0.7, linestyle=":")
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(tex + f" —— {name}", fontsize=12.5, loc="left")
    ax.grid(linestyle="--", alpha=0.4)
    ax.legend(loc="upper right", fontsize=9.5, framealpha=0.92, ncol=2)

    if err is not None:
        # 误差标注必须有白底 bbox，否则被曲线压住看不清
        ax.text(
            0.015, 0.06,
            "内部最大误差 %.2e   首尾 %.2e" % (err[1:-1].max(), err.max()),
            transform=ax.transAxes, fontsize=9.5, color="#c0392b",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.88, pad=3),
        )
    else:
        ax.text(
            0.015, 0.06, "位置是差分【输入】，误差恒为 0 —— 所以两条线完全重合",
            transform=ax.transAxes, fontsize=9.5, color="#c0392b",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.88, pad=3),
        )

axes[0].set_ylim(-1.35, 1.35)
axes[1].set_ylim(-8.6, 8.6)
axes[2].set_ylim(-52, 66)
axes[-1].set_xlim(0, T_END)
axes[-1].set_xlabel(r"时间 $t$ (s)", fontsize=11)

fig.suptitle(
    r"从位置差分到加速度：$A=1\,\mathrm{rad},\ \omega=2\pi\,\mathrm{rad\cdot s^{-1}}$"
    "\n" r"灰色虚线 = 解析真值，蓝色实线 = 差分结果（$N=2001$, $\Delta t=1\,\mathrm{ms}$）",
    fontsize=13.5,
)
fig.tight_layout(rect=(0, 0, 1, 0.955))

# ========== 保存 ==========
# 放 results/：这是"运行产物"，.gitignore 里 results/* 已忽略，不入库，
# 一条命令就能重新生成；要贴进 README 才需要再拷一份到 media/。
out = Path(__file__).resolve().parents[1] / "results" / "traj_sine_pva.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=130)
print()
print("=" * 70)
print(f"[7] 已保存：{out}")
print(f"    文件存在 = {out.exists()} | 大小 = {out.stat().st_size} B")
plt.close(fig)
