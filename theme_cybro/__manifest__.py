# -*- coding: utf-8 -*-

{
    'name': "Theme Cybro",
    'version': '16.0.1.0.0',
    'depends': ['website'],
    'author': "Ashwin",
    'category': 'theme',
    'summary': 'Technology',
    'description': """  """,
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        'data/menu.xml',
        'data/pages/about_us.xml',
    ],
    'images':['static/description/clean_description.jpg',
              'static/description/clean_screenshot.jpg',
              ],
    'assets':{
        'web._assets_primary_variables': [
            'theme_cybro/static/scss/primary_variabes.scss',
        ],
    }
}
