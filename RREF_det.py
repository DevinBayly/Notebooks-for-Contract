from __future__ import division
import random
from sympy import *
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)
init_printing()
import ipdb

pseudo_det = 1
def target_swap(mtx,row,lst):
    ret_mtx = mtx.copy()
    rep_ind = find_nonzero_ind(lst,row)
    if rep_ind:
        rep_row = ret_mtx[rep_ind,:]
        ret_mtx[rep_ind,:] = ret_mtx[row,:]
        ret_mtx[row,:] =rep_row
        return ret_mtx
    return False

def find_nonzero_ind(lst,row,backwards=False):
    if backwards:
        lst_to_bool = [x == 0 if i < row else True for i,x in enumerate(lst)]
    else:
        lst_to_bool = [x == 0 if i > row else True for i,x in enumerate(lst)]
    if False not in lst_to_bool:
        return False
    return lst_to_bool.index(False)

def add_mult_row(mtx,piv_row,other):
    return solve(piv_row*x+ other,x)[0]

def grab_diag(mtx):
    d = 1
    for i in range(mtx.rows):
        d*=mtx[i,i]
    return d
def give_pseudo_det():
    global pseudo_det
    if pseudo_det == 0:
        return 0
    else:
        return 1/pseudo_det

def shortEF(mtx):
    global pseudo_det
    pivots = []
    cop = mtx.copy()
    row,col = 0,0
    try_cap = cop.rows + 30
    while row < cop.rows and col < cop.cols: #took off -1 from cop.rows mighthave broken stuff
        col_list = list(cop[:,col])
        if try_cap < 0:
            return (row,col)
        if col_list.count(0) == cop.rows or col_list[row:].count(0) > cop.rows -1 -row:
            col +=1
            continue
        if cop[row,col] == 0 :
                #cop = rolling_rep(cop,row)
                cop = target_swap(cop,row,col_list)
                try_cap -=1
                pseudo_det *= -1
                continue
        if col_list[row:].count(0) == cop.rows -1 -row:
            pivots.append((row,col))
            col +=1
            row +=1
            continue
        else:
            
            rep_ind = find_nonzero_ind(col_list,row) #makes sure to not include the potential pivot row in the search but keeps the indexing constant with mtx
            multiple_factor = add_mult_row(cop,cop[row,col],cop[rep_ind,col])
            cop[rep_ind,:] += cop[row,:]*multiple_factor
    reduce_row(cop,pivots)
    return cop

def reduce_row(mtx,pivot_lst):
    pivot_lst.reverse()
    for row,col in pivot_lst:
        global pseudo_det
        pseudo_det /= mtx[row,col]
        mtx[row,:] = mtx[row,:]/mtx[row,col]
        col_list = list(mtx[:,col])
        while col_list.count(0) < mtx.rows -1:
            rep_ind = find_nonzero_ind(col_list,row,True) #makes sure to not include the potential pivot row in the search but keeps the indexing constant with mtx
            multiple_factor = add_mult_row(mtx,mtx[row,col],mtx[rep_ind,col])
            mtx[rep_ind,:] += mtx[row,:]*multiple_factor
            col_list = list(mtx[:,col])
    pseudo_det *= grab_diag(mtx)

    
## trbl seems to be about two zeros next to each other, fixed by using a check against 


##ipdb.runcall(shortEF,trbl_makr)

def main ():
    global pseudo_det
    serious_trbl_mkrs = []
    runs = 200
    for i in range(runs):
        pseudo_det = 1
        trbl_mkr = Matrix(4,4,[random.randrange(1,100) if random.randrange(1,5) < 3 else 0 for num in range(16)])
        if shortEF(trbl_mkr) != trbl_mkr.rref()[0]:
            serious_trbl_mkrs.append(trbl_mkr)
        print(give_pseudo_det(),trbl_mkr.det())
    pprint(serious_trbl_mkrs)
    if len(serious_trbl_mkrs)/runs == 0.0:
        print('no incorrect RREFS')

if __name__ == "__main__":
    #main()
    ipdb.runcall(main)
    
