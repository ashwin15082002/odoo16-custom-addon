
{
    'name': 'Product Create Or Edit From Point of Sale ',
    'version': '16.0.1.0.1',
    'summary': 'This Module will help to create and edit products directly from point of sale.',
    'category': 'Point of Sale',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'depends': ['base', 'point_of_sale'],
    'assets': {
        'point_of_sale.assets': [
            'Pos/static/src/js/*',
            'Pos/static/src/xml/*',
            'Pos/static/src/css/*',
        ],
    },
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
