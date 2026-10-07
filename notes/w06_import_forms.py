"""
演示python的模块导入
"""

# 使用import导入时间time模块使用sleep功能（函数）  # （import）是吧整个模块调用
# import time    # 导入python内置的time模块（time.py这个代码文件）
# print("你好")
# time.sleep(5)
# print("我好")

# 使用from导入time的sleep功能（函数）   #from是单独调用模块内的某个功能，单独只使用这个功能
# from time import sleep
# print("你好")
# sleep(5)
# print("我好")

# 使用* 导入time模块的全部功能
# from time import *  # *表示全部的意思
# print("你好")
# sleep(5)
# print("我好")

# 使用as给特定功能加上别名
# import time as t
# print("你好")
# t.sleep(5)
# print("我好")

from time import sleep as sl
print("你好")
sl(5)
print("我好")