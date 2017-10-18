# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError, \
                    RedirectWarning, ValidationError

class EstudiantesOdoo(models.Model):
    _name = 'estudiantes.odoo'

    _inherit = ['mail.thread', 'ir.needaction_mixin']

    _description = 'Modelo Captura Registros Est.'
    _order = 'id'
    #_rec_name = 'nombre' 

    name = fields.Char('Nombre', 
                        size=128, 
                        required=True)

    fecha_registro = fields.Datetime('Fecha Registro',
                    default=fields.Datetime.now)

    active = fields.Boolean('Activo', default=True)

    state = fields.Selection([
                            ('nvo','Nuevo'),
                            ('conf','Confirmado'),
                            ('fin','Ciclo Terminado'),
                            ('cancel','Cancelado'),
                            ], 'Estado', readonly=True, 
                            default='nvo')

    foto = fields.Binary('Fotografia')

    edad = fields.Integer('Edad', required=True)
    genero = fields.Selection([('m','Masculino'),
                                ('f','Femenino')], 
                                'Genero', required=True)
    curp = fields.Char('CURP',size=18)
    matricula = fields.Char('Matricula', size=64, readonly=True)

    fecha_nacimiento = fields.Date('Fecha de Nacimiento', 
                                    equired=True)

    notas  = fields.Text('Notas')

    ### Campos Relacionales ###

    usuario_id = fields.Many2one('res.users',
                                'Usuario Odoo')

    ## Metodos Basicos ORM
    # * Creacion
    # * Escritura
    # * Eliminacion
    # * Busqueda

    @api.model # context, id, cr
    def create(self, vals):
        context = self._context
        print "#### CONTEXT >>>> ",context
        cr = self._cr
        print "#### CR >>> ",cr
        print "#### VALS >>>> ",vals
        # id = self.id
        print "#### "
        ### Consumiendo la Secuencia ###
        matricula_secuencia = self.env['ir.sequence'].\
        next_by_code('estudiantes.odoo') or 'SIN-MT'
        vals['matricula'] = matricula_secuencia

        curp_mayusculas = vals['curp']
        if curp_mayusculas:
            curp_mayusculas = curp_mayusculas.upper()
            vals['curp'] = curp_mayusculas
            print "### LEN(CURP) ",len(curp_mayusculas)
            if len(curp_mayusculas) < 18:
                raise UserError("Error el CURP debe ser a 18 Dig.")
        
        if 'usuario_id' not in vals or not vals['usuario_id']:
            usuarios_obj = self.env['res.users']
            usuario_vals = {
                    'name': vals['name'],
                    'login': matricula_secuencia,#vals['name'].split(' ')[0].lower(),
                    }
            usuario_nuevo = usuarios_obj.create(usuario_vals)
            print "### USUARIO NUEVO >> ",usuario_nuevo
            usuario_nuevo_id = usuario_nuevo.id

            vals['usuario_id'] = usuario_nuevo_id

        res = super(EstudiantesOdoo, self).create(vals)
        print "### RECORDSET >>> ",res
        return res

    # * requerido = required
    # * solo lectura = readonly
    # * indexado = index
    # * copiado = copy



class ProfesorOdoo(models.Model):
    _name = 'profesor.odoo'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Registro para Profesores' 
    _order = 'id'
    #_rec_name = 'nombre' 
    name = fields.Char('Nombre Completo', 
                        size=128, 
                        required=True)
    fecha_registro = fields.Datetime('Fecha Registro',
                    default=fields.Datetime.now)

    active = fields.Boolean('Activo', default=True)

    foto = fields.Binary('Fotografia')
    edad = fields.Integer('Edad', required=True)
    genero = fields.Selection([('m','Masculino'),
                                ('f','Femenino')], 
                                'Genero')
    cedula_profesional = fields.Char('Cedula Profesional',required=True )
    usuario_id = fields.Many2one('res.users',
                                'Usuario Odoo')
    notas = fields.Text('Comentarios')
    carrera_profesional = fields.Char('Carrera Profesional', size=128, required=True)