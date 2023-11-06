# -*- coding: utf-8 -*-

{
    'name': "Credit Limit",
    'version': '16.0.1.0.0',
    'depends': ['base', 'account','sale','mrp'],
    'author': "Ashwin",
    'category': 'Category',
    'description': """  """,
    'installable': True,
    'application': True,

    # data files always loaded at installation
    'data':[
        'views/res_partner_views.xml',
        'views/sale_order_form.xml',
    ]

}
