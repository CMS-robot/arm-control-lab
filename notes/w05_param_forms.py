"""
演示多种传参的形式
"""

def user_info(name, age, gender):
    print(f"姓名是：{name}， 年龄是：{age}， 性别是：{gender}")

# 位置参数 - 默认使用形式
user_info("小明", 20, "male")

# 关键字参数 （可以乱序，也可以与位置参数混用）
user_info(name = "小王", age = 20, gender = "male")

# 缺省参数（默认值）
def user_info(name, age, gender = "男"):
    print(f"姓名是：{name}， 年龄是：{age}， 性别是：{gender}")

user_info("小天",30)
user_info("小天",30, gender = "女")


# 不定长 - 位置不定长， *号
# 不定长定义的形式参数会作为元组存在，接收不定长数量的参数传入
def user_info(*args):
    print(f"args参数的类型是：{type(args)}，内容是：{args}")
user_info(2, 3, "xiaoming")

# 不定长 - 关键字不定长， **号
def user_info(**kwargs):
    print(f"args参数的类型是：{type(kwargs)}，内容是：{kwargs}")

user_info(name = "小明", age = 20, gender = "male")