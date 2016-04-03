####################
# i think I need to start back with two index support, this will capture more of the issues 
####################


from __future__ import division
from sympy import *
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)
init_printing()

str_mtrx = "0 48 0 0 0 0 2 -1 0 -6 0 -4" #!! current problem with this is the possibility to get upward movement of row with more zeros than other rows
f = lambda A, n=4 : [A[i:i+n] for i in range(0,len(A),n)] 
p = lambda A : Matrix(f([ int (i) for i in A.split()]))
my_mat = p(str_mtrx)
def RREF(mtx):
    """this function exists to perform the correct operations and shifts to a matrix
    resulting in what is known as the echelon form
    
    it only takes a matrix mtx and changes it in place
    
    returns none"""
    row,col = (0,0)
    i = 0 #this is our indexer for the rows of the mtx matrix
    try_cap = mtx.rows+10 #this is a backup value that has been coded do decrease while the function performs operations likely to infinite loop

    pprint(mtx) #this command prints out our matrix using the latex character parser
    while col < mtx.cols-1: # quite possibly not necessary for ending, this while loop will run until we reach an i value 1 less than the number of columns, no operations need to be performed on the final row anyways
        if row == mtx.rows-1: # rowf we reach the last row, we don't need to do anything more
            print("done")
            pprint(mtx)
            break

        col_list = list( mtx[row:,col] ) #each time we run the loop will give us a list of the columns below the row we are creating a pivot for
        zero_check = [i==0 for i in col_list] #this feels somewhat unwieldly
        if False not in zero_check:
            print("column of zeros")
            col += 1
            continue
        if col_list[0] != 0: #this check creates error when rest of column shrinks
            if col_list.count(0) == mtx.rows -(row + 1): # example is, if the first row pivot has been created in a 3x?, then we will have 3-(0 + 1) which is 2, should have 2 zeros 
                print("pivot column found") 
                pprint(mtx) # throws is where the while loop could tick overto the next
                row += 1
            else: # this needs to happen for each non zero col entry with a row to match
                print("row replacing")
                 #this creates a list using list comprehension featuring the indexes in the column that row operations need to be applied to
                #!! have problem here because when we are dealing with rows that have a far left entry of zero it can't find an index to use 
                print("rep_ind is",find_first_rep(mtx,col_list))
                try_cap -= 1
                   
                print("replacing row with leading entry",col_list[find_first_rep])
                pprint(mtx)
                multiple_factor = add_mult_row(mtx,mtx[row,:] , mtx[find_first_rep,:] )[0] #effectively says solve for x that makes this 0
                #multiple_factor = non_sym_operation(mtx,mtx.row(i) , mtx.row(rep_ind)) #this is a function call to the below function use to give us a multiple that makes the row addition zero out the leading entry of the non i index rows
                print(multiple_factor, "is multiple factor")
                print("addition row looks like")
                pprint(mtx[row,:]*multiple_factor)
                mtx[rep_ind,:] += mtx[row,:]*multiple_factor #this is an operator overloading expression meaning that we tell python to add the right information to the assigned variable and update the variable we are naming, this is equivalent to saying xnew = xold + some val
                print("elementary row operation took place")
                pprint(mtx)

        else:
            if try_cap < 0: # if we try to perform 5 row switches without triggering any of the above code, then we are probably broken, and should stop the loop
                break

            swap_ind = find_first_swap(mtx,col) # currently this is prone to error, because we have a value generate from not the original matrix column, but the col_list instead
            print("swapping. try cap is",try_cap)
            swap_rows(mtx,row,swap_ind) # this function swaps the rows that specified by the indexes
            print("swapped")
            pprint(mtx)
            try_cap -= 1

#im starting to notice a need for a general function that can simply tell me whether there is a nonzero term in the column, and what it's index value is. Not two or anything, but just that single return
def swap_rows(mtx,num1,num2):
    top = mtx.row(num1)
    mtx[num1,:] = mtx.row(num2)
    mtx[num2,:] = top
    return mtx
def add_mult_row(mtx,top_row,bottom_row):
    return solve(top_row[0]*x+ bottom_row[0],x)
def find_first_swap (mtx,col):
#this might be all i need for both swapping and for replacing
    current_col = [i == 0 for i in mtx.col(col)]
    if False not in current_col:
        return None
    return current_col.index(False)
def find_first_rep (mtx,col_list):
    current_col = [x ==0 if i!=0 else True for i,x in enumerate(col_list) ]
    return current_col.index(False)

