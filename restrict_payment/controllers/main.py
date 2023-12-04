# -*- coding: utf-8 -*-

from odoo.addons.website_sale.controllers.main import WebsiteSale


class PaymentProviders(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        res = super(PaymentProviders, self)._get_shop_payment_values(order, **kwargs)
        providers = []
        for rec in res['providers']:
            if rec.active_restrict:
                if (res['amount'] >= rec.min_amount and res['amount'] <= rec.max_amount):
                    providers.append(rec)
        res['providers'] = providers
        return res
