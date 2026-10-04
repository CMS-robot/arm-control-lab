"""
黑马ATM
"""

# 全局变量，记录银行卡余额
money = 5000000
# 记录客户姓名
name = input("您的名字是：")

# 查询余额函数
def find(show_header):
    if show_header :
        print("---查询余额---")
    print(f"{name}，您好，您的余额剩余：{money}")


# 存款函数
def save(num):
    global money
    money += num
    print("---存款---")
    print(f"{name}，您好，您存款{num}元成功")
    find(False)


# 取款余额
def take(num):
    global money
    money -= num
    print("---取款---")
    print(f"{name}，您好，您取款{num}元成功")
    find(False)


# 主菜单函数
def menu():
    print("---主菜单---")
    print(f"{name}，您好，欢迎来到黑马银行ATM，请选择操作：")
    print("查询余额\t【输入1】")

    print("存款\t\t【输入2】")

    print("取款\t\t【输入3】")

    print("退出\t\t【输入4】")

    return input("请输入您的选择：")

while True:
    keyboard_input = menu()
    if keyboard_input == "1":
        find(True)
        continue
    elif keyboard_input == "2":
        num = int(input("你想要存多少钱："))
        save(num)
        continue
    elif keyboard_input == "3":
        num = int(input("你想要取多少钱"))
        take(num)
        continue
    else:
        print("程序退出")
        break

