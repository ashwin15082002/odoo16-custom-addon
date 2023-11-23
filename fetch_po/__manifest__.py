# -*- coding: utf-8 -*-

{
    'name': "Fetch PO",
    'version': '16.0.1.0.0',
    'depends': ['base', 'purchase'],
    'author': "Ashwin",
    'category': 'category',
    'description': """ . """,
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard.xml',

        'views/purchase_views.xml',

    ],

}
