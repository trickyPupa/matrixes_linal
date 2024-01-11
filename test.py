import sympy
from technical import *

x, y = sympy.symbols('x y')
f = x + y

x = Matrix(data=[[1, 2, 3], [2, 3, 4]])
y = Matrix(data=[[1, 1, 1], [1, 1, 1]])

f.subs([(x, x), (y, y)])
print(f)