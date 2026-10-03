# for循环的99乘法表

for x in range(1,10):
    for y in range(1,10):
        if y <= x:
            print(f"{y} * {x} = {y * x}\t", end="")

    print()