"""Simple input dialog

Compound objects in InputString
"""
res = askItems([
    _I('string', "This is a string"),
    _I('tuple', tuple('This is a tuple'.split())),
    _I('list', 'This is a list'.split()),
    _I('dict', dict(enumerate('This is a dict'.split()))),
    ])
print(res)
