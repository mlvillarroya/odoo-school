# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import *
from datetime import date

class student(models.Model):
     _name = 'school.student'
     _description = 'School students'

     name = fields.Char('Name', required = True)
     last_name = fields.Char(String="Last name", required = True)
     birthdate = fields.Date('Birthdate')
     id_number = fields.Char('ID', size=64, required = True)
     active = fields.Boolean('Active', default=True,
                             help="Is the student currently part of the class?")
     age = fields.Integer('Age', compute = '_age_compute')
     class_id = fields.Many2one('school.school_class')
     event_ids = fields.Many2many('school.event', string="Events")

     _sql_constraints = [('id_number_uniq', 'unique (id_number)', "Student ID already exists !")]

     @api.depends('birthdate')
     def _age_compute(self):
         today = date.today()
         for record in self:
             record.age = relativedelta(today, record.birthdate).years

class school_class(models.Model):
    _name = 'school.school_class'

    name = fields.Char('Denomination', size=64, required=True)
    grade = fields.Selection([('first','First grade'),('second','Second grade'),('third','Third grade'),('fourth','Fourth grade')], default='First')
    date_begin = fields.Date('Date begin')
    date_end = fields.Date('Date end')
    tutor_id = fields.Many2one('hr.employee', string='Tutor')
    student_ids = fields.One2many('school.student','class_id',string='Students')
    student_number = fields.Integer('Student number')
    description = fields.Text('Description')

class event(models.Model):
    _name = 'school.event'
    _order = 'datetime_begin'

    type = fields.Selection([('absence','Absence'),('delay','Delay'),('felicitation','Felicitation'),('behavior','Behavior')], default='absence')
    class_id = fields.Many2one('school.school_class','Class')
    datetime_begin = fields.Datetime('Datetime', default=fields.datetime.now())
    student_ids = fields.Many2many('school.student', string='Students')
    description = fields.Text('Description')
    teacher_id = fields.Many2one('hr.employee',string="Teacher")

    def name_get(self):
        result = []
        for record in self:
            name = '(' + record.class_id.name + ') ' + record.type
            result.append((record.id, name))
        return result