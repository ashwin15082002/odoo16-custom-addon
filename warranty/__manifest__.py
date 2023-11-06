# -*- coding: utf-8 -*-


{
    'name': "Warranty",
    'version': '16.0.4.0.0',
    'depends': ['base', 'mail', 'sale', 'account', 'product', 'stock',
                'website'],
    'author': "Ashwin",
    'category': 'Category',
    'description': """  
    In this module can create warranty request for warranty available products,
    and create stock move from and to customer location and warranty location, and in the invoice we can see the warranty request created 
    inside the invoice
    """,
    # data files always loaded at installation
    'data': [
        'security/warranty_module_management.xml',
        'security/ir.model.access.csv',

        'data/ir_sequence_data.xml',
        'data/stock_location_data.xml',
        'data/website_menu.xml',

        'views/warranty_views.xml',
        'views/product_template_views.xml',
        'views/account_move_views.xml',

        'views/website_warranty_template.xml',
        'views/snippet/warranty_snippet_template.xml',
        'views/snippet/warranty_snippet.xml',

        'wizard/wizard.xml',
        'report/report_template.xml',
        'report/warranty_report.xml',
        'views/warranty_action.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/warranty/static/src/js/action_manager.js',
        ],
        'web.assets_frontend': [

            'warranty/static/src/xml/qweb_template.xml',
            'warranty/static/src/js/warranty_snippet.js',
            'warranty/static/src/js/warranty_request.js',
        ]

    },
}
