# -*- coding: utf-8 -*-

from odoo import models, api


class SaleReturn(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create_picking(self, kw):
        print('helloooo', kw)
        # for i in kw:
        #     order = self.env['sale.order'].browse(i['order_id'])
        #
        #     picking = self.env['stock.picking'].create({
        #         # 'name': order.name,
        #         'picking_type_id': 1,
        #         'location_id': order.partner_id[0].property_stock_customer.id,
        #         'location_dest_id': 8,
        #         'origin': order.name,
        #         'move_ids': [(0, 0, {
        #             'name': '/',
        #             'product_id': i['product_id'],
        #             'product_uom_qty': i['qty'],
        #             'location_id': order.partner_id[0].property_stock_customer.id,
        #             'location_dest_id': 8,
        #         })],
        #     })
        #     print(picking)
        #
