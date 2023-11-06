# -*- coding: utf-8 -*-
{
    'name': "Simple Production",
    'version': '16.0.1.0.0',
    'depends': ['base', 'product', 'stock'],
    'author': "Ashwin",
    'category': 'Category',
    'description': """  """,
    'installable': True,
    'application': True,

    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'data/product_sequence_data.xml',
        'views/bom_views.xml',
        'views/sp_views.xml',
        'views/sp_menu.xml',
    ]
}
