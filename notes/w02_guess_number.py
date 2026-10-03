# 猜数字小案例

import random
num = random.randint(1,100)
# 定义一个变量，记录总共猜测了多少次
count = 0

# 通过一个布尔类型的变量，做循环是否继续的标记
flag = True
while flag:
    guess_num = int(input("请输入你猜测的数字："))
    count += 1
    if guess_num == num:
        print("猜对了")
        # 设置false就是终止循环的条件
        flag = False
    else:
        if guess_num > num:
            print("大了")
        else:
            print("小了")
print(f"你总共猜了：{count}次")