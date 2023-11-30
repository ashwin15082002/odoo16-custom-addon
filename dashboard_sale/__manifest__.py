# -*- coding: utf-8 -*-

{
    'name': "Dashboard Sale",
    'version': '16.0.1.0.0',
    'depends': ['base','web', 'sale','board'],
    'author': "Ashwin",
    'category': 'category',
    'description': """  """,
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        'data/sale_dashboard.xml',
    ],
    'assets':{
        'web.assets_backend':[
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js',
            'dashboard_sale/static/src/xml/dashboard_sale.xml',
            'dashboard_sale/static/src/js/dashboard_sale.js',

        ]
    }
}
