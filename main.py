from collections import OrderedDict
from sys import stdin
from technical import *

brackets_dict = {')': '(', ']': '['}


def create_exp(source, matrix_valuables, vector_valuables, brackets):
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
            vector_valuables[i] = Vector()


def solution(filename):
    if filename:
        f = open(filename)
    else:
        f = stdin

    ans = ""
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

    print(ans)


if __name__ == "__main__":
    filename = input()
    solution(filename)
