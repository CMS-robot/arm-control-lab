"""
arm-control-lab —— 机器人配置

本模块存放机械臂的几何参数（DH 参数表）与关节限位，供后续的
运动学、动力学、仿真模块统一读取。

机型：Franka Research 3（FR3）—— 七自由度（7 个关节）力控协作臂
      Franka 现役在售型号，前身是 Franka Emika Panda（2017—2022，已停产）。
      FR3 完整继承 Panda 的运动学链，两者 DH 参数逐项相同；差异在关节
      限位、关节速度、防护等级与固件/驱动（Panda 已停止更新）。

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
    ① Franka 官方文档（现役地址）
       https://frankarobotics.github.io/docs/robot_specifications.html
       → Kinematic Configuration → Denavit–Hartenberg Parameters
       原文：The Denavit–Hartenberg parameters for the Franka Research 3
             kinematic chain (following Craig's convention)
       （注：老地址 frankaemika.github.io 已整站下线，2026-10-08 实测 404）
    ② MuJoCo Menagerie 官方仿真模型 franka_fr3/fr3.xml（Apache-2.0）
       —— 关节限位取自这里，与 ① 交叉核对一致
    ③ robotics-toolbox-python 的 Panda 模型（用于确认运动学链未变）
    离线存档：D:/WorkBuddy/参考实现/Franka官方DH参数表-离线存档.html

    ⚠️ 官方表最后一行不是关节：Flange 是「法兰安装面」，位于 J7 坐标系
       前方 0.107 m。官方表把它单列，所以 J7 的 d 是 0。旧版 Panda 文档
       把 0.107 并进了 J7 那一行 —— 两种口径都能用，但改用 FR3 后按
       FR3 官方口径：J7 d = 0，法兰偏移单独记在 FLANGE_OFFSET。

机型选择说明（2026-10-08 定，全项目以此为准）
    选 Franka Research 3 的理由：
      ① 现役在售 —— Panda 已于 2022 年停产；FR3 是当前唯一在售的
         Franka 七轴研究平台（版本已迭代到 FR3 V2，2025-09 起）；
      ② 具身智能研究界的主流平台 —— 官方列出的规模化应用单位含
         Google DeepMind、TUM AI Factory、清华 RDT、银河通用、
         智元创新等；robosuite 等框架的默认机器人属这一支；
      ③ 七轴冗余（6 + 1）—— 主攻方向 WBC 的核心（零空间投影、任务
         优先级、自运动）只有在冗余臂上才有施展空间；六轴臂冗余度为零；
      ④ MuJoCo Menagerie 有官方模型 franka_fr3 且维护活跃
         （2025-09 新增 franka_fr3_v2）；franka_emika_panda 停在 2024-11；
      ⑤ 可退化：锁住 J7 就退化成六轴臂，反过来做不到。

    代价（提前记下）：七轴没有一般闭式逆解，逆解须用数值法（阻尼最小二乘 / QP）。

    历史（备查）：2026-10-08 曾比较 Panda / UR5 / FR3。git 历史
      4c8dc65 = UR5 六轴版，54e982d = Panda 版。最终定为 FR3 —— 与 Panda
      运动学一致，但型号是现役的。日后若改用 UR5e（六轴），替换下表条目
      即可，代码结构不变。
"""

import math

PI_2 = math.pi / 2  # 90°，DH 表里反复出现，提出来省得写错

# Franka Research 3 的 Modified DH 参数
# 外层列表：按「基座 → 末端」的连接顺序排列，顺序本身就是数据
# 内层字典：每个关节的固定参数，用名字取值，不必记位置
FR3_DH = [
    {"name": "J1", "a": 0.0, "alpha": 0.0, "d": 0.333},
    {"name": "J2", "a": 0.0, "alpha": -PI_2, "d": 0.0},
    {"name": "J3", "a": 0.0, "alpha": PI_2, "d": 0.316},
    {"name": "J4", "a": 0.0825, "alpha": PI_2, "d": 0.0},
    {"name": "J5", "a": -0.0825, "alpha": -PI_2, "d": 0.384},
    {"name": "J6", "a": 0.0, "alpha": PI_2, "d": 0.0},
    {"name": "J7", "a": 0.088, "alpha": PI_2, "d": 0.0},
]

# 法兰安装面：在 J7 坐标系前方 0.107 m（官方表里单列的 Flange 行）
FLANGE_OFFSET = 0.107

# 关节限位（弧度），取自官方 URDF / Menagerie fr3.xml，与厂家资料一致。
# 后面做逆解选解、轨迹规划、仿真建模都要用；写在配置里，避免各处硬编码。
JOINT_LIMITS = [
    (-2.9007, 2.9007),   # J1  ±166.2°
    (-1.8361, 1.8361),   # J2  ±105.2°
    (-2.9007, 2.9007),   # J3  ±166.2°
    (-3.0770, -0.1169),  # J4  -176.3° ~ -6.7°（注意：区间不包含 0）
    (-2.8763, 2.8763),   # J5  ±164.8°
    (0.4398, 4.6216),    # J6  +25.2° ~ +264.8°（注意：区间不包含 0）
    (-3.0508, 3.0508),   # J7  ±174.8°
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
    print_dh_table(FR3_DH)
