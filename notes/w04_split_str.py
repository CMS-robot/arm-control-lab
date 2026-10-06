"""
分割字符串小练习
"""

# 给定一个字符串
my_str = "itheima itcast boxuegu"

# 统计字符串内有多少个“it”字符
count = my_str.count("it")
print(f"字符串{my_str}中有：{count}个it字符")

# 将字符串内的空格，全部替换成字符："|"
new_str = my_str.replace(" ", "|")
print(f"字符串{my_str}，被替换空格后，结果：{new_str}")

# 并按照“|”进行字符串分割，得到列表
new_list = new_str.split("|")
print(f"字符串{new_str}，按照|分割后，得到：{new_list}")