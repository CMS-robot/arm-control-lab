"""
作用：把机械臂的 DH 参数表写进项目，供后面的运动学 / 动力学 / 仿真模块统一读取。
机型：Franka Research 3（FR3），七自由度。
约定：Modified DH（Craig 约定）—— 不是 Standard DH，变换顺序不一样。
单位：a、d 用米；表里 alpha 存弧度，打印时才转成度。
设计：数据藏在模块内部（名字以下划线开头），外面一律通过函数获取。
      函数每次给一份副本 —— 外面怎么改，都污染不到本模块的数据。
"""

import math
PI_2 = math.pi / 2

# ─────────────────────────────────────────────────────────────
# 内部数据（下划线开头是约定：私有）
# ─────────────────────────────────────────────────────────────

# 1. DH 参数表
#    外层 list —— 顺序本身就是数据：按「基座 → 末端」的连接顺序排列
#    内层 dict —— 用名字取值（joint["a"]），不用记「第 3 个元素是啥」
#    注意 theta 不在这张表里：它是关节变量，机械臂动的时候它一直在变

_FR3_DH = [
    {"name": "J1", "a": 0.0, "d": 0.333, "alpha": 0.0},
    {"name": "J2", "a": 0.0, "d": 0.0, "alpha": -PI_2},
    {"name": "J3", "a": 0.0, "d": 0.316, "alpha": PI_2},
    {"name": "J4", "a": 0.0825, "d": 0.0, "alpha": PI_2},
    {"name": "J5", "a": -0.0825, "d": 0.384, "alpha": -PI_2},
    {"name": "J6", "a": 0.0, "d": 0.0, "alpha": PI_2},
    {"name": "J7", "a": 0.088, "d": 0.0, "alpha": PI_2},
]

# 法兰安装面：在 J7 坐标系前方 0.107 m（官方表单列的 Flange 行）
_FLANGE_OFFSET = 0.107

# 关节限位（弧度）。写进配置里，免得以后逆解、轨迹规划到处硬编码同一个数。
# J4、J6 的区间「不包含 0」，这是 Franka 的结构特点。
_JOINT_LIMITS = [
    (-2.9007, 2.9007),   # J1  ±166.2°
    (-1.8361, 1.8361),   # J2  ±105.2°
    (-2.9007, 2.9007),   # J3  ±166.2°
    (-3.0770, -0.1169),  # J4  -176.3° ~ -6.7°   全负，不含 0
    (-2.8763, 2.8763),   # J5  ±164.8°
    (0.4398, 4.6216),    # J6  +25.2° ~ +264.8°  全正，不含 0
    (-3.0508, 3.0508),   # J7  ±174.8°
]


# ─────────────────────────────────────────────────────────────
# 取数据：一律返回副本，外面改不到内部
# ─────────────────────────────────────────────────────────────

def load_dh():
    """
    返回 DH 参数表（7 个关节）。
    """
    return [dict(joint) for joint in _FR3_DH]

def load_joint_limits():
    """
    返回 7 个关节的 (下限, 上限)，单位弧度。
    """
    return list(_JOINT_LIMITS)

def flange_offset():
    """
    返回法兰安装面的偏移距离 [m]（在 J7 坐标系前方）。
    """
    return _FLANGE_OFFSET

def load_all():
    """一次取回全部配置：(dh, limits, flange)。

    这就是「函数的多返回值」——return 后面写多个值，
    Python 会自动打包成一个 tuple，调用时用多个变量接住：
        dh, limits, flange = load_all()
    """
    return load_dh(), load_joint_limits(), flange_offset()


# ─────────────────────────────────────────────────────────────
# 查数据
# ─────────────────────────────────────────────────────────────

def count_joints(dh):
    """
    返回关节数（= DH 表有几行）。
    带参数而不是去读内部变量：传什么就数什么，好测也能复用。
    """
    return len(dh)

def joint_names(robot_dh):
    """
    用列表推导式一次取出所有关节名，返回字符串列表。

    「列表推导式」是 for 循环 + append 的压缩写法。
    上面 return 那一行，完全等价于下面这四行：
        names = []
        for joint in robot_dh:
            names.append(joint["name"])
        return names
    """
    return [joint["name"] for joint in robot_dh]

def filter_joints(robot_dh, keep):
    """
    按条件筛选关节；keep 是一个「吃一个 dict、返回 True/False」的函数。

    这就是「函数作为参数传递」：判断标准由调用方决定，本函数不用改。
    例如：
        filter_joints(dh, lambda j: j["d"] > 0)          # 只留 d > 0 的
        filter_joints(dh, lambda j: j["name"] != "J7")   # 去掉 J7
    """
    return [joint for joint in robot_dh if keep(joint)]

# ─────────────────────────────────────────────────────────────
# 打印
# ─────────────────────────────────────────────────────────────

def print_dh_table(robot_dh):
    """遍历 DH 表，打印成对齐的表格。

    alpha 在表里存的是弧度，打印时转成度，方便和官方手册对照。
    """
    print(f"共 {len(robot_dh)} 个关节")
    print("-" * 52)
    # 表头：文本用 < 左对齐，数字用 > 右对齐，后面的数字是「占几格」
    print(f"{'关节':<4}{'a (m)':>10}{'d (m)':>10}{'alpha (deg)':>14}")
    print("-" * 52)

    for joint in robot_dh:                             # 每个 joint 是一个 dict
        print(
            f"{joint['name']:<6}"                      # 名字左对齐，宽 6 格
            f"{joint['a']:>10.4f}"                     # 右对齐，保留 4 位小数
            f"{joint['d']:>10.4f}"
            f"{math.degrees(joint['alpha']):>14.1f}"   # 弧度 → 度，保留 1 位
        )


if __name__ == "__main__":      # 入口守卫：被 import 时不会自动打印
    dh = load_dh()
    print_dh_table(dh)
    print("关节数：", count_joints(dh))
    print("全部关节名：", joint_names(dh))
    print("d > 0 的关节：", [j["name"] for j in filter_joints(dh, lambda j: j["d"] > 0)])

    dh2, limits, flange = load_all()
    print("法兰偏移：", flange, "m；限位条数：", len(limits))
