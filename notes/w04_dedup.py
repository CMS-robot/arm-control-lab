"""
信息去重小练习
"""

# 定义对象
my_list = ["黑马程序员", "传智播客", "黑马程序员", "传智播客", "itheima", "itcast", "itheima", "itcast", "best"]

# 定义一个空集合
my_set = set()

# for循环遍历
for element in my_list:
    print(f"有列表:{element}")
    my_set.add(element)
print(f"存入集合后结果：{my_set}")
