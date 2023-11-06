# -*- coding: utf-8 -*-

from odoo.http import Controller, request, route


class SoldProduct(Controller):
    @route(route='/product_snippet', auth='public', type='json', website=True,
           csrf=False)
    def get_product(self):

        all_product = request.env['product.template'].search_read([],
                                                                  ['id', 'name',
                                                                   'sales_count',
                                                                   'image_1920'], )
        products = sorted(all_product, key=lambda x: x['sales_count'],
                          reverse=True)

        most_view = request.env['website.track'].search_read(
            [('product_id', '!=', False)])

        for vals in most_view:
            product_id = vals['product_id'][0]
            vals['image'] = request.env['product.product'].browse(
                product_id).image_1920

        print(most_view)

        return products, most_view
