"""
序列切片小练习
"""

# 定义字符串
my_str = "万过薪月，员序程马黑来，nohtyP学"

# 得到黑马程序员
result = my_str[::-1]
index = result.index("黑")

print(f"结果是：{result}")
print(f"字符串{result}中”黑”的下标是：{index}")
result2 = result[9:14]
print(f"结果是：{result2}")