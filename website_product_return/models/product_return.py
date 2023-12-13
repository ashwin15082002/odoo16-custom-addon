# -*- coding: utf-8 -*-

from odoo import api, models


class SaleReturn(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create_picking(self, val, order_id):
        """ This functions help us to create stock picking and shown the picking in the delivery tab"""
        print(val)
        print(order_id)

        order = self.env['sale.order'].browse(order_id)

        transfer = self.env['stock.picking'].sudo().create({
            'picking_type_id': 6,
            'location_id': order.partner_id[0].property_stock_customer.id,
            'location_dest_id': self.env.ref('stock.stock_location_stock').id,
            'origin': order.name,
        })
        for i in val:
            if i['quantity'] != '0':
                transfer['move_ids'] = [(0, 0, {
                    'name': order.name,
                    'product_uom_qty': i['quantity'],
                    'product_id': i['product_id'],
                    "location_id": order.partner_id[0].property_stock_customer.id,
                    "location_dest_id": self.env.ref('stock.stock_location_stock').id,
                })]
        picking = order.picking_ids.ids
        picking.append(transfer.id)
        order.picking_ids = picking

        #==========================================================

        # print(order.read())
        # for pick in order.picking_ids:
        #     if pick.picking_type_code == 'incoming':
        #         for moves in pick.move_ids:
        #             # print(moves.read())
        #             product = moves.mapped('product_id')
        #             print(moves.mapped('product_uom_qty'))
        # return_orders =
