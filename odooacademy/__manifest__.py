# -*- coding: utf-8 -*-

{
    'name': 'Modulo Odoo Escuela',
    'version': '1.0',
    'category': 'Corona',
    'description': """
MODULO CONTROL REGISTROS

Este modulo permite conocer y utilizar
las Bases de Desarrollo con  Odoo.

Instalar:

sudo apt-get update
sudo apt-get install xvfb libfontconfig wkhtmltopdf

    """,
    'author': 'German Ponce D.',
    'website': 'https://argil.mx',
    'depends': ['mail','product','decimal_precision','account','report'],
    'data': [
        'wizard.xml',
        'estudiantes_view.xml',
        'profesores_view.xml',
        'product_view.xml',
        'data.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'report.xml',
    ],
    'installable': True,
    'auto_install': False,
}
