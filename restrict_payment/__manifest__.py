# -*- coding: utf-8 -*-

{
    'name': "Restrict Payment",
    'version': '16.0.1.0.0',
    'depends': ['base', 'website', 'account'],
    'author': "Ashwin",
    'category': 'category',
    'summary': 'Restrict payment acquirers',
    'description': """ Restrict payment acquirers based on the order amount. Users should be able to
                        set a minimum and maximum amount on which each payment acquirer applies. """,
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        'views/payment_provider_views.xml',
    ],
}
