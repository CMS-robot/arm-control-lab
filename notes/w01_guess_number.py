# 构建一个随机的数字变量
import random
num = random.randint(1,10)

num_1 = int(input("猜数字："))

if num_1 == num:
    print("恭喜你，第一次就猜对了")
else:
    if num_1 > num:
        print("大了")
    else:
        print("小了")

    num_2 = int(input("给你第二次机会吧："))
    if num_2 == num:
        print("恭喜你，第二次就猜对了")
    else:
        if num_2 > num:
            print("大了")
        else:
            print("小了")

        num_3 = int(input("最后一次机会了："))
        if num_3 == num:
            print("恭喜你第三次猜对了")
        else:
            if num_3 > num:
                print("大了")
            else:
                print("小了")

