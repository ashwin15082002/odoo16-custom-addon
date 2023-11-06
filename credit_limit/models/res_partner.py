# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    active_credit = fields.Boolean(string='Active Credit')
    warning_amt = fields.Monetary(string='Warning Amount')
    blocking_amt = fields.Monetary(string='Blocking Amount')
