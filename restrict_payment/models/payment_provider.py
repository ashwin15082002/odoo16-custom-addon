# -*- coding: utf-8 -*-

from odoo import models, fields


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    active_restrict = fields.Boolean(string='Active Restrict', help='Active for set minimum and maximum amount of restriction')
    min_amount = fields.Integer(string='Minimum Amount', help='Set Minimum Amount for restriction')
    max_amount = fields.Integer(string='Maximum Amount', help='Set Maximum Amount for restriction')
