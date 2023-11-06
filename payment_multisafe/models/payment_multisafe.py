import datetime
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
        data = {
            "order_id": 'datetime512',
            "gateway": "",
            "currency": "EUR",
            "amount": 1000,
            "description": "Test order description",
            "payment_options": {
                "notification_url": "https://www.example.com/client/notification?type=notification",
                "notification_method": "POST",
                "redirect_url": "urls.url_join(base_url, MspController._return_url",
                "cancel_url": "https://www.example.com/client/notification?type=cancel",
                "close_window": True
            },
            "customer": {
                "locale": "en_US",
                "ip_address": "123.123.123.123",
                "first_name": "John",
                "last_name": "Doe",
                "company_name": "Test Company Name",
                "address1": "Kraanspoor",
                "house_number": "39C",
                "zip_code": "1033SC",
                "city": "Amsterdam",
                "country": "US",
                "phone": "0208500500",
                "email": "jdoe@example.com",
                "referrer": "https://example.com",
                "user_agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36"
            }
        }

        try:
            response = requests.request(method, url, json=data, headers=headers, timeout=60)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            _logger.exception("unable to communicate with Multisafe: %s", url)
            raise ValidationError("Multisafe: " + _("Could not establish the connection to the API."))
        return response.json()
