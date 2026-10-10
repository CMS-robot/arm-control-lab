"""io_utils.py —— 轨迹文件的读写工具。

文件约定（整个项目统一，写进 README 时照抄这一段）：

    · csv 文本，逗号分隔，utf-8 编码
    · 第一行是表头，固定写 q1, q2, ..., qn
    · 从第二行起，每个时刻一行，一行 = 该时刻全部 n 个关节角（单位 rad）
    · 数值统一格式化 8 位小数，方便人眼比对、也方便 diff

数据在内存里的表示：

    list[list[float]]，形状 (N, n)
        N = 采样点数（时刻数）
        n = 关节数（FR3 是 7）

为什么用 csv 模块而不是手写 split(",")：

    split(",") 在字段里出现引号、逗号、换行时会切错，且没有转义机制。
    csv.reader / csv.writer 会按 RFC 4180 正确转义，代价为零。
    你之前手写的那版能用，是因为轨迹文件里全是数字、绝对不会有特殊字符；
    换成别的地方（比如日志里的备注列）就会翻车。

注意：本版仍是纯 list 实现。
      按任务表的安排，D9 学完 NumPy 后会整体 NumPy 化（返回 np.ndarray），
      届时 load_trajectory 的签名会变成返回 ndarray，本文件是那一版的地基。
"""

import csv


def load_trajectory(path):
    """读 csv 轨迹文件 -> list[list[float]]，形状 (N, n)。

    参数
        path : str / Path，csv 文件路径

    返回
        list[list[float]]，N 行、每行 n 个 float

    约定
        第一行一律当表头丢掉（不校验内容）。
        空行（含只有逗号的行）会被跳过，不会让 float("") 抛 ValueError。

    异常
        ValueError : 某个字段不是合法数字
        FileNotFoundError 不抛：路径不存在时打印一句提示并返回空列表 []（D4）
    """
    data = []
    try:
        # newline="" 是 csv 模块的要求：交给 csv 自己处理换行符
        with open(path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # 丢掉表头；给默认值 None，空文件也不会抛 StopIteration

            for row in reader:
                # row 是「一个字符串列表」，空行会得到 [] 或 [''] 或 ['', '']
                if not row or all(cell.strip() == "" for cell in row):
                    continue
                data.append([float(cell) for cell in row])
    except FileNotFoundError:
        # 只捕这一种异常：把函数名敲错、float() 遇到坏数据，照样正常上抛，不会被吞掉
        print(f"轨迹文件不存在：{path}")
        return []

    return data


def save_trajectory(path, rows, header=None):
    """把二维轨迹写成 csv 文件。返回实际写出的数据行数（不含表头）。

    参数
        path   : str / Path，输出文件路径（已存在会被覆盖）
        rows   : 二维数据，list[list]，可传 list[tuple] / 生成器；元素须能转 float
        header : 表头列表；不传则自动生成 ["q1", "q2", ..., "qn"]

    返回
        int，写出的数据行数

    异常
        ValueError : rows 为空、某行列数不一致、或 header 长度与列数不符
    """
    # 先落地成 list[list[float]]：既统一了类型，也顺手挡掉「传进来的行是元组/字符串」
    rows = [[float(v) for v in r] for r in rows]

    if not rows:
        raise ValueError("save_trajectory: rows 为空，没有东西可以写")

    n_cols = len(rows[0])
    for i, r in enumerate(rows):
        if len(r) != n_cols:
            # 列数不齐会让下游的 ndarray 构造直接崩，且报错点离现场很远，所以在这里拦掉
            raise ValueError(
                f"save_trajectory: 第 {i} 行有 {len(r)} 列，第 0 行有 {n_cols} 列，不一致"
            )

    if header is None:
        header = [f"q{i + 1}" for i in range(n_cols)]
    if len(header) != n_cols:
        raise ValueError(
            f"save_trajectory: header 有 {len(header)} 项，数据有 {n_cols} 列，不一致"
        )

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for r in rows:
            # 固定 8 位小数：不写 f"{v:.8f}" 的话 csv 会用 repr，
            # 0.1 就写成 "0.1"，人眼比对两批轨迹时位数对不齐
            writer.writerow([f"{v:.8f}" for v in r])

    return len(rows)


if __name__ == "__main__":
    # 入口守卫：自己测一下，别把临时数据写得到处都是
    import os
    import tempfile

    demo = [[t * 0.01 + j * 0.1 for j in range(7)] for t in range(50)]
    tmp_path = os.path.join(tempfile.gettempdir(), "_io_utils_selftest.csv")

    n = save_trajectory(tmp_path, demo)
    back = load_trajectory(tmp_path)

    print(f"写出 {n} 行 -> 读回 {len(back)} 行 x {len(back[0])} 列")
    print("首行：", back[0])
    print("末行：", back[-1])

    bad = [
        (t, j)
        for t, row in enumerate(back)
        for j, v in enumerate(row)
        if abs(v - (t * 0.01 + j * 0.1)) > 1e-9
    ]
    print("超容差 1e-9 的个数：", len(bad))

    os.remove(tmp_path)
    print("自检结束")
