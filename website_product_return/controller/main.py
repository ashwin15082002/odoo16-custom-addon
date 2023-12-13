# -*- coding: utf-8 -*-

from odoo.http import Controller, request, route


class ProductReturn(Controller):
    @route(route='/return/product/<model("sale.order"):sale_order>', auth='public', website=True)
    def return_product(self, sale_order):
        print(sale_order)
        order_line = sale_order.order_line
        lines = [line for line in order_line]
        print(lines[0].product_id.read())
        return request.render('website_product_return.website_product_return', {'orderLines': lines})
