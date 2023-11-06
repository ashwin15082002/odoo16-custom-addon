# -*- coding: utf-8 -*-

from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale, lazy
from odoo.addons.website_sale.controllers.main import TableCompute


class ProductVisibility(WebsiteSale):
    """inherit the website sale controller"""

    @route()
    def shop(self, page=0, category=None, search='', min_price=0.0,
             max_price=0.0, ppg=False, **post):
        res = super(ProductVisibility, self).shop(page=page, category=category,
                                                  search=search,
                                                  min_price=min_price,
                                                  max_price=max_price, ppg=ppg,
                                                  **post)

        if request.env.user.partner_id.visibility_type:
            website = request.env['website'].get_current_website()
            if ppg:
                try:
                    ppg = int(ppg)
                    post['ppg'] = ppg
                except ValueError:
                    ppg = False
            if not ppg:
                ppg = website.shop_ppg or 20
            ppr = website.shop_ppr or 4
            pricelist = request.env['product.pricelist'].browse(
                request.session.get('website_sale_current_pl'))

            if (request.env.user.partner_id.visibility_type == 'product'
                    and request.env.user.partner_id.product_ids):
                print(request.env.user.partner_id.product_ids)
                all_products = request.env.user.partner_id.product_ids

            elif (
                    request.env.user.partner_id.visibility_type == 'product_category'
                    and request.env.user.partner_id.product_cate_ids):
                print(request.env.user.partner_id.product_cate_ids)
                all_products = request.env['product.template'].search([(
                                                                       'categ_id',
                                                                       'in',
                                                                       request.env.user.partner_id.product_cate_ids.ids)])
            else:
                return res

            pager = website.pager(url='/shop', total=len(all_products),
                                  page=page, step=ppg, scope=7, url_args=post)
            offset = pager['offset']
            products = all_products[offset:offset + ppg]

            products_prices = lazy(
                lambda: products._get_sales_prices(pricelist))

            # setting the values in qcontext

            res.qcontext['bins'] = lazy(
                lambda: TableCompute().process(products, ppg, ppr))
            res.qcontext['get_product_prices'] = lambda product: lazy(
                lambda: products_prices[product.id])
            res.qcontext['ppr'] = ppr
            res.qcontext['ppg'] = ppg
            res.qcontext['pager'] = pager
            res.qcontext['products'] = products
            res.qcontext['categories'] = False
            res.qcontext['search_product'] = all_products
            res.qcontext['search_count'] = len(all_products)
            res.qcontext['products_prices'] = products_prices
            print(res.qcontext)

        return res
