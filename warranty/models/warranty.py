# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import fields, models, api


class Warranty(models.Model):
    """ this class warranty is used for sending warranty request of sold products ...only select the invoice state in posted ,
    select one product from the invoice lines , show purchase date , customer details , lot / serial number of the products """

    _name = "warranty"
    _description = "warranty"
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', readonly=True)
    date = fields.Date(string='Request Date', default=fields.Datetime.now())
    invoice_id = fields.Many2one('account.move', string='Invoice',
                                 required=True, domain="[('move_type', '=', 'out_invoice'),('state','in',['posted'])]", tracking=True)
    customer_id = fields.Many2one('res.partner',
                                  string='Customer', related='invoice_id.partner_id', tracking=True, store=True)
    purchase_date = fields.Date(string='Purchase Date', related='invoice_id.invoice_date')

    available_ids = fields.Many2many('product.product')
    product_id = fields.Many2one('product.product', string="Product", domain="[('id', 'in', available_ids),('has_warranty','=',True)]", required=True, tracking=True)

    lot_id = fields.Many2one("stock.lot", string="Lot/Serial", domain="[('product_id','=', product_id )]", tracking=True)

    warranty_expire_date = fields.Date(string='Warranty Expiry', compute='_compute_warranty_expire_date')

    state = fields.Selection(selection=[('draft', 'Draft'), ('to approve', 'To Approve'), ('approved', 'Approved'), ('received', 'Product Received'), ('done', 'Done')],
                             string='Status', copy=False, tracking=True, default='draft')
    image = fields.Image(related='product_id.image_1920')

    @api.onchange('invoice_id')
    def _available_ids(self):
        """ for fetching products from the selected invoice , and while changing the invoice -remove the product selected """

        self.available_ids = self.invoice_id.invoice_line_ids.mapped('product_id')
        self.product_id = None

    @api.model
    def create(self, vals):
        """ for creating sequence number """

        vals['name'] = self.env['ir.sequence'].next_by_code('sequence_code')
        return super(Warranty, self).create(vals)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """ used for while changing the product wanted to remove the current lot number """
        self.lot_id = None

    @api.depends('product_id')
    def _compute_warranty_expire_date(self):
        """ used to compute warranty expire date by adding purchase date and warranty periods days """
        for warranty in self:
            if warranty.product_id.has_warranty:
                warranty.warranty_expire_date = warranty.purchase_date + timedelta(days=warranty.product_id.warranty_periods)
            else:
                warranty.warranty_expire_date = None

    def button_confirm(self):
        """ while clicking the confirm button state change from draft to - to approve """
        self.write({
            'state': "to approve"
        })

    def button_approve(self):
        """ function while clicking the button approve , state change and process a stock move to warranty location """
        self.write({'state': "approved"})
        if self.state == 'approved':

            move = {
                'name': self.name,
                'product_id': self.product_id.id,
                'product_uom_qty': 1,
                'location_id': self.customer_id.property_stock_customer.id,
                'location_dest_id': self.env.ref('warranty.location_warranty').id,
                'move_line_ids': [(0, 0, {
                    'product_id': self.product_id.id,
                    'qty_done': 1,
                    'lot_id': self.lot_id.id,
                })],
                'origin': self.name
            }
            stock_move = self.env['stock.move'].create(move)
            print(stock_move.product_id.name)
            stock_move._action_confirm()
            stock_move._action_done()

            self.write({'state': 'received'})

    def button_return_product(self):
        """ function while clicking the button return , state change and process a stock move to customer location """

        move = {
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_qty': 1,
            'location_id': self.env.ref('warranty.location_warranty').id,
            'location_dest_id': self.customer_id.property_stock_customer.id,
            'move_line_ids': [(0, 0, {
                'product_id': self.product_id.id,
                'qty_done': 1,
                'lot_id': self.lot_id.id,
            })],
            'origin': self.name

        }
        stock_move = self.env['stock.move'].create(move)
        stock_move._action_confirm()
        stock_move._action_done()
        self.write({'state': "done"})

    def action_view_stock_moves(self):

        """ used to fetch the stock moves into smart tab """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock Move',
            'view_mode': 'tree',
            'res_model': 'stock.move.line',
            'domain': [('origin', '=', self.name)]
        }


