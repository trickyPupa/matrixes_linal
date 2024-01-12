from collections import OrderedDict
from sys import stdin
from technical import *
from func import eval_


'''def create_exp(source, matrix_valuables, vector_valuables, brackets):
    # exp = [] if brackets else [[]]
    exp = [[]]

    while True:
        i = source.read(1)
        if i == '\n':
            return exp
        if i in " *":
            continue
        if i == "x":
            pass
        elif i == "+":
            exp.append([])
        elif i in "([":
            temp_summand = create_exp(source, matrix_valuables, vector_valuables, brackets + i)
            exp[-1] += temp_summand
        elif i in ")]":
            if brackets[-1] != brackets_dict[i]:
                raise Exception("Ошибка в записи выражения")
            print(exp)
            return exp
        elif i.isupper():
            exp[-1].append(i)
            matrix_valuables[i] = Matrix()
        elif i.islower():
            exp[-1].append(i)
            vector_valuables[i] = Vector()'''


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
            mat.append(list(map(int, it.__next__().split())))

        print(rows, cols, mat)
        assert len(mat) == rows and len(mat[0]) == cols
        valuables[k].set_data(mat)
    for k in queue[1]:
        n = int(it.__next__())
        vec = [list(map(int, it.__next__().split()))]
        valuables[k].set_data(vec)

        print(n, vec)
        assert len(vec[0]) == n

    # print(expression)
    # print(valuables)


'''    ans = ""
    matrix_valuables = OrderedDict()
    vector_valuables = OrderedDict()
    expression = create_exp(f, matrix_valuables, vector_valuables, '')

    print(matrix_valuables)
    print(vector_valuables)
    print(expression)

    # for i in f.readline().replace(" ", "").strip():
    #     if i == "x":
    #         pass
    #     elif i == "+":
    #         expression.append([])
    #         cur_address[-1] += 1
    #     elif i in "([<":
    #         expression[-1].append([])
    #     elif i == ")]>":
    #         del cur_address[-1]
    #     elif i.isupper():
    #         expression[-1].append(i)
    #         matrix_valuables[i] = Matrix()
    #     elif i.islower():
    #         expression[-1].append(i)
    #         vector_valuables[i] = Vector()

    # while True:
    #     i = f.read(1)
    #     if i == '\n':
    #         break
    #
    #     if i in " *":
    #         continue
    #     if i == "x":
    #         pass
    #     elif i == "+":
    #         expression.append([])
    #     elif i in "([<":
    #         temp_summand = create_summand(f)
    #         expression[-1].append(temp_summand)
    #     # elif i == ")]>":
    #     #     del cur_address[-1]
    #     elif i.isupper():
    #         expression[-1].append(i)
    #         matrix_valuables[i] = Matrix()
    #     elif i.islower():
    #         expression[-1].append(i)
    #         vector_valuables[i] = Vector()

    for i in matrix_valuables.keys():
        rows_n_cols = list(map(int, f.readline().split()))
        rows = rows_n_cols[0]
        if len(rows_n_cols) == 1:
            cols = rows
        else:
            cols = rows_n_cols[1]

        mat = []
        for _ in range(rows):
            mat.append(list(map(int, f.readline().split())))
        assert len(mat) == rows and len(mat[0]) == cols
        matrix_valuables[i].set_data(mat)

    for i in vector_valuables.keys():
        n = int(f.readline())
        vec = [list(map(int, f.readline().split()))]
        vector_valuables[i].set_data(vec)
        assert len(vec[0]) == n

    pass

    print(matrix_valuables)
    print(vector_valuables)

    print(ans)'''


if __name__ == "__main__":
    a = input("Ввод из файла или из консоли? Введите 1, если из файла, что угодно - если из консоли.\n")
    filename = ''
    if a.strip() == '1':
        filename = input("Введите имя файла:\n")
        file = True
    else:
        file = False
    solution(filename, file)
