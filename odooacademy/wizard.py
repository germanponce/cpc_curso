# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EstudianteFacturacionWizard(models.TransientModel):
    _name = 'estudiante.facturacion.wizard'
    _description = 'Generacion de Facturas'

    @api.model
    def _get_partner(self):
        print "### _get_partner"
        context = self._context
        estudiantes_obj = self.env['estudiantes.odoo']
        active_ids = context['active_ids']
        print "#### active_ids >>> ",active_ids
        for estudiante in estudiantes_obj.browse(active_ids):
            return estudiante.usuario_id.partner_id.id
                

    cliente_id = fields.Many2one('res.partner','Cliente', 
        default=_get_partner)


    @api.multi
    def crea_factura(self):
        factura_ids = []
        context = self._context
        estudiantes_obj = self.env['estudiantes.odoo']
        for rec in self:
            active_ids = context['active_ids']
            for estudiante in estudiantes_obj.browse(active_ids):
                materias_list = []
                for materia in estudiante.materias_ids:
                    xval = (0,0, {
                            'product_id': materia.name.product_variant_id.id,
                            'name': materia.name.name,
                            'quantity': 1.0,
                            'price_unit': materia.precio,
                            'uom_id': materia.name.uom_id.id,
            'account_id': materia.name.categ_id.property_account_income_categ_id.id,

                        })
                    materias_list.append(xval)

                factura_obj = self.env['account.invoice']
                factura_vals = {
                        'partner_id': self.cliente_id.id,
                        'invoice_line_ids': materias_list,
                }
                factura_id = factura_obj.create(factura_vals)
                factura_ids.append(factura_id.id)

                estudiante.write({
                    'facturado': True,
                    'factura_id': factura_id.id,
                    })

            print "### CONTEXT >>>> ",context
            print "### CREACION DE FACTURAS >>>> "
        return {
                'domain': [('id','in',factura_ids)],
                'name': 'Facturas para el Estudiante',
                'view_mode': 'tree,form',
                'view_type': 'form',
                'res_model': 'account.invoice',
                'type': 'ir.actions.act_window',
            }