# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    active_limit = fields.Boolean(string='Active limit')
    limit = fields.Integer(string='Limit')


class PosSessionLimit(models.Model):
    _inherit = 'pos.session'

    def _loader_params_res_partner(self):
        result = super()._loader_params_res_partner()
        result['search_params']['fields'].extend(['active_limit', 'limit', 'credit'])
        print(result['search_params']['fields'])
        return result
