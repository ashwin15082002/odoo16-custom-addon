# -*- coding: utf-8 -*-

{
    'name': "Stock Report",
    'version': '16.0.4.0.0',
    'depends': ['stock'],
    'author': "Ashwin",
    'category': 'inventory',
    'description': """  Generate and send stock report to the inventory manager at the end of the day. """,
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        'data/email_template.xml',
        'data/scheduler.xml',
        'report/report_action.xml',
        'report/pdf_template.xml',
    ],

}
