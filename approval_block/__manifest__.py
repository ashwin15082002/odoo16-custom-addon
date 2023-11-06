# -*- coding: utf-8 -*-


{
    'name': "Approval Block",
    'version': '16.0.1.0.0',
    'depends': ['base', 'mail', 'purchase'],
    'author': "Ashwin",
    'category': 'Category',
    'description': """  
    
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'data/approval_block_data.xml',
        'views/purchase_order_view.xml',
        'views/approval_block_views.xml',
        'views/approval_block_action.xml',

    ],
}
