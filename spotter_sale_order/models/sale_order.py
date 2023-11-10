# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SoApproval(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(string='status',
                             help='These states are visible in the status bar',
                             selection_add=[('waiting_for_approval',
                                             'Waiting for Approval'),
                                            ('approve', 'Approve'),
                                            ('approved', 'Approved'),
                                            ('sent',)])
    price_flag = fields.Boolean(
        string='It is a boolean field while the total amount greater than 25000 it will be true',
        default=False)

    @api.depends('amount_total')
    def _compute_amounts(self):
        """ supering the function and getting the value of total amount """
        super()._compute_amounts()
        amount = self.amount_total
        self.price_flag = True if amount > 25000 else False

    def button_approval_request(self):
        self.state = 'waiting_for_approval' if self.price_flag else None

    def button_approve(self):
        self.state = 'approve'

    def button_approve_2(self):
        self.state = 'approved'
        self.price_flag = False
