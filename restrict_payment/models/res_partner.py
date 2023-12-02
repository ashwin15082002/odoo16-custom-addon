# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    active_restrict = fields.Boolean(string='Active Restrict', )
    providers = fields.Many2many('payment.provider', string='Payment Providers')
    min_amount = fields.Integer(string='Minimum Amount')
    max_amount = fields.Integer(string='Maximum Amount')
