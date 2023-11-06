# -*- coding: utf-8 -*-

{
    'name': "Customer Due Limit POS",
    'version': '16.0.4.0.0',
    'depends': ['base', 'point_of_sale'],
    'author': "Ashwin",
    'category': 'Category',
    'description': """  """,
    # data files always loaded at installation
    'data': [
        'views/res_partner_views.xml',
        ],
    'assets':{
        'point_of_sale.assets':[
            'pos_customer_due_limit/static/src/js/cust_due_limit.js',
            'pos_customer_due_limit/static/src/xml/pos_partner_list_vew.xml',

        ],
    },
}
