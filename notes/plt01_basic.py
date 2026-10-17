# 导包
import random
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# ---------- 中文字体两行（必须在 import pyplot 之后、任何 plot 之前）----------
# 不写这两行的后果：
#   1) 中文全是方框，控制台刷一堆 "Glyph 27491 missing from font(s) DejaVu Sans"
#      因为 matplotlib 默认字体 DejaVu Sans 里根本没有汉字
#   2) 第 1 行：font.sans-serif 是「候选列表」，前面的找不到会自动退到后面，
#      所以写 ['SimHei', 'Microsoft YaHei'] 比只写一个稳（有的机器没装黑体）
#   3) 第 2 行：SimHei 里【没有】Unicode 减号 U+2212，而 matplotlib 默认就用它
#      画负数刻度 —— 结果中文正常了、负号还是方块。设 False 改用 ASCII 的 "-"。
#
# ⚠️ 注意这两个 "-" 不是同一个字符：
#      U+002D  -  ASCII 短横（unicode_minus=False 时用，SimHei 里有）
#      U+2212  −  数学减号（unicode_minus=True 默认，SimHei 里没有 -> 方块）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']    # 指定黑体（Windows 自带）
plt.rcParams['axes.unicode_minus'] = False      # 修负号的方框


"""
绘制Matplotlib入门案例_绘制北京近一周气温折线图
"""

# # 回顾可视化的3个步骤：1，创建画布；2，准备数据（x轴，y轴）；3，具体的绘图
# # 1，创建画布
# # 参数1：figsize（画布大小（宽，高））；参数2：dpi（像素密度，就是清晰度）
# plt.figure(figsize=(10,5), dpi=100)
#
# # 2，准备数据（x轴，y轴）
# # 参数1：x轴数据；参数2：y轴数据
# plt.plot([1, 2, 3, 4, 5, 6, 7],[15, 11, 6, 28, 22, 20,15])
#
# # 3. 具体的绘图
# plt.show()

"""
绘制标准折线图
"""

# 绘制北京某天1个小时内的气温折线图

# 1. 准备数据并绘制初始折线图

# 1.1 准备x轴（60分钟）和y轴（每分钟的温度）的数据
x = range(60)
y_beijing = [random.uniform(15, 18) for i in x]

# 2. 创建画布
plt.figure(figsize = (10, 5), dpi = 100)  # color 表示折线的颜色

# 3. 开始绘图
# label 是「这个图例叫什么」，legend() 靠它取名字。
# ⚠️ 标签必须挂在 plot 上，不能直接写进 legend("温度") —— legend 的第一个
#    位置参数是句柄列表(handles)，传字符串进去会静默取首字符，只显示「温」。
plt.plot(x, y_beijing, color = "red", label = "温度")

# 4. 添加x轴和y轴刻度信息
# 4.1 准备x轴刻度信息
x_ticks_label = [f"11点{i}分" for i in x]
# y 轴刻度故意从 -10 起：D10 的验收是「负号不是方块」，
# 原来的 range(40) 是 0~39 全正数，负号那行等于没被验证过。
# range(-10, 40, 5) -> -10, -5, 0, 5, 10, ... 35
y_ticks = range(-10, 40, 5)

# 4.2 具体的添加x轴和y轴刻度信息的动作
plt.xticks(x[::5], x_ticks_label[::5])       # 参数1：x轴刻度值     参数2：x轴刻度值对应的标签
plt.yticks(y_ticks)        # 参数1：y轴刻度值（已经是 5 的倍数，不用再切）

# 5 添加网格
# 参数1. 网格线的样式 -  --  -.  :
# 参数2. 网格线的透明度
plt.grid(linestyle = "--", alpha = 0.5)

# 6 添加标题
plt.title("北京某天1小时内的气温折线图", fontsize = 20)

# 7 添加x轴，y轴标签
plt.xlabel("时间", fontsize = 10)
plt.ylabel("温度", fontsize = 10)

# 7.5 图例（Tell you 哪条线是什么）
# loc 可写 'upper left' / 'upper right' / 'lower left' / 'best'（默认，自动找空位）
# 顺序不能反：先 plot(label=...) 再 legend()。只调 legend() 而 plot 没给 label
# 会抛 UserWarning: No artists with labels found to put in legend，图例是空的。
plt.legend(loc = "upper left", fontsize = 10)  # 图例

# 7.6 坐标轴显示范围
# xlim / ylim = 左右端、上下端。这里给 y 设 -10~40 是为了让负刻度露出来。
plt.xlim(0, 60)
plt.ylim(-10, 40)

# 8 保存图片
# 用 __file__ 定位而不是 "./my_picture.png"：
#   相对路径以「当前工作目录」为基准，PyCharm 里跑脚本时 cwd 可能是项目根、
#   也可能是脚本所在目录，同一个 "./xxx.png" 会存到不同地方，很坑。
#   Path(__file__).resolve() -> 本文件绝对路径
#   .parents[0] = notes/，.parents[1] = 仓库根 D:/arm-control-lab
# results/* 已在 .gitignore 里排除，图是产物、不入库，能一条命令重新生成。
out = Path(__file__).resolve().parents[1] / "results" / "plt01_basic.png"
out.parent.mkdir(parents = True, exist_ok = True)
plt.savefig(out, dpi = 100)
print(f"图已保存：{out}")

# 9. 具体绘图动作
# 本文件故意不写 matplotlib.use("Agg")：加了它 plt.show() 就不弹窗了
# （warning: FigureCanvasAgg is non-interactive, and thus cannot be shown）。
# 需要「只出图不弹窗」（服务器 / 批量生成）时，用环境变量 MPLBACKEND=Agg，
# 别改代码 —— 这样 PyCharm 里能看图、服务器上能批量跑，同一份代码。
plt.show()
