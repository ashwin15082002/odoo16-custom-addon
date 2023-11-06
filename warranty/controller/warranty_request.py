
import datetime

from odoo.http import Controller, request, route


class WarrantyRequest(Controller):
    @route(route='/warranty', auth='public', website=True)
    def warranty(self):
        """ warranty form """
        invoice_id = request.env['account.move'].search(
            [('move_type', '=', 'out_invoice'), ('state', 'in', ['posted'])])
        product_ids = request.env['product.product'].search(
            [('has_warranty', '=', 'True')])
        date = datetime.date.today()

        lot = request.env['stock.lot'].search([])

        return request.render('warranty.warranty_request_template',
                              {'invoice_id': invoice_id,
                               'product_ids': product_ids,
                               'date': date,
                               'lot': lot,
                               })

    @route(route='/getdata', type='json', auth='user', methods=['POST'],
           website=True, csrf=False)
    def get_data(self, **kw):

        invoice_id = int(kw.get('invoice'))
        if invoice_id:
            invoice = request.env['account.move'].browse(invoice_id)
            products = invoice.invoice_line_ids.mapped('product_id')

            product_names = [{'id': rec.id, 'name': rec.name} for rec in
                             products if rec.has_warranty]
            purchase_date = invoice.invoice_date
            customer = {'id': invoice.partner_id.id,
                        'name': invoice.partner_id.name}

            return {
                'products': product_names,
                'purchase_date': purchase_date,
                'customer': customer,
            }

    @route(route='/getproductdata', type='json', auth='public',
           methods=['POST'],
           website=True, csrf=False)
    def compute_expiry_date(self, **kw):

        product_id = int(kw.get('product'))
        invoice_id = int(kw.get('invoice'))
        invoice = request.env['account.move'].browse(invoice_id)
        purchase_date = invoice.invoice_date

        if product_id != 'Select Product':
            product = request.env['product.product'].browse(product_id)
            warranty_periods = product.warranty_periods
            warranty_expiry = purchase_date + datetime.timedelta(
                days=warranty_periods)
            print(warranty_expiry)

            return {
                'warranty_expiry': warranty_expiry
            }

    @route(route='/create/warranty', auth='public', website=True, csrf=False)
    def create_warranty(self, **kw):
        product_id = kw.get('product')

        if product_id:
            warranty = request.env['warranty'].create({
                'date': kw.get('date'),
                'invoice_id': kw.get('invoice'),
                'product_id': product_id,
                'customer_id': kw.get('customer_id'),
                'purchase_date': kw.get('purchase_date'),
                'warranty_expire_date': kw.get('expiry_date'),

            })
            return request.render('warranty.website_warranty_success_template')

    @route(route='/requests', auth='public', website=True)
    def warranty_list(self):
        user_id = request.env.user.id
        warranty_requests = request.env['warranty'].search(
            [('create_uid', '=', user_id)])

        return request.render('warranty.warranty_request_list_template',
                              {
                                  'warranty_req': warranty_requests
                              })
# snippet

    @route(route='/snippet', auth='public', type='json', website=True,
           csrf=False)
    def get_warranty(self):
        warranty_ids = request.env['warranty'].search_read([], limit=6,
                                                           order='create_date desc')
        print('warranty ids = ', warranty_ids)

        return warranty_ids

    @route(route='/view/<id>', auth='public', website=True)
    def get_view(self, id):
        warranty_id = request.env['warranty'].browse(int(id ))

        return request.render('warranty.warranty_view_data',
                              {
                                  'warranty_id': warranty_id,
                              })
