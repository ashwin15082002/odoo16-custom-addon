# -*- coding: utf-8 -*-

from odoo import models, fields, api


class IdleSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    idle_timer = fields.Integer(string='Idle Timer', default=1,
                                config_parameter='idle_timer.idle_timer')

