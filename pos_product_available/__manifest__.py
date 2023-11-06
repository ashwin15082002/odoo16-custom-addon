# -*- coding: utf-8 -*-


{
    'name': "Product Available POS",
    'version': '16.0.4.0.0',
    'depends': ['base', 'point_of_sale','stock'],
    'author': "Ashwin",
    'category': 'Category',
    'description': """  """,
    # data files always loaded at installation
    'data': [
        'views/product_views.xml',
        'views/pos_setting_views.xml',
        ],
    'assets':{
        'point_of_sale.assets':[
            'pos_product_available/static/src/xml/product_available.xml',
        ],
    },
}
