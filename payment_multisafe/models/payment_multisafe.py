import logging
import requests
from werkzeug import urls

from odoo import _, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('multisafe', 'multisafe')],
                            ondelete={'multisafe': 'set default'})
    multisafe_api_key = fields.Char(string="Multisafe API Key")

    def _msp_make_request(self, endpoint, data=None, method='POST'):

        self.ensure_one()
        print('api =', self.multisafe_api_key)
        endpoint = f'/v1/{endpoint.strip("/")}'
        url = urls.url_join('https://testapi.multisafepay.com/', endpoint)

        print('url == ', url)
        headers = {

            "api_key": self.multisafe_api_key,
            "Content-Type": 'application/json',
            "accept": 'application/json'
        }

        try:
            response = requests.request(method, url, json=data, headers=headers, timeout=60)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            _logger.exception("unable to communicate with Multisafe: %s", url)
            raise ValidationError("Multisafe: " + _("Could not establish the connection to the API."))
        return response.json()
