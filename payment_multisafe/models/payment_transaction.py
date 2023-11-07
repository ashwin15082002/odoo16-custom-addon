import logging
import pprint

from werkzeug import urls

from odoo import models, _
from odoo.exceptions import ValidationError

from odoo.addons.payment_multisafe.controllers.main import MspController

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)

        if self.provider_code != 'multisafe':
            return res

        payload = self._msp_prepare_payment_request_payload()
        print('payload = ', payload)
        _logger.info("sending '/payments' request for link creation:\n%s",
                     pprint.pformat(payload))
        payment_data = self.provider_id._msp_make_request('/json/orders',
                                                          data=payload)
        print('payment data = ', payment_data)

        checkout_url = payment_data['data']['payment_url']
        parsed_url = urls.url_parse(checkout_url)
        url_params = urls.url_decode(parsed_url.query)
        return {'url': checkout_url, 'url_params': url_params}

    def _msp_prepare_payment_request_payload(self):

        base_url = self.provider_id.get_base_url()
        redirect_url = urls.url_join(base_url, MspController._return_url)
        print('asihiuasiu', self.read())

        return {
            "order_id": self.id,
            "currency": self.currency_id.name,
            "amount": self.amount * 100,
            "description": self.reference,
            "payment_options": {
                "redirect_url": f'{redirect_url}?ref={self.reference}',
                "cancel_url": base_url + 'shop/payment',
                "close_window": True
            },
            "locale": self.partner_lang,
        }

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code,
                                                    notification_data)
        if provider_code != 'multisafe' or len(tx) == 1:
            return tx

        tx = self.search(
            [('reference', '=', notification_data.get('ref')),
             ('provider_code', '=', 'multisafe')])
        print(tx)
        if not tx:
            raise ValidationError("Multisafe: " + _(
                "No transaction found matching reference %s.",
                notification_data.get('ref')
            ))
        return tx

    def _process_notification_data(self, notification_data):

        super()._process_notification_data(notification_data)
        if self.provider_code != 'multisafe':
            return

        self._set_done()
