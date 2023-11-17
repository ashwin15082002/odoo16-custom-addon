# -*- coding: utf-8 -*-

{
    'name': "brand",
    'version': '16.0.1.0.0',
    'depends': ['sale'],
    'author': "Ashwin",
    'category': 'Category',
    'description': """  """,
    'installable': True,
    'application': True,

    # data files always loaded at installation
    'data':[
        'data/sheduler.xml',
        'views/product_template_views.xml',
        'views/sale_order_line_views.xml',
        'views/stock_move_line_views.xml',
    ]

}
