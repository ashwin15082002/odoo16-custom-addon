# -*- coding: utf-8 -*-

from odoo import models, fields


class EmployeeTicket(models.Model):
    _name = 'employee.ticket'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Name',
                                  required=True,
                                  help='Select the employee.')
    subject = fields.Char(string='Subject',
                          help='Enter the subject')
