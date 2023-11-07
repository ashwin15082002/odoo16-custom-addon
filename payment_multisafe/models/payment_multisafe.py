# -*- coding: utf-8 -*-

import logging
import requests
from werkzeug import urls

from odoo import _, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('multisafe', 'multisafe')],
                            ondelete={'multisafe': 'set default'},
                            help="Code for the provider")

    multisafe_api_key = fields.Char(string="Multisafe API Key",
                                    help="Enter the API Key")

    def _msp_make_request(self, endpoint, data=None, method='POST'):
        """ Make a request at multisafe pay endpoint."""

        self.ensure_one()
        endpoint = f'/v1/{endpoint.strip("/")}'
        url = urls.url_join('https://testapi.multisafepay.com/', endpoint)

        headers = {
            "api_key": self.multisafe_api_key,
            "Content-Type": 'application/json',
            "accept": 'application/json'
        }

        try:
            response = requests.request(method, url, json=data, headers=headers, timeout=60)
        except requests.exceptions.RequestException:
            raise ValidationError("Multisafe: " + _(
                "Could not establish the connection to the API."))
        return response.json()
