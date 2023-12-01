# -*- coding: utf-8 -*-
from datetime import timedelta
from operator import itemgetter

from odoo import models, fields, api
from odoo.fields import Date


class SaleDashboard(models.Model):
    _name = 'sale.dashboard'

    @api.model
    def get_sale_counts(self, date=None):
        date_count = date
        end_date = Date.today()
        if date_count == '30':
            start_date = end_date - timedelta(days=30)
            res = self.get_data(start_date)
            return res
        else:
            start_date = end_date - timedelta(days=7)
            res = self.get_data(start_date)
            return res

    def get_data(self, start_date):
        sale_order = self.env['sale.order'].search(
            [('date_order', '>', start_date)])
        quotations = len(
            sale_order.filtered(lambda quot: quot.state in ['draft', 'sent']))
        orders = sale_order.filtered(lambda quot: quot.state in ['sale'])
        revenue = round(sum(orders.mapped('amount_total')))
        average_order = round(
            ((sum(orders.mapped('amount_total'))) / len(orders)))

# ------------------------- chart for sales person -----------------------------

        sales_users = sale_order.mapped('user_id')
        sales_person = [person.name for person in sales_users]
        data_sales_person = []
        for user in sales_users:
            data_sales_person.append(
                len(sale_order.filtered(lambda data: data.user_id == user)))

# -------------------------- chart for sales team ------------------------------

        sales_teams = sale_order.mapped('team_id')
        team = [team.name for team in sales_teams]
        data_sales_team = []
        for teams in sales_teams:
            data_sales_team.append(
                len(sale_order.filtered(lambda data: data.team_id == teams)))

# ------------------------ chart for top 10 customer ---------------------------

        partners = sale_order.mapped('partner_id')
        vals = []
        partner_name = []
        count_records = []
        for partner in partners:
            aa = sale_order.filtered(lambda data: data.partner_id == partner)
            vals.append({'name': partner.name, 'count': len(aa)})

        new_list = sorted(vals, key=itemgetter('count'), reverse=True)
        for items in new_list:
            partner_name.append(items['name'])
            count_records.append(items['count'])

# -------------------------- chart for products --------------------------------

        order_line = sale_order.order_line
        products = []
        for product in order_line:
            products.append(product.product_id.id)
        product_detail = []
        for product_id in list(set(products)):
            product_count = len(sale_order.order_line.filtered(
                lambda top: top.product_id.id == product_id))
            product_detail.append(
                {'name': self.env['product.product'].browse(product_id).name,
                 'count': product_count})
        #  chart for top products

        top_product = sorted(product_detail, key=itemgetter('count'),
                             reverse=True)
        top_product_name = []
        top_product_count = []
        for items in top_product[:8]:
            top_product_name.append(items['name'])
            top_product_count.append(items['count'])

        # chart for low products
        low_product = sorted(product_detail, key=itemgetter('count'))
        low_product_name = []
        low_product_count = []
        for items in low_product[:6]:
            low_product_name.append(items['name'])
            low_product_count.append(items['count'])

# ----------------------- chart for order status -------------------------------

        order_status = sale_order.mapped('state')
        order_state = []
        for status in set(order_status):
            order_state.append({'name': status,
                                'count': len(sale_order.filtered(
                                    lambda st: st.state == status))})
        state_name = []
        state_count = []
        for items in order_state:
            state_name.append(items['name'])
            state_count.append(items['count'])

# ----------------------- chart for invoice status -------------------------------

        invoice_status = orders.mapped('invoice_status')
        invoice_state = []
        for state in set(invoice_status):
            invoice_state.append({'name': state,
                                  'count': len(orders.filtered(
                                      lambda st: st.invoice_status == state))})
        invoice_state_name = []
        invoice_state_count = []
        for items in invoice_state:
            invoice_state_name.append(items['name'])
            invoice_state_count.append(items['count'])

# --------------------------- passing values -----------------------------------

        records = {
            'quotations': quotations,
            'orders': len(orders),
            'avg_order': average_order,
            'revenue': revenue,

            'sales_person': sales_person,
            'data_sales_person': data_sales_person,

            'team': team,
            'data_sales_team': data_sales_team,

            'partner_name': partner_name,
            'count_records': count_records,

            'top_product': top_product_name,
            'top_count': top_product_count,

            'low_product': low_product_name,
            'low_count': low_product_count,

            'state_name': state_name,
            'state_count': state_count,

            'invoice_state_name': invoice_state_name,
            'invoice_state_count': invoice_state_count,

        }
        return records
