# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductBrand(models.Model):
    _inherit = 'product.product'

    brand = fields.Char(string='Brand')


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'].extend(['brand'])
        # print(result['search_params']['fields'])
        return result
