"""
小练习：元组的基本操作
"""

# 定义一个元组
word = ("周杰伦", 11, ["football", "music"])

# 查询其年龄所在的下标位置
index = word.index(11)
print(f"其年龄所在下标位置：{index}")

# 查询学生的姓名
name = word[0]
print(f"学生的姓名是：{name}")

# 删除学生爱好中的football
del word[2][0]
print(f"删除后元组：{word}")

# 增加爱好：coding到爱好list内
word[2].append("coding")
print(f"增加后的元组：{word}")