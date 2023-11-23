# -*- coding: utf-8 -*-

{
    'name': "Idle Timer",
    'version': '16.0.1.0.0',
    'depends': ['base', 'survey'],
    'author': "Ashwin",
    'category': 'category',
    'description': """ Set an idle timer for the quiz,
                        If mouse and keyboard are idle for a particular time,  timer should start 
                        After a particular time it should move to next page.
                        Note:  Set the required timings in the configuration . """,
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        'views/idle_timer.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'survey.survey_assets': [
            '/idle_timer/static/src/js/idle_timer.js',
        ]
    },
}
