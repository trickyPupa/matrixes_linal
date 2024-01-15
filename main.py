from sys import stdin
from technical import *
from func import eval_


def solution(filename="", file=False):
    if file:
        with open(filename) as f:
            data = f.readlines()
    else:
        data = stdin.readlines()

    expression = ""
    valuables = {}
    queue = ["", ""]

    # считывание выражения
    a = data[0].strip()
    for i in range(len(a) - 1):
        if a[i].isalpha():
            expression += a[i]
            if a[i + 1].isalpha() or a[i + 1] == "(":
                expression += '*'

            if a[i].isupper() and a[i] not in queue[0]:
                queue[0] += a[i]
                valuables[a[i]] = Matrix()
            elif a[i] != 'x' and a[i].islower() and a[i] not in queue[1]:
                queue[1] += a[i]
                valuables[a[i]] = valuables.get(a[i], Vector())
        elif a[i] in "()+*":
            expression += a[i]
    expression += a[-1]
    if a[-1].isupper() and a[-1] not in queue[0]:
        queue[0] += a[-1]
        valuables[a[-1]] = Matrix()
    elif a[-1] != 'x' and a[-1].islower() and a[-1] not in queue[1]:
        queue[1] += a[-1]
        valuables[a[-1]] = valuables.get(a[-1], Vector())

    # запись значений матриц и векторов
    it = iter(data[1:])
    for k in queue[0]:
        rows_n_cols = list(map(int, it.__next__().split()))
        rows = rows_n_cols[0]
        if len(rows_n_cols) == 1:
            cols = rows
        else:
            cols = rows_n_cols[1]

        mat = []
        for _ in range(rows):
            mat.append(list(map(complex, it.__next__().replace('i', 'j').split())))
        assert len(mat) == rows and len(mat[0]) == cols
        valuables[k].set_data(mat)
    for k in queue[1]:
        n = int(it.__next__())
        vec = [list(map(complex, it.__next__().replace('i', 'j').split()))]
        valuables[k].set_data(vec)
        assert len(vec[0]) == n

    # print(queue)
    print(expression)
    print(valuables)

    res = eval_(expression, valuables)
    print(res)
    ans = res.solve()
    if type(ans) == str:
        print(ans)
    else:
        for i in range(len(ans)):
            print(f"x{i + 1} = {ans[i]}")


if __name__ == "__main__":
    a = input("Ввод из файла или из консоли? Введите 1, если из файла, что угодно - если из консоли.\n")
    filename = ''
    if a.strip() == '1':
        filename = input("Введите имя файла:\n")
        file = True
    else:
        file = False
    solution(filename, file)
