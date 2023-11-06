# -*- coding: utf-8 -*-

from odoo import models, fields


class ApprovalBlock(models.Model):
    """ this class is used to """
    _name = 'approval.block'
    _description = "approval_block"
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', required=True)
    amount_limit = fields.Integer(string='Amount Limit')
