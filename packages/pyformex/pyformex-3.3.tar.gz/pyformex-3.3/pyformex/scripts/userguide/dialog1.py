"""Simple input dialog

Creates an (nrows, ncols) array filled with numbers from arange(nrows*ncols).
The values nrows and ncols are asked from the user.
"""

res = askItems([
    dict(name='nrows', value=3),
    dict(name='ncols', value=6),
])
if res:
    nrows = res['nrows']
    ncols = res['ncols']
    A = np.arange(nrows*ncols).reshape(nrows,ncols)
    print(A)
