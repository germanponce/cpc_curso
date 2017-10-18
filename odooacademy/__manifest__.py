# -*- coding: utf-8 -*-

{
    'name': 'Modulo Odoo Escuela',
    'version': '1.0',
    'category': 'Corona',
    'description': """
MODULO CONTROL REGISTROS

Este modulo permite conocer y utilizar
las Bases de Desarrollo con  Odoo.

    """,
    'author': 'German Ponce D.',
    'website': 'https://argil.mx',
    'depends': ['mail'],
    'data': [
        'estudiantes_view.xml',
        'profesores_view.xml',
        'data.xml',
    ],
    'installable': True,
    'auto_install': False,
}