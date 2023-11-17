# -*- coding: utf-8 -*-

from odoo import models, fields


class Brand(models.Model):
    _inherit = 'product.template'

    brand = fields.Char(string='brand')

    def hp_brand(self):
        products = self.env['product.product'].search([('brand', '=', 'hp')])
        print(products)

        for product in products:
            order = {
                'product_id': product.id,
                'partner_id': 14,
                'order_line': [(0, 0, {
                    'product_id': product.id,
                    'product_qty': 1,
                })],
            }
            self.env['purchase.order'].create(order)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    brand = fields.Char(string='brand', related='product_template_id.brand')


class StockMoveLine(models.Model):
    _inherit = 'stock.move'

    brand = fields.Char(string='brand', related='sale_line_id.brand')
