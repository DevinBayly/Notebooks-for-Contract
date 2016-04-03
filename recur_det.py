from __future__ import division
import random
from sympy import *
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)
init_printing()
import ipdb

my_mat = Matrix(3,3,[random.randrange(100) for i in range(9)])
pprint(my_mat)
print("starting")
def split_mtx(mtx,row,col):
    mtx.row_del(row)
    mtx.col_del(col)
    return mtx
def recurse_det(mtx):
    if len(mtx) == 1:
        print("bottom of recurse")
        pprint(mtx)
        return mtx 
    else:
        print("stripping")
        pprint(mtx)
        return sum([mtx[0,i]*recurse_det(split_mtx(mtx.copy(),0,i))[0] if i%2 == 0 else
                    -mtx[0,i]*recurse_det(split_mtx(mtx.copy(),0,i))[0]
                    for i in range(mtx.cols)])
ipdb.runcall(recurse_det,my_mat)    
print(my_mat.det())
        
