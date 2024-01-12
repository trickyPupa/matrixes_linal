def determinant(matrix):
    rows, cols = len(matrix), len(matrix[0])

    def minor(ai, aj):
        return [[matrix[i][j] for j in range(cols) if j != aj] for i in range(rows) if i != ai]

    if rows != cols:
        return None
    else:
        if rows == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            return sum((-1) ** j * matrix[0][j] * determinant(minor(0, j)) for j in range(cols))


class Matrix:
    def __init__(self, n: int = 0, m: int = 0, data: list[list[float]] = None, other=None):
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

        # print(self.matrix)
        # print(self.n, self.m)

    def __add__(self, other):
        if isinstance(other, Matrix):
            if other.rows == self.rows and other.cols == self.cols:
                result = [[self.matrix[i][j] + other.matrix[i][j] for j in range(self.cols)] for i in range(self.rows)]
                return Matrix(data=result)
            else:
                raise ValueError("Сложение матриц разных размеров")
        elif other is None:
            return self
        else:
            raise TypeError("Неподходящее слагаемое для матрицы")

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.cols != other.rows:
                raise ValueError("Матрицы неподходящих размеров для перемножения")
            res = [[sum(self.matrix[i][k] * other.matrix[k][j] for k in range(self.cols)) for j in range(other.cols)]
                   for i in range(self.rows)]
            # for i in range(self.rows):
            #     for j in range(other.cols):
            #         res[i][j] = sum(self.matrix[i][k] * other.matrix[k][j] for k in range(self.cols))

            return Matrix(data=res) if len(res) != 1 else Vector(data=res[0])
        elif isinstance(other, (int, float)):
            return Matrix(data=[[j * other for j in self.matrix[i]] for i in range(self.rows)])
        elif isinstance(other, X):
            return other * self
        elif isinstance(other, SLAU):
            return SLAU(self * other.matrix, other.x)
        else:
            raise TypeError("Неподходящий множитель для матрицы")

    def __str__(self):
        ans = ""
        for i in self.matrix:
            ans += '(' + ' '.join(map(str, i)) + ')' + '\n'
        return ans.strip()

    def __repr__(self):
        return str(self.matrix)

    def set_data(self, data):
        self.matrix = data.copy()
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])

    def determinant(self):
        return determinant(self.matrix)

    def inverse(self):
        pass

    def union(self):
        pass


class Vector(Matrix):
    def __init__(self, n=0, data: list[float] = None):
        if data is not None:
            super().__init__(data=[data])
        elif n:
            super().__init__(n=1, m=0)
        else:
            super().__init__(data=[[]])


class X(Vector):
    def __init__(self):
        super().__init__()

    def __mul__(self, other):
        if isinstance(other, (Matrix, int, float)):
            return SLAU(other, self)
        else:
            raise TypeError("Неподходящий множитель")


class SLAU:
    def __init__(self, matrix, x, free: Matrix = None):
        self.matrix = matrix
        self.x = x
        self.free = free

    def __mul__(self, other):
        if isinstance(other, (int, float, Matrix)):
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
        return f"SLAU:Matrix={self.matrix.__repr__()}"

    def __repr__(self):
        return self.__str__()

    def __cramer_mat_i(self, a):
        res = [[self.free.matrix[0][i] if j == a else self.matrix.matrix[i][j] for j in range(self.matrix.cols)]
               for i in range(self.matrix.rows)]
        # print(res)
        return res

    def solve(self):
        if not isinstance(self.free, Vector):
            raise ValueError("Неправильная формула")
        if self.matrix.cols > self.matrix.rows:
            return "Бесконечно решений"
        if self.matrix.cols == self.matrix.rows:
            det = self.matrix.determinant()
            dets_i = [determinant(self.__cramer_mat_i(i)) for i in range(self.matrix.cols)]

            print(det)
            print(dets_i)

            return Vector(data=[i / det for i in dets_i])
        else:
            return SLAU(Matrix(data=self.matrix.matrix[:self.matrix.cols]), self.x, self.free).solve()

    def gauss_solve(self):
        pass
