# -*- coding: utf-8 -*-

from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def merge(self):
        for line in self.order_line:
            if line.id in self.order_line.ids:
                line_ids = self.order_line.filtered(
                    lambda m: m.product_id.id == line.product_id.id and line.price_unit == m.price_unit)

                quantity = sum(qty.product_uom_qty for qty in line_ids)
                # for qty in line_ids:
                #     quantity += qty.product_uom_qty
                line_ids[0].write({'product_uom_qty': quantity,
                                   'price_unit': line.price_unit,
                                   })
                line_ids[1:].unlink()

    def action_confirm(self):
        self.merge()
        super().action_confirm()

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        res.merge()
        return res
