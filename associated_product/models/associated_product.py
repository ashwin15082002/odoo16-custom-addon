# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AssociatedProduct(models.Model):
    """ this class is used for inheriting res.partner (customer form) and add fields in the form to add products """
    _inherit = 'res.partner'

    multiple_products_ids = fields.Many2many('product.product', string='Multiple products')


class SaleOrder(models.Model):
    """ this class is used for inheriting sale.order and add boolean fields in the form  """
    _inherit = 'sale.order'

    add_associated = fields.Boolean(string='Add Associated')

    @api.onchange('add_associated')
    def _onchange_add_associated(self):
        """ this function is used to fetch products and add in the customer form while clicking the boolean field """

        print(self.partner_id.name, self.add_associated)

        if self.partner_id :
            if self.add_associated:
                associated_products = self.partner_id.multiple_products_ids

                print("associated_products", associated_products)
                order_lines = [fields.Command.create({
                        'product_id': product.id,
                        'product_uom_qty': 1, }) for product in associated_products]

                """below commented lines are added for my reference"""

                # for product in associated_products:
                #     order_line = fields.Command.create({
                #         'product_id': product.id,
                #         'product_uom_qty': 1, })

                    # order_lines.append(order_line)

                self.order_line = order_lines

            else:
                associated_product_ids = self.partner_id.multiple_products_ids.ids
                updated_order_line = [(0, 0, {
                            'product_id': rec.product_id.id,
                            'product_uom_qty': rec.product_uom_qty,
                        }) for rec in self.order_line if rec.product_id.id not in associated_product_ids]

                """below commented lines are added for my reference"""

                # for rec in self.order_line:
                #     if rec.product_id.id not in associated_product_ids:
                #         updated_order_line.append((0, 0, {
                #             'product_id': rec.product_id.id,
                #             'product_uom_qty': rec.product_uom_qty,
                #         }))

                self.order_line = [(5, 0, 0)]
                self.order_line = updated_order_line
                print(self.order_line.product_id.name)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.order_line = [(5, 0, 0)]
        self.add_associated = False
