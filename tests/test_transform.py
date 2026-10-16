"""test_transform.py —— src/transform.py 的单元测试（8 组用例，共 12 个测试函数）。

━━━ 关于 np.allclose 与 1e-9 这类容差 ━━━

    旋转矩阵里的数是 sin / cos 算出来的，永远带浮点误差：
    实跑 rot_z(np.pi/2) @ [1,0,0] 得到的是 [6.123234e-17, 1.0, 0.0]，
    那个 6.12e-17 就是"本该是 0 的 0"。
    所以本项目所有浮点比较一律走 np.allclose / np.isclose，绝不写 ==。
"""

import numpy as np
import pytest

from src.transform import is_rotation, rot_x, rot_y, rot_z


# ============================================================
# 第 1 组：t = 0 必须是单位阵（最便宜的健全性检查）
# ============================================================


def test_zero_angle_gives_identity():
    """
    转 0 弧度 = 没转，必须得到单位阵 np.eye(3)。
    """
    I = np.eye(3)

    # 三个函数各查一次，一条 assert 一个函数，红了就知道是谁
    assert np.allclose(rot_x(0.0), I)
    assert np.allclose(rot_y(0.0), I)
    assert np.allclose(rot_z(0.0), I)


# ============================================================
# 第 2~4 组：方向用例 —— 抓"符号写反"
# ============================================================


def test_rot_z_90deg_maps_x_to_y():
    """绕 z 轴转 +90 度：x 轴应该被送到 y 轴。

    这是 D9 验收 4 的那条命令，也是 rot_z 最直观的物理含义：
    逆时针转 90 度，原本指向 +x 的向量现在指向 +y。
    """
    v = np.array([1.0, 0.0, 0.0])

    result = rot_z(np.pi / 2) @ v

    # 实跑结果不是干净的 [0,1,0]，而是 [6.123234e-17, 1.0, 0.0]
    # 那个极小值是 cos(pi/2) 的浮点表示 —— 所以只能用 allclose
    assert np.allclose(result, np.array([0.0, 1.0, 0.0]))


def test_rot_x_90deg_maps_y_to_z():
    """绕 x 轴转 +90 度：y 轴 -> z 轴。

    右手定则：大拇指指 +x，四指从 +y 弯向 +z，所以 y 转到 z 是正向。
    """
    v = np.array([0.0, 1.0, 0.0])

    result = rot_x(np.pi / 2) @ v

    assert np.allclose(result, np.array([0.0, 0.0, 1.0]))


def test_rot_y_90deg_maps_z_to_x():
    """
    绕 y 轴转 +90 度：z 轴 -> x 轴。
    """
    v = np.array([0.0, 0.0, 1.0])

    result = rot_y(np.pi / 2) @ v

    assert np.allclose(result, np.array([1.0, 0.0, 0.0]))


# ============================================================
# 第 5 组：所有旋转都必须是"正交 + 右手"
# ============================================================


# @pytest.mark.parametrize 是什么：
#   它让同一个测试函数用不同的输入**各跑一遍**，
#   下面两层叠起来 = 3 个函数 x 4 个角度 = 12 个测试，
#   每个都会单独显示在 -v 列表里（不是只跑 1 次！）。
#   ids=[...] 是给每组参数起个短名，否则报告里会打印整串浮点
#   （比如 1.5707963267948966），看不懂是哪个角度。
#   叠两层时的顺序是：[角度-函数名]，实际长这样 ——
#       test_..._right_handed[t=0-rot_x] PASSED
#       test_..._right_handed[t=pi/2-rot_y] PASSED
@pytest.mark.parametrize("func", [rot_x, rot_y, rot_z], ids=["rot_x", "rot_y", "rot_z"])
@pytest.mark.parametrize("t", [0.0, np.pi / 2, np.pi, -1.234],
                         ids=["t=0", "t=pi/2", "t=pi", "t=-1.234"])
def test_rotations_are_orthogonal_and_right_handed(func, t):
    """任何角度的旋转矩阵都必须满足：R.T @ R = I 且 det(R) = +1。

    这两条就是 SO(3) 的定义（特殊正交群）：
        · 正交：转完长度不变、夹角不变，且 R 的逆 = R 的转置
        · det = +1：排除镜面反射（那种"旋转"会把右手变左手）

    这条用例测试的是"数学性质"，不管具体数值 —— 所以它比方向用例更通用：
    以后加 rot_axis_angle() 之类的函数，直接把它加到上面的参数表里就行。
    """
    name = func.__name__   # 报错信息里用，告诉你挂的是哪个函数
    R = func(t)

    # 性质 1：正交 —— 转置乘自己等于单位阵
    # 这里自己写容差，不靠 np.allclose 的默认值（默认 rtol=1e-5 太松）
    assert np.allclose(R.T @ R, np.eye(3), rtol=1e-12, atol=1e-12), \
        f"{name}({t}) 不正交"

    # 性质 2：右手 —— 行列式必须精确等于 +1（同样给一点浮点容差）
    assert np.isclose(np.linalg.det(R), 1.0, rtol=1e-12, atol=1e-12), \
        f"{name}({t}) 的行列式不是 +1"


# ============================================================
# 第 6 组：is_rotation 的正面用例
# ============================================================


@pytest.mark.parametrize("func", [rot_x, rot_y, rot_z], ids=["rot_x", "rot_y", "rot_z"])
def test_is_rotation_accepts_real_rotations(func):
    """自己造出来的旋转矩阵，is_rotation 必须认。"""
    name = func.__name__
    assert is_rotation(func(0.7)) is True, f"{name} 被误判为非旋转矩阵"

    # t=0 得到的单位阵也是合法旋转（单位阵就是"不转"）
    assert is_rotation(func(0.0)) is True


def test_is_rotation_accepts_plain_list():
    """传"列表的列表"进来也不能崩 —— 这是第 0 关"入口消毒"在起作用。

    旋转矩阵的数值以后可能来自 JSON / csv / 手敲的字面量，
    那些地方给出来的都是 list，不是 ndarray。
    函数第一行的 np.asarray(R, dtype=float) 就是为这个准备的。
    """
    R_as_list = [
        [0.0, -1.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
    ]

    # 它其实是 rot_z(pi/2)，只是把里面的浮点尾巴擦干净了
    assert is_rotation(R_as_list) is True


# ============================================================
# 第 7~9 组：is_rotation 的反面用例（最容易漏掉的一类）
# ============================================================


def test_is_rotation_rejects_mirror():
    """镜面反射矩阵 diag(1, 1, -1)：正交，但 det = -1，不是旋转。

    这条用例是 is_rotation 里"第 3 关（右手关）"存在的唯一理由。
    实跑证据：
        diag(1,1,-1).T @ diag(1,1,-1) = I   -> 正交成立（第 2 关会放它过去）
        det = -1.0                          -> 第 3 关拦下
    它的物理含义：把 z 方向翻个个儿 —— 平面上看像"转了一下"，
    实际上是把右手变成了左手（照镜子），Robot 里绝不允许出现。
    """
    mirror = np.diag([1.0, 1.0, -1.0])

    # 先确认它确实通过了"正交"这一关，否则这条测试就测不到第 3 关
    assert np.allclose(mirror.T @ mirror, np.eye(3))
    assert np.isclose(np.linalg.det(mirror), -1.0)

    assert is_rotation(mirror) is False


def test_is_rotation_rejects_scale():
    """带缩放的矩阵 2*eye(3)：长度被拉长了一倍，连正交都不满足。

    实跑：det = 8.0（不是 ±1），(2I).T @ (2I) = 4I ≠ I
    """
    scale = 2.0 * np.eye(3)

    assert is_rotation(scale) is False


def test_is_rotation_rejects_wrong_shape():
    """形状不对的一律 False，不允许悄悄通过或者抛异常。

    三种情况：
        · 2x2 单位阵  -> 维度不对（本项目只用 3x3）
        · 4x4 单位阵  -> 以后做齐次变换时会出现，但它不是 3x3 旋转
        · 一维向量    -> 根本不是矩阵
    """
    assert is_rotation(np.eye(2)) is False
    assert is_rotation(np.eye(4)) is False
    assert is_rotation(np.array([1.0, 0.0, 0.0])) is False


# ============================================================
# 第 10~11 组：返回值规格 + 数学性质
# ============================================================


def test_return_type_shape_and_dtype():
    """返回值的"规格"必须稳定：ndarray、(3,3)、float64。

    为什么要单独测这个：后面 src/robot.py 会把这些返回值直接塞进矩阵连乘，
    形状或 dtype 一变，错误会出现在很远的地方（很难查）。
    把规格钉在测试里，改坏了立刻红在本地。
    """
    R = rot_z(0.3)

    assert isinstance(R, np.ndarray)         # 是数组，不是 list
    assert R.shape == (3, 3)                 # 3x3，一行不多一列不少
    assert R.dtype == np.float64             # 浮点，别变成整数或 object


def test_rotations_do_not_commute():
    """旋转不能交换顺序：rot_x(a) @ rot_y(b) 不等于 rot_y(b) @ rot_x(a)。

    实跑：max|rx@ry - ry@rx| = 1.0（差得非常多，不是浮点误差）

    这条为什么要测：
        1) 它是"欧拉角为什么有歧义"的根源 —— 同样三个角，换个顺序结果完全不同
        2) 后面 W8 的 DH 连乘是"一串矩阵相乘"，顺序绝对不能调换，
           这条用例就是先用最简单的方式把这个事实钉死
    """
    rx = rot_x(np.pi / 2)
    ry = rot_y(np.pi / 2)

    # 先确认两个乘积各自都还是合法旋转（顺序换了，但它们各自都是 SO(3) 的元素）
    assert is_rotation(rx @ ry) is True
    assert is_rotation(ry @ rx) is True

    # 关键断言：换个顺序就**不**相等
    assert not np.allclose(rx @ ry, ry @ rx)
