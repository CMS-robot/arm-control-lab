"""
三个函数各演示一种常见写法：

    1. deg2rad   —— 标量进、标量出               float -> float
    2. clamp3    —— 列表进、列表出               list[float] -> list[float]
    3. first_row —— 可能没有结果，返回 None      ... -> list[float] | None

语法对照（三种都写在这里了，后面照抄）：

    x: float           参数注解，写在参数名后面，冒号
    ) -> float:        返回值注解，写在括号后面，箭头
    list[float]        列表里装 float（小写 list，Python 3.9 起可这么写）
    list[float] | None 「要么是 list[float]，要么是 None」，竖线表示"或者"
"""

import math


def deg2rad(deg: float) -> float:
    """角度转弧度。

    机器人里所有关节角、旋转角一律用弧度 —— 这是项目的一个硬约定，
    因为 math / numpy 的三角函数吃的都是弧度。写代码时凡是看到"角度"，
    先想清楚它到底是度还是弧度，这是新手最容易混的一处。

    参数
        deg : float，角度（单位：度）

    返回
        float，对应的弧度值
    """
    return math.radians(deg)


def clamp3(q: list[float]) -> list[float]:
    """把每个关节角夹到 [-pi, pi] 之内，超出的拉到边界上。

    为什么叫 clamp3：clamp = 夹紧 / 限幅。这是控制里最常见的操作之一 ——
    你算出来的关节角可能超出物理限位，比如算出 5.0 rad，但电机最多转 π，
    那就得把它压回 π，而不是硬发下去（会撞限位）。

    参数
        q : list[float]，若干个关节角（单位：rad）

    返回
        list[float]，**新列表**，长度与输入相同，每个元素都在 [-pi, pi] 里。
        注意：原列表 q 不会被修改（这条有测试专门盯着）。

    异常
        不抛异常。这里刻意不做类型校验 —— 传进来非数字，Python 会在
        比较那一行自己报 TypeError，不需要我们手动挡。
    """
    lo, hi = -math.pi, math.pi
    out: list[float] = []
    for v in q:
        if v < lo:
            out.append(lo)
        elif v > hi:
            out.append(hi)
        else:
            out.append(v)
    return out


def first_row(rows: list[list[float]]) -> list[float] | None:
    """取二维数据的第 0 行；数据为空时返回 None。

    这是 `| None` 的典型场景：函数**有可能拿不到结果**。
    对比一下你在 io_utils.load_trajectory 里的做法 —— 那里是"文件不存在
    就返回空列表 []"。两种都行，但语义不同：

        · 返回 []      → "读到了，只是内容是空的"（代码能继续算）
        · 返回 None    → "根本没有，你最好先判一下"（逼调用方处理）

    选哪种没有标准答案，但**同一个项目里要一致**，否则调用方永远猜不到
    该判 `if x == []` 还是 `if x is None`。

    参数
        rows : list[list[float]]，形如 [[q1, q2, ...], [...], ...]

    返回
        list[float]，第一行；输入为空时返回 None
    """
    if not rows:
        return None
    return rows[0]


if __name__ == "__main__":
    # 自己跑一遍看效果：python notes/prereq01_typing_pytest.py
    print("deg2rad(180) =", deg2rad(180.0))
    print("clamp3([0, 5, -5]) =", clamp3([0.0, 5.0, -5.0]))
    print("first_row([]) =", first_row([]))
    print("first_row([[1, 2]]) =", first_row([[1.0, 2.0]]))

    # 演示「注解是文档不是检查器」：传错类型，Python 不会拦你
    print()
    print("--- 注解不检查，只记录 ---")
    print("deg2rad 的注解是：", deg2rad.__annotations__)
    print("传个字符串进去 →", end=" ")
    try:
        print(deg2rad("一百八十度"))
    except TypeError as e:
        print("还是炸了，但炸在 math.radians 里，不是注解拦下的：", e)
