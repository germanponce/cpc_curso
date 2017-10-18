# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit ='product.template' # Clave para la Herencia

    es_asignatura = fields.Boolean('Asignatura Escolar')
    

    # type = fields.Selection([('service','Servicio'),
    #                        ('consu','Consumible'),
    #                        ('materia','Materia Escolar')
    #                           ], 'Tipo')