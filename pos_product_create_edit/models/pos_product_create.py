# -*- coding: utf-8 -*-
import base64

import numpy as np

from odoo import models, api
from odoo.fields import Image


class PosProductCreate(models.Model):
    _name = 'pos.product.create'

    @api.model
    def custom(self, data):
        print(data)
        # img = base64.b64decode(data['product_image'])
        # print(img)
        # with open(data['product_image'], 'rb') as image_file:
        #     print(image_file)
        # base64_bytes = base64.b64encode(data['product_image'].read())
        # print(base64_bytes)

        # base64_string = base64_bytes.decode()
        # print(base64_string)

        self.env['product.product'].create({
            'name': data['product_name'],
            'lst_price': data['product_price'],
            'standard_price': data['product_cost'],
            'pos_categ_id': data['product_categ'],
            'available_in_pos': True,
        })

