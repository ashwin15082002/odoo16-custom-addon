from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Many2one('res.company', string='Company',
                                   compute='_compute_company_type',
                                   required=True, )

    def _compute_company_type(self):
        print('hiiiiiii')
        for order in self:
            if not order.id:
                order.company_type = False
                continue
            order = order.with_company(order.company_id)
            order.company_type = order.id.property_company_type
