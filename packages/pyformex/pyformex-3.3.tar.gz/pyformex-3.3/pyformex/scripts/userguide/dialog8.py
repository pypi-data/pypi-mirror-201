"""Simple input dialog

Visual improvements to the layout
"""
res = askItems([
    _I('val0', 0, text='Default formatting'),
    _I('val1', 1, text="spacer='l'", spacer='l'),
    _I('val2', 2, text="spacer='r'", spacer='r'),
    _I('val3', 3, text="spacer='c'", spacer='c' ),
    _I('val4', 4, text="spacer='lr'", spacer='lr' ),
    _I('val5', 5, text="width=800", width=30),
    _I('val6', 6, text="enabled=False", enabled=False),
    _I('val7', 7, text="readonly=True", readonly=True),
    _I('val8', choices=list(range(20)), itemtype='list', maxh=10),
    ])
print(res)
