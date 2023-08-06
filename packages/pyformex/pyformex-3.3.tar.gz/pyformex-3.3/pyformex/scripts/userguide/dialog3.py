"""Simple input dialog

Similar dialog as dialog2, but with limits on the input values,
more explicative labels, and a function to print the array.
"""
def print_array(nrows, ncols):
    A = np.arange(nrows*ncols).reshape(nrows,ncols)
    print(A)

res = askItems([
    _I('nrows', 3, min=0, text='Number of rows'),
    _I('ncols', 6, min=2, max=10, text='Number of columns'),
])
if res:
    print_array(**res)
