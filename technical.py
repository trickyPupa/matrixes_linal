class Matrix:
    def __init__(self, n=0, m=0, data=None):
        self.matrix = []
        if not n and data is None:
            return
        if data is not None:
            self.matrix = data.copy()
        else:
            if not m:
                m = n
            self.matrix = [[0] * m for _ in range(n)]
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])

        # print(self.matrix)
        # print(self.n, self.m)

    def __add__(self, other):
        if isinstance(other, Matrix):
            if other.rows == self.rows and other.cols == self.cols:
                result = [[self.matrix[i][j] + other.matrix[i][j] for j in range(self.cols)] for i in range(self.rows)]
                return Matrix(data=result)
            else:
                raise Exception("Нельзя складывать матрицы разных размеров")
        else:
            raise Exception("Матрицы можно складывать только с матрицами")

    def __mul__(self, other):
        pass

    def __str__(self):
        ans = ""
        for i in self.matrix:
            ans += '(' + ' '.join(i) + ')' + '\n'
        return ans.strip()

    def __repr__(self):
        return str(self.matrix)

    def set_data(self, data):
        self.matrix = data.copy()
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])

    def determinant(self):
        if self.rows != self.cols:
            return None
        else:
            div = 0

            return div

    def slau(self, solution_vector):
        pass

    def gauss_slau(self, solution_vector):
        pass

    def inverse(self):
        pass

    def union(self):
        pass


class Vector(Matrix):
    def __int__(self, n=0, data=None):
        if data is not None:
            super(data=data)
        elif n:
            super(n=1, m=0)
        else:
            super(data=[[]])


class X(Vector):
    def __init__(self):
        pass