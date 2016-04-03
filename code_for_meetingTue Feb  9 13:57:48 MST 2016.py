trbl_mkr = "1 4 1 1 2 8 -1 4 5 0 1 1" #having 48 crashed program
trbl_mtrx = p(trbl_mkr)
pprint(trbl_mtrx)

str_mtrx = "2 0 0 0 1 0 2 -1 2 -1 0 -4"
f = lambda A, n=4 : [A[i:i+n] for i in range(0,len(A),n)] #this creates a short purposed function that is used with the one below to give us a sympy matrix object from a string of integers separated by spaces
p = lambda A : Matrix(f([ int (i) for i in A.split()]))
my_mat = p(str_mtrx)
my_mat
def RREF(mtx):
    """this function exists to perform the correct operations and shifts to a matrix
    resulting in what is known as the echelon form
    
    it only takes a matrix mtx and changes it in place
    
    returns none"""
    i = 0 #this is our indexer for the rows of the mtx matrix
    try_cap = 5 #this is a backup value that has been coded do decrease while the function performs operations likely to infinite loop

    pprint(mtx) #this command prints out our matrix using the latex character parser
    while i < mtx.cols-1: # quite possibly not necessary for ending, this while loop will run until we reach an i value 1 less than the number of columns, no operations need to be performed on the final row anyways
        col_list = list(mtx.col(i)[i:]) #each time we run the loop will give us a list of the columns below the row we are creating a pivot for
        if i == mtx.rows-1: # if we reach the last row, we don't need to do anything more
            print("done")
            pprint(mtx)
            break
        if col_list[0] != 0: #this check creates error when rest of column shrinks
            if col_list.count(0) == mtx.rows -(i + 1): # the plus ones are going to need to go sooner or later
                print("pivot column found") 
                pprint(mtx) # this is where the while loop could tick overto the next
                i += 1
            else: # this needs to happen for each non zero col entry with a row to match
                print("row replacing")
                rep_inds = [i for i in range(i+1,len(col_list)) if col_list[i] != 0] #this creates a list using list comprehension featuring the indexes in the column that row operations need to be applied to
                print("rep_inds are",rep_inds)
                for rep_ind in rep_inds: # now we iterate through the indexes of the rows that need to have elementary row operations on them
                    print("replacing row with leading entry",col_list[rep_ind])
                    pprint(mtx)
#                     multiple_factor = add_mult_row(mtx,mtx.row(i) , mtx.row(rep_ind) )[0] #effectively says solve for x that makes this 0
                    multiple_factor = non_sym_operation(mtx,mtx.row(i) , mtx.row(rep_ind)) #this is a function call to the below function use to give us a multiple that makes the row addition zero out the leading entry of the non i index rows
                    print(multiple_factor, "is multiple factor")
                    print("addition row looks like")
                    pprint(mtx.row(i)*multiple_factor)
                    mtx[rep_ind,:] += mtx.row(i)*multiple_factor #this is an operator overloading expression meaning that we tell python to add the right information to the assigned variable and update the variable we are naming, this is equivalent to saying xnew = xold + some val
                    print("elementary row operation took place")
                    pprint(mtx)

        else:
            if try_cap < 0: # if we try to perform 5 row switches without triggering any of the above code, then we are probably broken, and should stop the loop
                break
            print("swapping. try cap is",try_cap)
            swap_num = i+1 #this will have to become more flexible, related to i
            swap_rows(mtx,i,swap_num) # this function basically shifts all the rows up by one, such that we wind up with the leading zero rows lower than the others
            print("swapped")
            pprint(mtx)
            try_cap -= 1
