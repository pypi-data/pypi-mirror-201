"""Simple input dialog

A modeless dialog with the same input items as dialog3
"""
def print_array(nrows, ncols):
    A = np.arange(nrows*ncols).reshape(nrows,ncols)
    print(A)

def show():
    if dialog.validate():
        create_array(**dialog.results)

def close():
    dialog.close()

dialog = Dialog([
    _I('nrows', 3, min=0, text='Number of rows'),
    _I('ncols', 6, min=2, max=10, text='Number of columns'),
    ], actions=[('Close', close), ('Show', show)])
dialog.show()
