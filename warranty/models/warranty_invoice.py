# -*- coding: utf-8 -*-

from odoo import fields, models


class WarrantyInvoice(models.Model):
    """ this class is used to inherit account. move and adding fields in invoice form """
    _inherit = 'account.move'

    warranty_request_ids = fields.One2many('warranty', 'invoice_id', string='Warranty Requests')
