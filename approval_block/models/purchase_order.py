# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    approval_block_id = fields.Many2one('approval.block', string='Approval Block', compute='_compute_approval_block',
                                        store=True)

    @api.depends('amount_total')
    def _compute_approval_block(self):
        total_amount = self.amount_total
        approval_block = self.approval_block_id.search([('amount_limit', '<', total_amount)], order='amount_limit desc', limit=1)
        print(approval_block)

        if approval_block:
            print(approval_block.name)
            self.approval_block_id = approval_block.id
        else:
            self.approval_block_id = False


