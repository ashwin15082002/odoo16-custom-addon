# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'product.product'

    pos_avl_qty = fields.Integer(string='pos_avl_qty')


class PosSessionLimit(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):

        quant = self.config_id.locations.default_location_src_id.quant_ids
        print(quant)

        product = self.env['product.product'].search([])
        for j in product:
            j.pos_avl_qty = 0
        if quant:
            for i in quant:
                i.product_id.pos_avl_qty = i.quantity

        result = super()._loader_params_product_product()
        result['search_params']['fields'].extend(['pos_avl_qty'])

        return result
