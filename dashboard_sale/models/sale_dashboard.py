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
            res = self.get_data(start_date, end_date)
            return res
        else:
            start_date = end_date - timedelta(days=7)
            res = self.get_data(start_date, end_date)
            return res

    def get_data(self, start_date, end_date):
        sale_order = self.env['sale.order'].search(
            [('date_order', '>', start_date)])
        print(sale_order)
        quotations = len(
            sale_order.filtered(lambda quot: quot.state in ['draft', 'sent']))
        orders = sale_order.filtered(lambda quot: quot.state in ['sale'])
        revenue = round(sum(orders.mapped('amount_total')))
        average_order = round(
            ((sum(orders.mapped('amount_total'))) / len(orders)))
        # print(self.env['sale.order'].search_read([], limit=1))
        print(self.env['sale.order.line'].search_read([], limit=1))

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
            data_sales_team.append(len(sale_order.filtered(lambda data: data.team_id == teams)))

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

# ------------------------ chart for lowest products ---------------------------

        order_line = sale_order.order_line
        print([product.product_id for product in order_line])



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
        }
        return records
