"""Simple input dialog

A modeless dialog with the same input items as dialog3
"""
def create_grid(base, nrows, ncols, shear, color, custom):
    F = Formex(base).replic2(ncols, nrows).shear(0, 1, shear)
    if color == 'index':
        color = arange(nrows*ncols)
    elif color == 'custom':
        color = custom
    F.attrib(color=color)
    return F

def show():
    if dialog.validate():
        F = create_grid(**dialog.results)
        clear()
        draw(F)

def close():
    dialog.close()


flat()
dialog = Dialog([
    _I('base', choices=['4:0123', '3:016']),
    _I('nrows', 2, min=1, text='Number of rows'),
    _I('ncols', 3, min=1, text='Number of columns'),
    _I('shear', 0.0, text='Shear dx/dy'),
    _I('color', choices=['index', 'random', 'custom'], text='Color'),
    _I('custom', value='black', itemtype='color', text='Custom color'),
    ], actions=[('Close', close), ('Show', show)])
dialog.show()

for c in pf.GUI.children():
    print(c)
