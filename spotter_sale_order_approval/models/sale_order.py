# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amt_greater = fields.Boolean(string='amt_greater',
                                 help='Boolean field it will true while total amount greater than 25000 .')
    state = fields.Selection(
        selection_add=[('waiting', 'Waiting'), ('approved', 'Approved')],
        help='adding more selection fields .')

    @api.depends('amount_total')
    def _compute_amounts(self):
        super()._compute_amounts()
        amount = self.amount_total
        print(amount)
        if amount > 25000:
            self.amt_greater = True

        else:
            self.amt_greater = False

    def action_approve(self):
        print('approved')
        self.write({'state': 'waiting'})

    def action_approve_2(self):
        print('approved 2')

        self.write({'state': 'approved'})
        self.amt_greater = False

    def action_confirm(self):
        print('confirmed')
        self.amt_greater = True
        super().action_confirm()
