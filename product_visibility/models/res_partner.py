# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductVisibility(models.Model):
    _inherit = 'res.partner'

    product_cate_ids = fields.Many2many('product.category',
                                        string='Product Category')
    product_ids = fields.Many2many('product.template', string='Products')
    visibility_type = fields.Selection(string="Type",
                                       default='product',
                                       required=True,
                                       selection=[
                                           ('product', "Product"),
                                           ('product_category', "Product Category")],
                                       )

