# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    warning = fields.Boolean()

    @api.constrains('partner_id', 'amount_total', 'partner_id.active_credit',
                    'partner_id.warning_amt', 'partner_id.blocking_amt')
    def _change_partner_id(self):

        if self.partner_id.active_credit:
            due_amount = sum(self.partner_id.invoice_ids.mapped('amount_residual'))
            print(due_amount)

            if self.partner_id.blocking_amt > due_amount:

                if self.amount_total + due_amount >= self.partner_id.blocking_amt:
                    print('block', due_amount)
                    raise models.ValidationError(
                        _("Amount greater than blocking amount."))

                elif self.amount_total + due_amount >= self.partner_id.warning_amt:
                    print('warning', due_amount)
                    self.warning = True

                else:
                    self.warning = False

            else:
                raise models.ValidationError(
                    _("Already reached the blocking limit."))
