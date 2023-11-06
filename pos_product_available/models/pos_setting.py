# -*- coding: utf-8 -*-

from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    locations = fields.Many2one('stock.picking.type', string='Location')


class PosSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    locations = fields.Many2one(related='pos_config_id.locations', string='Location', readonly=False)
