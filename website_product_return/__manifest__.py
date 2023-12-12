# -*- coding: utf-8 -*-

{
    'name': "Multi Product Return",
    'version': '16.0.4.0.0',
    'depends': ['sale','website','stock'],
    'author': "Ashwin",
    'category': 'category',
    'description': """  """,
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        'views/portal_views.xml',
    ],
    'assets': {

        'web.assets_frontend': [
         'website_product_return/static/src/js/produt_return.js',
        ]
    },
}
