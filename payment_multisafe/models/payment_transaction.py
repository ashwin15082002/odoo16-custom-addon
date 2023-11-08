# -*- coding: utf-8 -*-

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
        """ Override of payment to return Multisafe Pay-specific rendering values. """

        res = super()._get_specific_rendering_values(processing_values)

        if self.provider_code != 'multisafe':
            return res

        base_url = self.provider_id.get_base_url()
        redirect_url = urls.url_join(base_url, MspController._return_url)

        payload = {
            "order_id": self.id,
            "currency": self.currency_id.name,
            "amount": self.amount * 100,
            "description": self.reference,
            "locale": self.partner_lang,
            "payment_options": {
                "redirect_url": f'{redirect_url}?ref={self.reference}',
                "cancel_url": base_url + 'shop/payment',
            },
        }

        _logger.info("sending '/payments' request for link creation:\n%s",
                     pprint.pformat(payload))

        payment_data = self.provider_id._msp_make_request('/json/orders',
                                                          data=payload)

        checkout_url = payment_data['data']['payment_url']
        parsed_url = urls.url_parse(checkout_url)
        url_params = urls.url_decode(parsed_url.query)
        return {'url': checkout_url, 'url_params': url_params}

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ To get transaction based multisafe pay data ."""

        tx = super()._get_tx_from_notification_data(provider_code,
                                                    notification_data)
        if provider_code != 'multisafe' or len(tx) == 1:
            return tx
        tx = self.search(
            [('reference', '=', notification_data.get('ref')),
             ('provider_code', '=', 'multisafe')])

        if not tx:
            raise ValidationError("Multisafe: " + _(
                "No transaction found matching reference %s.",
                notification_data.get('ref')
            ))
        return tx

    def _process_notification_data(self, notification_data):
        """ Override of payment to process the transaction based on Multisafe Pay data . """

        super()._process_notification_data(notification_data)
        if self.provider_code != 'multisafe':
            return

        self._set_done()
