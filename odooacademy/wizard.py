# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EstudianteFacturacionWizard(models.TransientModel):
    _name = 'estudiante.facturacion.wizard'
    _description = 'Generacion de Facturas'


    @api.multi
    def crea_factura(self):
    	print "### CREACION DE FACTURAS >>>> "
    	factura_ids = []
    	return {
                'domain': [('id','in',factura_ids)],
                'name': 'Facturas para el Estudiante',
                'view_mode': 'tree,form',
                'view_type': 'form',
                'res_model': 'account.invoice',
                'type': 'ir.actions.act_window',
            }