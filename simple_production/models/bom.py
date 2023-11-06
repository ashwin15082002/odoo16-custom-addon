# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BOM(models.Model):
    _name = 'bom.bom'
    _order = 'name desc'
    _rec_name = 'product_id'

    name = fields.Char(string='Name')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    bom_line_ids = fields.One2many('bom.line', 'bom_line_id')

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (product_id)', 'BOM for this product already exist!.')
    ]


class BomLine(models.Model):
    _name = 'bom.line'

    component_products_id = fields.Many2one('product.product', string='Components', required=1)
    qty = fields.Integer(string='Quantity', default=1)
    lot_id = fields.Many2one('stock.lot', domain="[('product_id','=', component_products_id )]")
    bom_line_id = fields.Many2one('bom.bom', string='parent')

    computed_qty = fields.Integer(string='Computed Qty')
