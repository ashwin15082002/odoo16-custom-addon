# -*- coding: utf-8 -*-

{
    'name': "Weather Notification",
    'version': '16.0.4.0.0',
    'depends': ['web'],
    'author': "Ashwin",
    'category': 'category',
    'description': """  """,
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        'views/settings_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/weather_notification/static/src/xml/weather.xml',
            'weather_notification/static/src/js/weather_notification.js',
        ],
    }

}
