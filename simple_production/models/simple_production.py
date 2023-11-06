# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SimpleProduction(models.Model):
    """ This class is used for creating production of products using bom and creating stock moves """
    _name = 'simple.production'
    _order = 'name desc'
    _inherit = 'mail.thread'

    name = fields.Char(string='New', default='New', readonly=True)
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True,
                                 help='Select Product for production')
    quantity = fields.Integer(string='Quantity', default=1,
                              help='select the quantity')
    bom_id = fields.Many2one('bom.bom', string='Bill Of Material',
                             domain="[('product_id','=',product_id)]",
                             required=True,
                             help='Select the bill of material wanted ')
    components_ids = fields.Many2many('bom.line', string='Components',
                                      compute='_compute_components_ids',
                                      store=True,
                                      help='Automatically fill the bill of material while selecting the bom ')

    stock_moves = fields.Many2many('stock.move')

    state = fields.Selection(
        selection=[('draft', 'Draft'), ('confirm', 'Confirmed'),
                   ('produce', 'Produced')],
        string='Status', default='draft', help='Different states ')

    @api.model
    def create(self, vals):
        """ for creating sequence number """

        vals['name'] = self.env['ir.sequence'].next_by_code(
            'sequence_product_code')
        return super(SimpleProduction, self).create(vals)

    @api.depends('bom_id')
    def _compute_components_ids(self):
        """ for collecting components from bom """
        self.components_ids = self.bom_id.mapped('bom_line_ids')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """ By changing the field product_id fetch the bom based on the product """
        self.bom_id = None
        if self.product_id:
            self.bom_id = self.env['bom.bom'].search(
                [('product_id', '=', self.product_id.id)], limit=1)

    def button_confirm(self):
        """ creating stock move of components from stock to production location  while clicking confirm button """
        for rec in self.components_ids:
            move = {
                'name': rec.component_products_id.name,
                'product_id': rec.component_products_id.id,
                'product_uom_qty': rec.computed_qty,
                'location_id': rec.env.ref('stock.stock_location_stock').id,
                'location_dest_id': rec.component_products_id.property_stock_production.id,
                'move_line_ids': [fields.Command.create({
                    'product_id': rec.component_products_id.id,
                    'qty_done': rec.computed_qty,
                    'lot_id': rec.lot_id.id,
                })],
            }
            stock_move = self.env['stock.move'].create(move)
            stock_move._action_confirm()
            stock_move._action_done()
            self.stock_moves = [fields.Command.link(stock_move.id)]

        self.write({'state': 'confirm'})

    def button_produce(self):
        """ creating stock move of product from production to stock location  while clicking confirm button """

        move = {
            'name': self.name,
            'product_id': self.product_id.id,

            'product_uom_qty': self.quantity,
            'location_id': self.product_id.property_stock_production.id,
            'location_dest_id': self.env.ref('stock.stock_location_stock').id,
            'move_line_ids': [fields.Command.create({
                'product_id': self.product_id.id,
                'qty_done': self.quantity,

            })],
        }
        stock_move = self.env['stock.move'].create(move)
        self.stock_moves = [fields.Command.link(stock_move.id)]
        stock_move._action_confirm()
        stock_move._action_done()

        self.write({'state': 'produce'})

    def action_view_stock_moves(self):
        """ used to fetch the stock moves into smart tab """

        tree_view_ref = self.env.ref('stock.view_move_tree')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock Move',
            'view_mode': 'tree',
            'res_model': 'stock.move',
            'domain': [('id', 'in', self.stock_moves.ids)],
            'views': [(tree_view_ref.id, 'tree')]
        }

    @api.onchange('quantity', 'bom_id')
    def _onchange_quantity(self):
        """ by changing the fields quantity and bom wanted to calculate the components quantity """
        if self.bom_id and self.quantity != 0:
            for rec in self.components_ids:
                rec.computed_qty = self.quantity * rec.qty

    @api.constrains('quantity')
    def _check_quantity(self):
        """ if the production quantity = 0 raise error """
        if self.quantity == 0:
            raise models.ValidationError("Quantity must greater than zero. ")
