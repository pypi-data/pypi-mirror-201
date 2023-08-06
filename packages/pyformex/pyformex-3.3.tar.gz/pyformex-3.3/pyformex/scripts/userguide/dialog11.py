"""Simple input dialog

Compound objects in InputString
"""
res = askItems([
    _I('string', "This is a string"),
    _I('text_plain', """
Text(plain)
This is a multiline text
in plain format
""", 'text'),
    _I('text_rst', """..

Text(rst)
---------
This is a multiline text
in rst format.

It is converted to html before display.
""", 'text'),
    _I('text_rst1', """..

Text(rst)
---------
This is a multiline text
in rst format.

It is converted to html before display.
""", 'text', ret_format='html'),
    ])
print(res)
