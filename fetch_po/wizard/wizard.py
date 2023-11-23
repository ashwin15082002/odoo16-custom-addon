# -*- coding: utf-8 -*-

from odoo import models, fields
import xmlrpc.client


class ReportWizard(models.TransientModel):
    _name = 'fetch.po.wizard'

    odoo15_db = fields.Char(string='Odoo 15 DB Name', required=1)
    odoo15_ur = fields.Char(string='Odoo 15 Username', required=1)
    odoo15_pwd = fields.Char(string='Odoo 15 Password', required=1)
    port_15 = fields.Char(string='Odoo 15 Port', required=1)

    odoo16_db = fields.Char(string='Odoo 16 DB Name', required=1)
    odoo16_ur = fields.Char(string='Odoo 16 Username', required=1)
    odoo16_pwd = fields.Char(string='Odoo 16 Password', required=1)
    port_16 = fields.Char(string='Odoo 16 Port', required=1)

    def fetch(self):
        try:
            url_15 = 'http://localhost:' + self.port_15
            common_15 = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/common'.format(url_15))
            uid_14 = common_15.authenticate(self.odoo15_db, self.odoo15_ur,
                                            self.odoo15_pwd, {})
            models_15 = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/object'.format(url_15))
            records = models_15.execute_kw(self.odoo15_db, uid_14,
                                           self.odoo15_pwd, 'purchase.order',
                                           'search_read', [], {
                                               'fields': ['name', 'partner_id',
                                                          'product_id',
                                                          'order_line',
                                                          'amount_total']})
            print(records)

            url_16 = 'http://localhost:' + self.port_16

            common_16 = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/common'.format(url_16))
            uid_15 = common_16.authenticate(self.odoo16_db, self.odoo16_ur,
                                            self.odoo16_pwd, {})
            models_16 = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/object'.format(url_16))
            for i in records:
                print(i)

                models_16.execute_kw(self.odoo16_db, uid_15, self.odoo16_pwd,
                                     'purchase.order', 'create',
                                     [{'name': i['name'],
                                       'partner_id': i['partner_id'][0],
                                       'product_id': i['product_id'][0],
                                       'amount_total': i['amount_total']
                                       }])
            return {'success': {
                'title': ("Success"),
                'message': "Successfully fetched Records."}}

        except:
            raise models.ValidationError(
                "Connection to the Database failed!! \n Enter Valid details")
