# -*- coding: utf-8 -*-

from odoo import models, fields


class IdleSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    idle_timer = fields.Integer(string='Idle Timer',
                                config_parameter='idle_timer.idle_timer',
                                help='Enter the idle time in seconds.')

