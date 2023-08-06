"""Simple input dialog

The same dialog as dialog1, but using the _I function to construct
the items, and globals().update to set the results in global variables.
"""

res = askItems([
    _I('nrows', 3),
    _I('ncols', 6),
])
if res:
    globals().update(res)
    A = np.arange(nrows*ncols).reshape(nrows,ncols)
    print(A)
