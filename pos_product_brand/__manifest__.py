# -*- coding: utf-8 -*-


{
    'name': "Product Brand POS",
    'version': '16.0.4.0.0',
    'depends': ['base', 'point_of_sale'],
    'author': "Ashwin",
    'category': 'Category',
    'description': """  """,
    # data files always loaded at installation
    'data': [
        'views/product_form.xml',
        ],
    'assets':{
        'point_of_sale.assets':[
            'pos_product_brand/static/src/js/custom_order_receipt.js',
            'pos_product_brand/static/src/xml/pos_orderline.xml',
            'pos_product_brand/static/src/xml/pos_order_receipt.xml',

        ],
    },
}
