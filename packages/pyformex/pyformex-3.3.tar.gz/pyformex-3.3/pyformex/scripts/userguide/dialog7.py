"""Simple Button Box

"""
from pyformex.gui.widgets import ButtonBox

def show(fld):
    n = fld.name()
    i = fld.checkedId()
    v = fld.value()
    print(f"You clicked button {i} = {v} of button group {n}")

def showleft():
    print('BB left')

def showright():
    print('BB right')

def results():
    if dia.validate():
        print("Current results:")
        print(dia.results)
    else:
        print("Input data are invalid")


BB = ButtonBox(name='bb', actions=[('left',showleft),('right',showright)])

dia = Dialog(items=[
    _I('push', itemtype='push', choices=['left','right','up','down'],
       func=show, icons=['left','right',None,None]),
    _I('push2', itemtype='push', choices=['left','right','up','down'],
       value='right', func=show,
       icons=['left','right','up','down'], iconsonly=True),
    _I('bb', BB, itemtype='widget'),
    ], actions=[('Close',), ('Results', results)], buttonsattop=False)

dia.show()
