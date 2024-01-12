from technical import *

a = Matrix(data=[[506, 66], [66, 11]])
b = SLAU(a, X(), Vector(data=[2315.1, 392.3]))

print(b.solve())
