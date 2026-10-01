# 写一个BMI计算器
# 公式：BMI = 体重（千克）÷ 身高（米）²

weight = float(input("请输入您的体重（千克）："))
height = float(input("请输入您的身高（米）："))

bmi = weight / (height ** 2)
print(f"您的BMI值是：{bmi:.2f}")
