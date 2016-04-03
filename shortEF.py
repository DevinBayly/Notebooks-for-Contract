from __future__ import division
import random
from sympy import *
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)
init_printing()
import ipdb
def rolling_rep(mtx,row_starting):
    rep_row = mtx[row_starting,:]
    ret_mat = mtx.copy()
    ret_mat.row_del(row_starting)
    return ret_mat.row_insert(ret_mat.rows,rep_row)

def target_swap(mtx,row,lst):
    ret_mtx = mtx.copy()
    rep_ind = find_nonzero_ind(lst,row)
    if rep_ind:
        rep_row = ret_mtx[rep_ind,:]
        ret_mtx[rep_ind,:] = ret_mtx[row,:]
        ret_mtx[row,:] =rep_row
        return ret_mtx
    return False

def find_nonzero_ind(lst,row):
    lst_to_bool = [x == 0 if i > row else True for i,x in enumerate(lst)]
    if False not in lst_to_bool:
        return False
    return lst_to_bool.index(False)

def add_mult_row(mtx,piv_row,other):
    return solve(piv_row*x+ other,x)[0]


import ipdb

def shortRREF(mtx):
    cop = mtx.copy()
    row,col = 0,0
    try_cap = cop.rows + 30
    while row < cop.rows -1 and col < cop.cols:
        col_list = list(cop[:,col])
        if try_cap < 0:
            return (row,col)
        if col_list.count(0) == cop.rows or col_list[row:].count(0) > cop.rows -1 -row:
            col +=1
            continue
        if cop[row,col] == 0 and col_list[row]!= col_list[row+1]:
                #cop = rolling_rep(cop,row)
                cop = target_swap(cop,row,col_list)
                pprint(cop)
                try_cap -=1
                continue
        if col_list[row:].count(0) == cop.rows -1 -row:
            col +=1
            row +=1
            continue
        else:
            
            rep_ind = find_nonzero_ind(col_list,row) #makes sure to not include the potential pivot row in the search but keeps the indexing constant with mtx
            multiple_factor = add_mult_row(cop,cop[row,col],cop[rep_ind,col])
            cop[rep_ind,:] += cop[row,:]*multiple_factor
            pprint(cop)
    return cop
trbl_makr = Matrix(4,8,[
0,0,0,0,25,0,0,54,4,0,0,0,71,52,82,0,0,0,0,0,61,51,0,0,0,0,0,14,37,77,85,0 
])
## trbl seems to be about two zeros next to each other, fixed by using a check against 


ipdb.runcall(shortRREF,trbl_makr)
