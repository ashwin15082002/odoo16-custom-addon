# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WeatherSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_module_weather = fields.Boolean(string='Weather API',
                                       config_parameter='weather.is_module_weather')

    weather_api_key = fields.Char(string='API Key',
                                  help='paste the api key here.',
                                  config_parameter='weather.weather_api_key')

    city = fields.Char(string='city',
                       config_parameter='weather.city')

    @api.model
    def custom(self):

        return {
            'api_key': self.env['ir.config_parameter'].sudo().get_param(
                'weather.weather_api_key'),
            'city': self.env['ir.config_parameter'].sudo().get_param(
                'weather.city'),
            'is_active': self.env['ir.config_parameter'].sudo().get_param(
                'weather.is_module_weather'),
        }
