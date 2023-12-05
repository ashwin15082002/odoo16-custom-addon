# -*- coding: utf-8 -*-

{
    'name': "Pos Product Create Edit",
    'version': '16.0.1.0.0',
    'depends': ['point_of_sale',],
    'author': "Ashwin",
    'category': 'pos',
    'description': """ Clicking on product button show all products as a list view.
                    We can either create a new product from that screen or Edit the existing one """,
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'assets':{
        'point_of_sale.assets':[
            'pos_product_create_edit/static/src/xml/*',
            'pos_product_create_edit/static/src/js/*',
        ],
    },


}
