# 小练习

import random

# 账户余额
money = 10000

# 员工有20人
for i in range(1,21):
    # 随机绩效
    num = random.randint(1, 10)
    # 判断绩效是否达标
    if num < 5:
        print(f"员工{i}，绩效分{num}，低于5，不发工资，下一位")
        continue
    # 判断余额是否充足
    if money >= 1000:
        money -= 1000
        print(f"向员工{i}发放工资1000元，账户余额还剩余{money}元")
    else:
        print("余额不够了，下个月再来")
        break


