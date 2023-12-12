# -*- coding: utf-8 -*-
from odoo import fields, models


class StockPicking(models.Model):
    """Inheriting stock_picking model for validating the return order"""
    _inherit = 'stock.picking'

    return_order_id = fields.Many2one('sale.return',
                                   string='Return order',
                                   help="Shows the return order of current"
                                        " transfer")
    return_order_pick_id = fields.Many2one('sale.return',
                                        string='Return order Pick',
                                        help="Shows the return order picking"
                                             " of current return order")
    return_order_picking = fields.Boolean(string='Return order picking',
                                          help="Helps to identify delivery and"
                                               " return picking, if true the "
                                               "transfer is return picking"
                                               " else delivery")

    def button_validate(self):
        """Validating the stock picking and update the return order"""
        res = super(StockPicking, self).button_validate()
        for rec in self:
            if rec.return_order_pick_id:
                if any(line.state != 'done' for line in
                       rec.return_order_pick_id.stock_picking_ids):
                    return res
                else:
                    rec.return_order_pick_id.write({'state': 'done'})
        return res
