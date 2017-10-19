# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError, \
                    RedirectWarning, ValidationError

from odoo.addons import decimal_precision as dp

from datetime import datetime, timedelta
from odoo.tools import misc, \
DEFAULT_SERVER_DATETIME_FORMAT

class PasatiempoOdoo(models.Model):
    _name = 'pasatiempo.odoo'
    _description = 'Pasatiempos del Estudiante'

    name = fields.Char('Descripcion', size=128, 
                                   required=True)

    
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
    curp = fields.Char('CURP',size=18, track_visibility="onchange")
    matricula = fields.Char('Matricula', size=64, readonly=True)

    fecha_nacimiento = fields.Date('Fecha de Nacimiento', 
                                    equired=True,
                                    track_visibility="onchange")

    notas  = fields.Text('Notas')

    ### Campos Relacionales ###

    usuario_id = fields.Many2one('res.users',
                                'Usuario Odoo', track_visibility="onchange")

    materias_ids = fields.One2many('materia.odoo',
                        'estudiante_id',
                        'Asignaturas/Materias')

    pasatiempos_ids = fields.Many2many('pasatiempo.odoo',
                        'estudiantes_pasatiempos_rel',
                        'estudiante_id',
                        'pasatiempo_id',
                        'Pasatiempos')

    @api.multi
    def accion_confirmar(self):
        print "### SELF >>> ",self
        for rec in self:
            print "### rec name >>> ",rec.name
            if not rec.curp:
                raise UserError("Error!\nNo puedes confirmar \
                    sin tener un valor en el campo CURP...")
            self.state = 'conf'
            rec.message_post(body='El usuario %s \
                confirmo el Registro' % self.env.user.name)
            #self.write({'state':'conf'})

    @api.multi
    def accion_cancelar(self):
        for rec in self:
            self.state = 'cancel'
            rec.message_post(body='El usuario %s \
                cancelo el Registro' % self.env.user.name)
            #self.write({'state':'conf'})

    @api.multi
    def accion_a_nuevo(self):
        for rec in self:
            self.state = 'nvo'
            rec.message_post(body='El usuario %s \
                reedito el Registro' % self.env.user.name)
            #self.write({'state':'conf'})

    @api.multi
    def accion_cerrar(self):
        for rec in self:
            self.state = 'fin'
            rec.message_post(body='El usuario %s \
                finalizo el Registro' % self.env.user.name)
            #self.write({'state':'conf'})

    @api.onchange('fecha_nacimiento')
    def onchange_calculo_edad(self):
        if not self.fecha_nacimiento:
            return {}
        print "#### CALCULO AUTOMATICO DE EDAD >>> "
        fecha_actual = fields.Datetime.now()
        fecha_nacimiento = self.fecha_nacimiento+" 00:00:00"
        print "##### fecha_actual >>>> ",fecha_actual
        print "#### fecha_nacimiento >>>> ",fecha_nacimiento
        server_dt = DEFAULT_SERVER_DATETIME_FORMAT
        fecha_actual_strp = datetime.strptime(fecha_actual,server_dt)
        fecha_nacimiento_strp = datetime.strptime(fecha_nacimiento,server_dt)
        print "### fecha_actual_strp ",fecha_actual_strp
        print "### fecha_nacimiento_strp ",fecha_nacimiento_strp
        print "##### fecha_actual año >> ",fecha_actual_strp.year
        print "##### fecha_actual mes >> ",fecha_actual_strp.month
        print "##### fecha_actual dia >> ",fecha_actual_strp.day
        diff_fechas = fecha_actual_strp - fecha_nacimiento_strp
        diff_dias = diff_fechas.days
        print "### DIFERENCIA EN DIAS >> ",diff_dias

        calculo_anios = diff_dias/365
        self.edad = calculo_anios

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


class MateriaOdoo(models.Model):
    _name = 'materia.odoo'
    _description = 'Asignaturas para Estudiantes'
    
    name = fields.Many2one('product.template','Materia')
    maestro_id = fields.Many2one('profesor.odoo',
                                'Profesor')
    estudiante_id = fields.Many2one('estudiantes.odoo', 
                                    'ID Ref')
    #     precio = fields.Float('Costo', digits=(14,2), )
    precio = fields.Float('Costo', 
                    dp.get_precision('Costo Materia'))


    @api.onchange('name')
    def actualizar_costo_materia(self):
        context = self._context
        print "###### actualizar_costo_materia >>"
        print "###### CONTEXT >>>> ",context
        list_price = self.name.list_price
        print "##### PRECIO DE LA MATERIA >>> ",list_price
        self.precio = list_price
        #self.write({'precio':list_price})

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