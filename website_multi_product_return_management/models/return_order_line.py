# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ReturnOrderLine(models.Model):
    """creating model for return order lines"""
    _name = 'return.order.line'
    _description = "return products Details"

    order_id = fields.Many2one("sale.return", string="Order",
                               help="Orders")
    product_id = fields.Many2one('product.product',
                                 string="Product Variant", required=True,
                                 help="Defines the product variant that need to"
                                      " be returned")
    product_tmpl_id = fields.Many2one('product.template',
                                      related="product_id.product_tmpl_id",
                                      store=True, string="Product",
                                      help="Product")
    quantity = fields.Float(string="Delivered Quantity", store=True,
                            help="product quantity")
    received_qty = fields.Float(string="Received Quantity",
                                help="Received quantity")
    reason = fields.Text("Reason", help="Reason for returning the product")
    to_refund = fields.Boolean(string='Update SO/PO Quantity',
                               help='Trigger a decrease of the'
                                    ' delivered/received quantity in the '
                                    'associated Sale Order/Purchase Order')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """ setting up domain for products as per the products in the
         vendor price list"""
        self.ensure_one()
        if self._context.get('order_id'):
            order_id = self.env['sale.order'].browse(
                self._context.get('order_id'))
            products = order_id.order_line.mapped('product_id').ids
            if self.product_id:
                dqty = sum(
                    order_id.order_line.filtered(
                        lambda p: p.product_id == self.product_id).mapped(
                        'qty_delivered'))
                self.quantity = dqty
            return {'domain': {'product_id': [('id', 'in', products)]}}
