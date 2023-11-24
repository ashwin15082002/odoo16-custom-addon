# -*- coding: utf-8 -*-

from odoo import models, fields
import xmlrpc.client


class ReportWizard(models.TransientModel):
    _name = 'fetch.po.wizard'

    odoo15_db = fields.Char(string='Odoo 15 DB Name', required=1)
    odoo15_ur = fields.Char(string='Odoo 15 Username', required=1)
    odoo15_pwd = fields.Char(string='Odoo 15 Password', required=1)
    port_15 = fields.Char(string='Odoo 15 Port', required=1)

    odoo16_pwd = fields.Char(string='Odoo 16 Password', required=1)
    port_16 = fields.Char(string='Odoo 16 Port', required=1)

    def fetch(self):
        try:
            odoo16_db = self.env.cr.dbname
            odoo16_ur = self.env.user.login

            url_15 = 'http://localhost:' + self.port_15
            url_16 = 'http://localhost:' + self.port_16

            common_15 = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/common'.format(url_15))
            common_16 = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/common'.format(url_16))

            uid_15 = common_15.authenticate(self.odoo15_db, self.odoo15_ur,
                                            self.odoo15_pwd, {})
            uid_16 = common_16.authenticate(odoo16_db, odoo16_ur,
                                            self.odoo16_pwd, {})

            models_15 = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/object'.format(url_15))
            models_16 = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/object'.format(url_16))

        except:
            raise models.ValidationError(
                "Connection to the Database failed!! \nEnter Valid details.")

        records = models_15.execute_kw(self.odoo15_db, uid_15,
                                       self.odoo15_pwd, 'purchase.order',
                                       'search_read', [], {
                                           'fields': ['name',
                                                      'partner_id',
                                                      'product_id',
                                                      'order_line',
                                                      'amount_total',
                                                      'date_order',
                                                      'state']})

        contacts_15 = models_15.execute_kw(self.odoo15_db, uid_15,
                                           self.odoo15_pwd,
                                           'res.partner', 'search_read', [],
                                           {'fields': ['id', 'name',
                                                       'email']})
        print('contacts_15==', contacts_15)

        contacts_16 = models_16.execute_kw(odoo16_db, uid_16,
                                           self.odoo16_pwd,
                                           'res.partner', 'search_read', [],
                                           {'fields': ['id', 'name',
                                                       'email']})
        print('contacts_16==', contacts_16)
        contacts = []
        for cont16 in contacts_16:
            for cont15 in contacts_15:
                if cont15['name'] != cont16['name']:
                    print('already exist')
                    contacts.append({'name': cont15['name'],
                                     'email': cont15['email']})
        result = list(
            {
                dictionary['name']: dictionary
                for dictionary in contacts
            }.values()
        )
        print(result)

        for j in contacts_16:
            for i in records:
                if j['name'] == i['partner_id'][1]:
                    contact_id = j['id']
                    models_16.execute_kw(odoo16_db, uid_16,
                                         self.odoo16_pwd,
                                         'purchase.order', 'create',
                                         [{'name': i['name'],
                                           'partner_id': contact_id,
                                           'product_id': i['product_id'][0],
                                           'amount_total': i[
                                               'amount_total'],
                                           'date_order': i['date_order'],
                                           'state': i['state'],
                                           }])
