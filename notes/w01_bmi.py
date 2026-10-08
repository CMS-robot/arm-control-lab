"""
BMI 计算器小练习 —— 输入体重身高，计算 BMI 并按区间给出评判。

公式：BMI = 体重(kg) / 身高(m) ** 2
分界（WHO）：<18.5 偏瘦 | 18.5—25 正常 | 25—30 超重 | >=30 肥胖
"""

weight = float(input("请输入您的体重(kg)："))
height = float(input("请输入您的身高(m)："))

bmi = weight / (height ** 2)

print(f"您的BMI数值是：{bmi:.2f}")

if bmi < 18.5:
    print("偏瘦")
elif 18.5 <= bmi < 25:
    print("正常")
elif 25 <= bmi < 30:
    print("超重")
else:
    print("肥胖")
