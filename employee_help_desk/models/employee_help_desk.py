# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.fields import Date


class EmployeeTicket(models.Model):
    _name = 'employee.ticket'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Name',
                                  required=True,
                                  help='Select the employee.')
    description = fields.Char(string='Description',
                              help='Enter the subject')

    employee_manager_id = fields.Many2one(related="employee_id.parent_id",
                                          string="Assigned To")
    email = fields.Char(related="employee_id.work_email",
                        string="Email")
    department = fields.Many2one(related="employee_id.department_id", string="Department ")

    date = fields.Date(string="Created Date", default=Date.today(),
                       readonly=True)

    category = fields.Selection([('Technical', 'Technical'),
                                 ('Personal', 'Personal'),
                                 ('Others', 'Others')],
                                string='Category', readonly=True)

    state = fields.Selection(string='status',
                             help='These states are visible in the status bar',
                             selection=[('waiting', 'Waiting'),
                                        ('closed', 'Closed')],
                             default='waiting')

    def button_approve(self):
        self.state = 'closed'
