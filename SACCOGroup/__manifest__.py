{
    'name': 'SACCO',
 
    'category': 'Sacco Droga',
    'sequence': 5,
    'summary': 'Track leads and close opportunities',
    'website': 'https://www.odoo.com/app/crm',
    'depends': [
        'base_setup','hr',
    ],
    'data': ['views/sacco_views.xml'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
