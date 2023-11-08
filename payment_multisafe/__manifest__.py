# -*- coding: utf-8 -*-

{
    'name': "Multisafe Pay",
    'version': '16.0.4.0.0',
    'depends': ['payment', 'website'],
    'author': "Ashwin",
    'category': 'Category',
    'description': """   """,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        # 'views/payment_provider_form.xml',
        'views/payment_multisafe_templates.xml',
        'views/payment_provider_form.xml',
        'data/payment_provider_data.xml'
    ],

}
