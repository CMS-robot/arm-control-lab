"""
文件处理相关工具
"""

# 接收传入文件的路径，打印文件的全部内容，如文件不存在则捕获异常，输出提示信息，通过finally关闭文件对象
# 第一种，with
# def print_file_info(file_name):
#     try:
#         with open(file_name, "r", encoding="utf-8") as f:
#             print(f.read())
#     except Exception as e:
#         print(f"文件不存在，程序出现异常：{e}")

# 第二种，finally
def print_file_info(file_name):
    f = None                                     # ① 先占位
    try:
        f = open(file_name, "r", encoding="utf-8")
        content = f.read()                       # ② 一次读完全部内容
        print("文件的全部内容如下：")
        print(content)
    except Exception as e:
        print(f"文件不存在，程序出现异常：{e}")
    finally:
        if f:                                    # ③ 关键守卫
            f.close()


# 接收文件路径以及传入数据，将数据追加写入文件中
def append_to_file(file_name, data):
    f = open(file_name, "a", encoding="utf-8")
    f.write(data)
    f.write("\n")      # 追加一个换行，否则下次写入会和这一行粘在一起
    f.close()


