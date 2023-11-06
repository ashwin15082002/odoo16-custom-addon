# -*- coding: utf-8 -*-

{
    'name': "Most Sold Product",
    'version': '16.0.4.0.0',
    'depends': ['base','sale','product','website'],
    'author': "Ashwin",
    'category': 'Category',
    'description': """   """,
    # data files always loaded at installation
    'data': [
        'views/snippet.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'most_sold_product/static/src/xml/product_view.xml',
            'most_sold_product/static/src/xml/product_snippet.xml',
            'most_sold_product/static/src/js/product_snippet.js',
        ]
    },
}
