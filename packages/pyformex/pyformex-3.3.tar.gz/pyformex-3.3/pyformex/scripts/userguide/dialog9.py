"""Simple input dialog

Visual improvements to the layout
"""
choices = ['Left', 'Up', 'Right']
icons = ['left', 'up', 'right']

res = askItems([
    _I(choices=choices, itemtype='push'),
    _I(choices=choices, itemtype='push', icons=icons),
    _I(choices=choices, itemtype='push', icons=icons, iconsonly=True),
    _I(choices=choices, itemtype='push', small=True),
    _I(choices=choices, itemtype='vpush'),
    ])
print(res)
