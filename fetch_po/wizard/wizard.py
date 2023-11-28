# -*- coding: utf-8 -*-

from odoo import models, fields
import xmlrpc.client


class ReportWizard(models.TransientModel):
    _name = 'fetch.po.wizard'

    odoo15_db = fields.Char(string='Odoo 15 DB Name', required=1,
                            help='Enter the odoo 15 db name')
    odoo15_ur = fields.Char(string='Odoo 15 Username', required=1,
                            help='Enter the odoo 15 username')
    odoo15_pwd = fields.Char(string='Odoo 15 Password', required=1,
                             help='Enter the odoo 15 password')
    port_15 = fields.Char(string='Odoo 15 Port', required=1,
                          help='Enter the odoo 15 port number')
    odoo_url_15 = fields.Char(string='Odoo 15 URL', required=1,
                              help='Paste the odoo 15 URL')

    odoo16_pwd = fields.Char(string='Odoo 16 Password', required=1,
                             help='Enter the odoo 16 password')
    odoo_url_16 = fields.Char(string='Odoo 16 URL', required=1,
                              help='Paste the odoo 16 URL')

    port_16 = fields.Char(string='Odoo 16 Port', required=1,
                          help='Enter the odoo 16 port number')

    def fetch(self):
        try:
            odoo16_db = self.env.cr.dbname
            odoo16_ur = self.env.user.login

            url_15 = self.odoo_url_15 + ':' + self.port_15
            url_16 = self.odoo_url_16 + ':' + self.port_16

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

            contacts_15 = models_15.execute_kw(
                self.odoo15_db, uid_15, self.odoo15_pwd,
                'res.partner', 'search_read', [],
                {'fields': ['name', 'email']})

            for cont15 in contacts_15:
                contact_name_15 = cont15['name']
                contact_email_15 = cont15['email']
                contact_16 = self.env['res.partner'].search(
                    [('name', '=', contact_name_15),
                     ('email', '=', contact_email_15)])
                if not contact_16:
                    models_16.execute_kw(
                        odoo16_db, uid_16, self.odoo16_pwd,
                        'res.partner', 'create',
                        [{'name': cont15['name'],
                          'email': cont15['email']}])

            contacts_16 = models_16.execute_kw(
                odoo16_db, uid_16, self.odoo16_pwd,
                'res.partner', 'search_read', [],
                {'fields': ['name',
                            'email']})

            #  -------------------------products--------------------------------

            products_15 = models_15.execute_kw(
                self.odoo15_db, uid_15, self.odoo15_pwd,
                'product.product', 'search_read', [])

            for product in products_15:
                product_name_15 = product['display_name']
                product_code_15 = product['default_code']
                product_16 = self.env['product.product'].search(
                    [('display_name', '=', product_name_15),
                     ('default_code', '=', product_code_15)])

                if not product_16:
                    models_16.execute_kw(
                        odoo16_db, uid_16, self.odoo16_pwd,
                        'product.product', 'create',
                        [{'name': product['display_name'],
                          'display_name': product[
                              'display_name'],
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

            records = models_15.execute_kw(
                self.odoo15_db, uid_15, self.odoo15_pwd, 'purchase.order',
                'search_read', [], {'fields': ['name',
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
                            models_16.execute_kw(
                                odoo16_db, uid_16, self.odoo16_pwd,
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

            order_lines_15 = models_15.execute_kw(
                self.odoo15_db, uid_15, self.odoo15_pwd,
                'purchase.order.line',
                'search_read', [], {'fields': ['name',
                                               'order_id',
                                               'product_id',
                                               'product_qty',
                                               'price_unit',
                                               'price_subtotal']})

            for line_15 in order_lines_15:
                print(line_15)
                order_name_15 = line_15['order_id'][1]
                product_name_15 = line_15['product_id'][1]

                corresponding_order_16 = self.env['purchase.order'].search(
                    [('name', '=', order_name_15)])
                corresponding_product_16 = self.env[
                    'product.product'].search(
                    [('name', '=', product_name_15)], limit=1)

                if corresponding_order_16 and corresponding_product_16:
                    order_line_exists = self.env[
                        'purchase.order.line'].search(
                        [('order_id', '=', corresponding_order_16.id),
                         ('product_id', '=', corresponding_product_16.id)])

                    if not order_line_exists:
                        models_16.execute_kw(
                            odoo16_db, uid_16, self.odoo16_pwd,
                            'purchase.order.line',
                            'create', [{
                                'order_id': corresponding_order_16.id,
                                'product_id': corresponding_product_16.id,
                                'product_qty': line_15[
                                    'product_qty'],
                                'price_unit': line_15[
                                    'price_unit'],
                                'price_subtotal': line_15[
                                    'price_subtotal'],
                            }])

        except:
            raise models.ValidationError("Error !!.")
