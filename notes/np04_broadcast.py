"""
D7 交付物：一次算 1000 个向量旋转（不许用 for）

把 1000 个二维向量堆成 (1000, 2)，用一次矩阵乘法全部转完，
再写一个逐向量循环的对照版对拍，最后对比两者的耗时。
"""

import timeit

import numpy as np
from numpy import linalg as LA

N = 1000           # 向量个数
THETA_DEG = 90.0   # 逆时针旋转角度

# ---------- 1. 构造数据 ----------

# 单位圆上均匀取 N 个点，每行一个向量，形状 (N, 2)
phi = np.linspace(0.0, 2.0 * np.pi, N, endpoint=False)
V = np.stack([np.cos(phi), np.sin(phi)], axis=1)

# 旋转矩阵（逆时针）
#     [[ cos, -sin],
#      [ sin,  cos]]
theta = np.deg2rad(THETA_DEG)
c, s = np.cos(theta), np.sin(theta)
R = np.array([[c, -s],
              [s,  c]])

# ---------- 2. 批量版：一次算完 1000 个，没有 for ----------

V_batch = V @ R.T    # 向量按行堆叠时，转置加在右边


# ---------- 3. for 对照版：一个向量一个向量转，只用来对拍 ----------

def rotate_loop(V, R):
    """老老实实逐个转，作为验收基准。"""
    out = np.empty_like(V)
    for i in range(len(V)):
        out[i] = R @ V[i]
    return out


V_loop = rotate_loop(V, R)

# ---------- 4. 校验 ----------

print(f"V.shape       = {V.shape}     # 每行一个向量")
print(f"R =")
print(np.round(R, 6))
print(f"V_batch.shape = {V_batch.shape}")
print()

# 单点方向验：专门用来卡「转置加错边」
v1 = np.array([1.0, 0.0])
v2 = np.array([0.0, 1.0])
print(f"(1,0) 转 {THETA_DEG:.0f} 度  ->  {np.round(v1 @ R.T, 6)}")
print(f"(0,1) 转 {THETA_DEG:.0f} 度  ->  {np.round(v2 @ R.T, 6)}")
print(f"反面教材：写成 (1,0) @ R  ->  {np.round(v1 @ R, 6)}   <- 转反了")
print()

print(f"两版结果 allclose     -> {np.allclose(V_batch, V_loop)}")
print(f"旋转后长度仍然是 1    -> {np.allclose(LA.norm(V_batch, axis=1), 1.0)}")
print()

# ---------- 5. 计时（取最快一次，避免被系统抖动干扰）----------

REPEAT = 200
NAMESPACE = {"V": V, "R": R, "rotate_loop": rotate_loop}

t_batch = min(timeit.repeat("V @ R.T", globals=NAMESPACE,
                            number=1, repeat=REPEAT)) * 1e6
t_loop = min(timeit.repeat("rotate_loop(V, R)", globals=NAMESPACE,
                           number=1, repeat=REPEAT)) * 1e6

print(f"{N} 个向量旋转一次（取 {REPEAT} 次最快）：")
print(f"  批量版（无 for）: {t_batch:8.1f} us")
print(f"  for 版          : {t_loop:8.1f} us")
print(f"  提速            : {t_loop / t_batch:8.1f} 倍")
