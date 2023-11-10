# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WeatherSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    weather_api_key = fields.Char(string='API Key',
                                  help='paste the api key here.',
                                  config_parameter='weather_notification.weather_api_key',
                                  store=True)

    location = fields.Char(string='Location',
                           config_parameter='weather_notification.location',
                           store=True)

    def custom_method(self):
        print('hiii')
        location= self.env['res.config.settings'].location
        print(location)
