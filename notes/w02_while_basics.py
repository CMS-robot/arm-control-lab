"""
演示while循环的基础应用
"""

# i = 0
# while i < 10:
#     print("小妹，我喜欢你哦")
#     i += 1

# num = 1
# sum = 0
# while num <= 100:
#     sum += num
#     num += 1
#
# print(f"从1-100累加的和是：{sum}")

num = 1
total = 0
expr =""
while num <= 100:
    total += num
    expr += str(num)
    if num<100:
        expr += "+"
    num += 1
print(f"{expr} = {total}")