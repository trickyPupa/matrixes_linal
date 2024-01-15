from itertools import combinations


def minor(matrix, ai, aj):
    rows, cols = len(matrix), len(matrix[0])
    return [[matrix[i][j] for j in range(cols) if j != aj] for i in range(rows) if i != ai]


def determinant(matrix):
    rows, cols = len(matrix), len(matrix[0])

    if rows != cols:
        return None
    else:
        if rows == 1:
            return matrix[0][0]
        if rows == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            return sum((-1) ** j * matrix[0][j] * determinant(minor(matrix, 0, j)) for j in range(cols))


def gauss(a, y):
    n = len(a[0])

    eps = 0.000001
    x = [0] * n
    k = 0
    while k < n:
        # поиск строки с максимальным a[i][k]
        mx = abs(a[k][k])
        index = k
        for i in range(k + 1, n):
            if abs(a[i][k]) > mx:
                mx = abs(a[i][k])
                index = i

        # перестановка строк
        if mx < eps:
            # нет ненулевых диагональных элементов
            print(f"Нет решения, так как есть нулевой столбец {index}")
            return None

        a[k], a[index] = a[index], a[k]
        y[k], y[index] = y[index], y[k]

        # нормализация уравнений
        for i in range(k, n):
            temp = a[i][k]
            if abs(temp) < eps:
                continue
            a[i] = [a[i][j] / temp for j in range(n)]
            y[i] = y[i] / temp
            if i == k:
                continue

            a[i] = [a[i][j] - a[k][j] for j in range(n)]
            y[i] -= y[k]

        k += 1

    # обратная подстановка
    for k in range(n - 1, -1, -1):
        x[k] = y[k]
        y = [y[i] - a[i][k] * x[k] for i in range(k)]

    return x


class Matrix:
    def __init__(self, n: int = 0, m: int = 0, data: list[list[complex]] = None, other=None):
        if other is not None:
            if isinstance(other, Matrix):
                self.matrix = other.matrix.copy()
                self.rows = len(self.matrix)
                self.cols = len(self.matrix[0])
            else:
                raise TypeError("Неподходящие входные данные")
        elif data is not None:
            self.matrix = data.copy()
            self.rows = len(self.matrix)
            self.cols = len(self.matrix[0])
        elif n != 0:
            if not m:
                m = n
            self.matrix = [[0] * m for _ in range(n)]
            self.rows = n
            self.cols = m
        else:
            self.rows = 0
            self.cols = 0
            self.matrix = []

    def __add__(self, other):
        if isinstance(other, Matrix):
            if other.rows == self.rows and other.cols == self.cols:
                result = [[self.matrix[i][j] + other.matrix[i][j] for j in range(self.cols)] for i in range(self.rows)]
                return Matrix(data=result)
            else:
                raise ValueError(f"Сложение матриц разных размеров:\n{self}\t{other}")
        elif isinstance(other, SLAU):
            return other + self
        elif other is None:
            return self
        else:
            raise TypeError(f"Неподходящее слагаемое для матрицы {self}:" + other)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.cols != other.rows:
                raise ValueError(
                    f"Матрицы неподходящих размеров для перемножения:\n{self.__repr__()}\t{other.__repr__()}")
            res = [[sum(self.matrix[i][k] * other.matrix[k][j] for k in range(self.cols)) for j in range(other.cols)]
                   for i in range(self.rows)]

            return Matrix(data=res) if len(res) != 1 else Vector(data=res[0])
        elif isinstance(other, (int, float, complex)):
            return Matrix(data=[[j * other for j in self.matrix[i]] for i in range(self.rows)])
        elif isinstance(other, X):
            return other * self
        elif isinstance(other, SLAU):
            return SLAU(self * other.matrix, other.x)
        else:
            raise TypeError(f"Неподходящий множитель для матрицы {self}:" + other)

    def pretty_str(self):
        ans = ""
        for i in self.matrix:
            ans += '(' + ' '.join(map(str, i)) + ')' + '\n'
        return ans.strip()

    def __str__(self):
        return str(self.matrix)

    def __repr__(self):
        return str(self.matrix)

    def set_data(self, data):
        self.matrix = data.copy()
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])

    def determinant(self):
        return determinant(self.matrix)

    def rang(self):
        k = min(self.rows, self.cols)
        while k > 1:
            c1 = list(combinations(range(self.rows), k))
            c2 = list(combinations(range(self.cols), k))
            for o in range(len(c1)):
                for p in range(len(c2)):
                    mat = [[self.matrix[i][j] for j in c2[p]] for i in c1[o]]
                    if determinant(mat) != 0:
                        return k
            k -= 1
        return k

    def inverse(self):
        pass

    def union(self):
        pass


class Vector(Matrix):
    def __init__(self, n=0, data: list[complex] = None):
        if data is not None:
            super().__init__(data=[data])
        elif n:
            super().__init__(n=1, m=0)
        else:
            super().__init__(data=[[]])


class X:
    def __init__(self):
        super().__init__()

    def __mul__(self, other):
        if isinstance(other, (Matrix, complex, int, float)):
            return SLAU(other, self)
        else:
            raise TypeError("Неподходящий множитель для X:" + other)


class SLAU:
    def __init__(self, matrix, x, free: Matrix = None):
        self.matrix = matrix
        self.x = x
        self.free = free

    def __mul__(self, other):
        if isinstance(other, (int, float, complex, Matrix)):
            return SLAU(self.matrix * other, self.x) if self.free is None \
                else SLAU(self.matrix * other, self.x, self.free * other)
        else:
            raise TypeError("Неподходящий множитель")

    def __add__(self, other):
        if isinstance(other, SLAU):
            return SLAU(self.matrix + other.matrix, self.x, self.free + other.free)
        elif isinstance(other, Matrix):
            return SLAU(self.matrix, self.x, other + self.free)
        else:
            raise TypeError("Неподходящее слагаемое")

    def __str__(self):
        return f"SLAU:Matrix={self.matrix.__repr__()}+{self.free.__repr__()}"

    def __repr__(self):
        return self.__str__()

    def __cramer_mat_i(self, a):
        res = [[self.free.matrix[0][i] if j == a else self.matrix.matrix[i][j] for j in range(self.matrix.cols)]
               for i in range(self.matrix.rows)]
        # print(res)
        return res

    def solve(self, gauss=True):
        if not isinstance(self.free, Vector) and len(self.free.matrix[0]) != 1:
            raise ValueError(f"Неправильная формула:\n\tМатрица = {self.matrix}\n\tСвободный член = {self.free}")
        if len(self.free.matrix[0]) == 1:
            self.free = Vector(data=[self.free.matrix[i][0] for i in range(self.free.rows)])

        RE, R = self.__rang(), self.matrix.rang()
        print(RE, R)

        if RE > R:
            return "Нет решений"
        if RE == R:
            if R != self.matrix.cols:
                return "Бесконечное множество решений"

            if gauss:
                return self.gauss_solve()
            else:
                det = self.matrix.determinant()
                if det == 0:
                    return "абоб"
                dets_i = [determinant(self.__cramer_mat_i(i)) for i in range(self.matrix.cols)]

                print(det)
                print(dets_i)

                return [i / det for i in dets_i]

    def gauss_solve(self):
        a = gauss(self.matrix.matrix, self.free.matrix[0])
        if a is not None:
            return a
        else:
            return "Нет Решений"

    def __rang(self):
        mat = [i[:] for i in self.matrix.matrix]
        for i in range(self.matrix.rows):
            mat[i] += [self.free.matrix[0][i]]
        return Matrix(data=mat).rang()
