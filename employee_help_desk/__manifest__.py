# -*- coding: utf-8 -*-

{
    'name': "Employee Help Desk",
    'version': '16.0.1.0.0',
    'depends': ['base', 'website','hr'],
    'author': "Ashwin",
    'category': 'category',
    'description': """  """,
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'data/website_menu.xml',
        'views/website_template.xml',
        'views/employee_ticket_views.xml',
        'views/employee_ticket_action.xml',
    ],

}
