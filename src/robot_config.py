"""
arm-control-lab —— 机器人配置

本模块存放机械臂的几何参数（DH 参数表），供后续的运动学、
动力学、仿真模块统一读取。

机型：Franka Emika Panda —— 七自由度（7 个关节）力控协作臂

DH 参数（Modified DH / Craig 约定，长度单位米，角度单位弧度）
    a      连杆长度      沿 X 轴量，两关节轴之间公垂线的长度
    alpha  连杆扭转角    绕 X 轴转，相邻两根关节轴的夹角
    d      连杆偏距      沿 Z 轴量，两条公垂线之间的距离
    theta  关节角        绕 Z 轴转 —— 这是「关节变量」，机械臂运动时它
                        一直在变，所以不写死在表里，算的时候按关节值代入

    单个连杆的变换：A_i = Rx(α_i) · Tx(a_i) · Rz(θ_i) · Tz(d_i)
    ⚠️ 这是 Modified DH 的顺序。Standard DH 是 Rz·Tz·Tx·Rx，两套约定
       不能混用，混了算出来的末端位姿会整体偏 90°。

数据来源
    Franka 官方控制参数文档
    https://frankaemika.github.io/docs/control_parameters.html
    三个独立来源逐项核对一致：
      ① Franka 官方文档
      ② robotics-toolbox-python 的 Panda 模型（Modified DH）
      ③ 《上海工程技术大学学报》Franka Panda D-H 参数表

机型选择说明（2026-10-08 定，此前一度用过 UR5）
    项目规格原写「六轴机械臂」，实际选型为 Panda 七轴。理由：
      ① 具身智能研究界事实标准 —— robosuite 的默认机器人就是 Panda，
         大量 RL / 模仿学习 / Sim2Real 工作都以它为平台；
      ② MuJoCo Menagerie 有官方模型 franka_emika_panda，且自带平行夹爪，
         抓取-放置任务开箱可用（Menagerie 里没有 UR5，只有 UR5e）；
      ③ 七轴冗余臂对 WBC / 零空间控制是额外的话题储备。
    项目相关描述中的「六轴」一律以此为准。
    （备查：日后若改用 UR5e 六轴，替换下表条目即可，代码结构不变。）
"""

import math

PI_2 = math.pi / 2  # 90°，DH 表里反复出现，提出来省得写错

# Franka Emika Panda 的 Modified DH 参数
# 外层列表：按「基座 → 末端」的连接顺序排列，顺序本身就是数据
# 内层字典：每个关节的固定参数，用名字取值，不必记位置
PANDA_DH = [
    {"name": "J1", "a": 0.0, "alpha": 0.0, "d": 0.333},
    {"name": "J2", "a": 0.0, "alpha": -PI_2, "d": 0.0},
    {"name": "J3", "a": 0.0, "alpha": PI_2, "d": 0.316},
    {"name": "J4", "a": 0.0825, "alpha": PI_2, "d": 0.0},
    {"name": "J5", "a": -0.0825, "alpha": -PI_2, "d": 0.384},
    {"name": "J6", "a": 0.0, "alpha": PI_2, "d": 0.0},
    {"name": "J7", "a": 0.088, "alpha": PI_2, "d": 0.107},
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
    print_dh_table(PANDA_DH)
