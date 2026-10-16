"""
四条规则，就这四条，别多学：

    1. 文件名 test_*.py，测试函数名 test_*()
       —— 名字不对，pytest 直接无视（显示 collected 0 items，不报错）
    2. 函数体里写 `assert 条件`
       —— 条件不成立就 FAILED，成立就 PASSED
    3. 跑：在仓库根执行 `python -m pytest tests/ -v`
    4. 全绿 = 通过；红了会告诉你：哪个文件、哪一行、期望什么、实际什么

这里测的是 notes/prereq01_typing_pytest.py 里的三个函数。

注意 import 的写法：从**仓库根**开始写路径。
`python -m pytest` 会把当前目录（仓库根）放进搜索路径，
所以 `notes.xxx` 和 `src.xxx` 都能直接 import。
"""

import math

from notes.prereq01_typing_pytest import clamp3, deg2rad, first_row


def test_deg2rad_basic():
    # 180 度 = π 弧度。
    # 浮点比较一律写 abs(a - b) < 容差，不用 ==（1e-12 够宽松也够严格）
    assert abs(deg2rad(180.0) - math.pi) < 1e-12


def test_deg2rad_zero_and_right_angle():
    # 0 和 90 这种"能被二进制精确表示"的值，用 == 是安全的，
    # 但为了不给自己挖坑，项目里统一都写成容差比较更省心
    assert deg2rad(0.0) == 0.0
    assert abs(deg2rad(90.0) - math.pi / 2) < 1e-12


def test_clamp3_clips_out_of_range():
    # 5.0 > π 应该被压到 π；-5.0 < -π 应该被抬到 -π；0.0 原样保留
    assert clamp3([0.0, 5.0, -5.0]) == [0.0, math.pi, -math.pi]


def test_clamp3_does_not_mutate_input():
    # 这条测的是「副作用」：夹取必须返回新列表，不能就地改调用方的数据。
    # 这类 bug 手工跑一遍基本看不出来（因为你看的是返回值），只有测试盯得住。
    q = [0.5, 100.0, -100.0]
    out = clamp3(q)
    assert q == [0.5, 100.0, -100.0]          # 原列表没被动过
    assert out == [0.5, math.pi, -math.pi]    # 返回值是对的


def test_first_row_empty_is_none():
    # 判 None 用 `is None`，不用 `== None`。
    # 原因：None 在内存里只有一个，is 比的是"是不是同一个"，最准确。
    assert first_row([]) is None


def test_first_row_returns_first():
    assert first_row([[1.0, 2.0], [3.0, 4.0]]) == [1.0, 2.0]
