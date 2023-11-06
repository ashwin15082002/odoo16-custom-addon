# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):
    """ this class is used to inherit product.template and adding fields in the product form """

    _inherit = 'product.template'

    warranty_periods = fields.Integer(required=True, string="Warranty Periods (Days)", store=True)
    warranty_types = fields.Selection(string='Warranty Types',
                                      selection=[('service', 'Service Warranty'), ('replacement', 'Replacement warranty')], default='service')
    has_warranty = fields.Boolean(string='Has Warranty', store=True)