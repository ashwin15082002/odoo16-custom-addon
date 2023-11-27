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
        try:

            #  -------------------------contacts--------------------------------

            contacts_15 = models_15.execute_kw(self.odoo15_db, uid_15,
                                               self.odoo15_pwd,
                                               'res.partner', 'search_read', [],
                                               {'fields': ['name',
                                                           'email']})
            print('contacts_15==', contacts_15)
            contacts_in_16 = self.env['res.partner'].search([]).mapped('name')
            print(contacts_in_16)

            for cont15 in contacts_15:
                if cont15['name'] not in contacts_in_16:
                    models_16.execute_kw(odoo16_db, uid_16,
                                         self.odoo16_pwd,
                                         'res.partner',
                                         'create', [{'name': cont15['name'],
                                                     'email': cont15['email']}])
            contacts_16 = models_16.execute_kw(odoo16_db, uid_16,
                                               self.odoo16_pwd,
                                               'res.partner', 'search_read', [],
                                               {'fields': ['name',
                                                           'email']})
            #  -------------------------products--------------------------------

            products_15 = models_15.execute_kw(self.odoo15_db, uid_15,
                                               self.odoo15_pwd,
                                               'product.product',
                                               'search_read', [])

            products_16 = self.env['product.product'].search([]).mapped('name')
            for product in products_15:
                if product['name'] not in products_16:
                    models_16.execute_kw(odoo16_db, uid_16,
                                         self.odoo16_pwd,
                                         'product.product', 'create',
                                         [{'name': product['name'],
                                           'list_price': product['list_price'],
                                           'standard_price': product[
                                               'standard_price'],
                                           'lst_price': product['lst_price'],
                                           'default_code': product[
                                               'default_code'],
                                           'detailed_type': product[
                                               'detailed_type'],
                                           'image_1920': product['image_1920'],
                                           }])

            #  ----------------------purchase order-----------------------------

            records = models_15.execute_kw(self.odoo15_db, uid_15,
                                           self.odoo15_pwd, 'purchase.order',
                                           'search_read', [], {
                                               'fields': ['name',
                                                          'partner_id',
                                                          'product_id',
                                                          'order_line',
                                                          'amount_total',
                                                          'date_order',
                                                          'date_planned',
                                                          'state']})

            orders_in_16 = self.env['purchase.order'].search([]).mapped('name')
            for i in records:
                if i['name'] not in orders_in_16:
                    for j in contacts_16:
                        if j['name'] == i['partner_id'][1]:
                            partner_id = j['id']
                            models_16.execute_kw(odoo16_db, uid_16,
                                                 self.odoo16_pwd,
                                                 'purchase.order', 'create',
                                                 [{'name': i['name'],
                                                   'partner_id': partner_id,
                                                   'amount_total': i[
                                                       'amount_total'],
                                                   'date_order': i[
                                                       'date_order'],
                                                   'state': i['state'],
                                                   'date_planned': i[
                                                       'date_planned'],
                                                   }])

            #  ---------------------purchase order line-------------------------

            order_line_in_15 = models_15.execute_kw(self.odoo15_db, uid_15,
                                                    self.odoo15_pwd,
                                                    'purchase.order.line',
                                                    'search_read', [], [])
            orders_in_16 = self.env['purchase.order'].search_read([])
            print(orders_in_16)
            products_in_16 = self.env['product.product'].search_read([])

            for line in order_line_in_15:
                for order in orders_in_16:
                    for product in products_in_16:
                        if line['product_id'][1] == product['name'] and line['order_id'][1] == order['name']:
                            models_16.execute_kw(odoo16_db, uid_16,
                                                 self.odoo16_pwd,
                                                 'purchase.order.line', 'create',
                                                 [{'name': order['name'],
                                                   'product_qty': line['product_qty'],
                                                   'product_id': product['id'],
                                                   'price_unit': line['price_unit'],
                                                   'price_subtotal': line['price_subtotal'],
                                                   'order_id': order['id'],
                                                   }])

            print(self.env['purchase.order.line'].search_read([]))

        except:
            raise models.ValidationError("Error !!.")
