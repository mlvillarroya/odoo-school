# -*- coding: utf-8 -*-

from odoo import models, fields, api


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
     class_id = fields.Many2one('school.class')


     @api.depends('birthdate')
     def _age_compute(self):
         for record in self:
             pass

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
