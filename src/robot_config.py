"""
arm-control-lab —— 机器人配置

本模块存放机械臂的几何参数（DH 参数表），供后续的运动学、
动力学、仿真模块统一读取。

DH 参数（Standard DH / Paul 形式，长度单位米，角度单位弧度）
    单个连杆的变换：A_i = Rz(θ_i) · Tz(d_i) · Tx(a_i) · Rx(α_i)

    a      连杆长度      沿 X 轴量
    alpha  连杆扭转角    绕 X 轴转
    d      连杆偏距      沿 Z 轴量
    theta  关节角        绕 Z 轴转 —— 这是「关节变量」，机械臂运动时它一直在
                        变，所以不写死在表里，算的时候按关节值代入

⚠️ DH 有两套约定，符号和顺序都不一样，绝对不可混用
    Standard DH（本文件所用）  美国标准，UR / ABB 手册常用
    Modified DH (Craig)        先转 alpha 再转 theta，Franka / 部分教材使用
    两者的中间坐标系不同，但末端位姿结果一致。

数据来源
    Universal Robots 官方手册 B.2 Robot DH Parameter（UR5 serie 3）
    已与机器人学公开资料交叉核对，三处数值一致
"""

import math

PI_2 = math.pi / 2  # 90°，DH 表里反复出现，提出来省得写错

# Universal Robots UR5 的 Standard DH 参数（六轴）
# 外层列表：按「基座 → 末端」的连接顺序排列，顺序本身就是数据
# 内层字典：每个关节的固定参数，用名字取值，不必记位置
UR5_DH = [
    {"name": "J1", "a": 0.0, "alpha": PI_2, "d": 0.089159},
    {"name": "J2", "a": -0.425, "alpha": 0.0, "d": 0.0},
    {"name": "J3", "a": -0.39225, "alpha": 0.0, "d": 0.0},
    {"name": "J4", "a": 0.0, "alpha": PI_2, "d": 0.10915},
    {"name": "J5", "a": 0.0, "alpha": -PI_2, "d": 0.09465},
    {"name": "J6", "a": 0.0, "alpha": 0.0, "d": 0.0823},
]


def print_dh_table(robot_dh):
    """遍历打印 DH 参数表。

    alpha 在表里存的是弧度，打印时转成角度，方便和手册对照。
    """
    print(f"共 {len(robot_dh)} 个关节")
    print("-" * 52)
    print(f"{'关节':<6}{'a (m)':>10}{'alpha (deg)':>14}{'d (m)':>10}")
    print("-" * 52)
    for joint in robot_dh:
        print(
            f"{joint['name']:<6}"
            f"{joint['a']:>10.4f}"
            f"{math.degrees(joint['alpha']):>14.1f}"
            f"{joint['d']:>10.4f}"
        )


if __name__ == "__main__":
    print_dh_table(UR5_DH)
