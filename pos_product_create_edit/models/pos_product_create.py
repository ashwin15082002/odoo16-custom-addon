# -*- coding: utf-8 -*-
import base64

from odoo import models, api


class PosProductCreate(models.Model):
    _name = 'pos.product.create'

    @api.model
    def custom(self, data, img):
        print(data)
        if (data['product_name'] and data['product_price'] and
                data['product_cost'] and data['product_categ']):
            created_product = self.env['product.product'].create({
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
        data['image_1920'] = img
        if len(data) != 0:
            product = self.env['product.product'].browse(product_id)
            product.update(data)
            return product
