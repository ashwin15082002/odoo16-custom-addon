# -*- coding: utf-8 -*-

from odoo import models, api


class PosProductCreate(models.Model):
    _inherit = 'product.product'

    @api.model
    def create_product(self, data, img):
        if (data['product_name'] and data['product_price'] and
                data['product_cost'] and data['product_categ']):
            created_product = self.create({
                'name': data['product_name'],
                'lst_price': data['product_price'],
                'standard_price': data['product_cost'],
                'pos_categ_id': data['product_categ'],
                'available_in_pos': True,
                'image_1920': img,
            })
            return created_product

    @api.model
    def edit_product(self, data, product_id, img):
        print(data)
        if img:
            data['image_1920'] = img
        if len(data) != 0:
            if 'pos_categ_id' in data:
                data['pos_categ_id'] = int(data['pos_categ_id'])

            product = self.browse(product_id)
            product.update(data)
            return product
        else:
            return
