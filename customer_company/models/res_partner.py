# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Many2one('res.company', string='Company',
                                   company_dependent=True,
                                   required=True)
