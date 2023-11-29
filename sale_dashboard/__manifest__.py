# -*- coding: utf-8 -*-

{
    'name': "Sale Dashboard",
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
            'sale_dashboard/static/src/xml/sale_dashboard.xml',
            'sale_dashboard/static/src/xml/chart_rendered.xml',
            'sale_dashboard/static/src/js/sale_dashboard.js',
            'sale_dashboard/static/src/js/chart_rendered.js',

        ]
    }
}
