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

    team = fields.Many2one('hr.department', string='Team')

    state = fields.Selection(string='status',
                             help='These states are visible in the status bar',
                             selection=[('waiting', 'Waiting for Approval'),
                                        ('approved', 'Approved')], default='waiting')

    def button_approve(self):
        print('hiiii')
        self.state = 'approved'
