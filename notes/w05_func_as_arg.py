"""
演示lambda匿名函数
"""

# # 定义一个函数，接收另一个函数作为传入参数
def test_func(computer):
    result = computer(1, 2)  #确定computer是函数
    print(f"computer参数的类型是：{type(computer)}")
    print(f"计算结果是：{result}")

# 通过lambda匿名函数的形式，将匿名函数作为参数传入
test_func(lambda a, b: a + b)