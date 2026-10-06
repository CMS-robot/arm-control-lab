"""
取出列表内的偶数，组成新的列表
"""

# 定义一个列表

# 使用while循环列表

def list_while_func():
    num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    num_1 = []
    index = 0
    while index < len(num):
        # index变量取出列表中的元素
        element = num[index]
        if element % 2 == 0:
            num_1.append(element)

        index += 1
    return num_1
print(list_while_func())



# 使用for循环列表

def list_for_func():
    num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    num_1 = []
    for element in num:
        if element % 2 == 0:
            num_1.append(element)

    print(f"通过for循环，从列表：{num}中取出偶数，组成新的列表：{num_1}")
list_for_func()



