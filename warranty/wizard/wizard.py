# -*- coding: utf-8 -*-

import datetime
from odoo.tools import date_utils
import io
import json

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

from odoo import models, fields, api


class ReportWizard(models.TransientModel):
    """ In this model it temporarily save th datas , for getting the wizard data """
    _name = 'warranty.wizard'

    product_ids = fields.Many2many('product.product', string='Product',
                                   domain="[('has_warranty','=',True)]")
    customer = fields.Many2one('res.partner', string='Customer')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    @api.onchange('start_date', 'end_date')
    def onchange_end_date(self):
        """ while changing the start date and end date validation required for checking the end date is greater than start date"""
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise models.ValidationError(
                    "End Date cannot be lower than Start Date")

    def button_pdf(self):
        """while clicking the button pdf in the wizard this function runs get the data and calls report.action """
        data = {
            'customer': self.customer.name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'product_ids': self.product_ids.ids,
            'customer_id': self.customer.id,
        }

        print('data ===', data)
        # print(self.name, '-', self.start_date, '-', self.end_date)
        return self.env.ref('warranty.action_report_warranty').report_action(
            None, data=data)

    def button_xlsx(self):
        """while clicking the button xlsx in the wizard this function runs get the data and calls report.action """
        data = {
            'customer': self.customer.name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'product_ids': self.product_ids.ids,
            'customer_id': self.customer.id,
        }
        print(data)

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'warranty.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Product Warranty',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        print('excel')

        customer_id = data.get('customer_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        product_ids = data.get('product_ids')
        customer = data.get('customer')

        query = """ select warranty.name as warranty , res_partner.name as customer , warranty.date, 
                    warranty.product_id ,warranty.purchase_date + product_template.warranty_periods as warranty_expire_date, product_template.name::json->'en_US' as product
                            from warranty
                            join res_partner on warranty.customer_id = res_partner.id 
                            join product_product on warranty.product_id = product_product.id 
                            join product_template on product_product.product_tmpl_id = product_template.id where 1=1 """

        params = []
        if customer_id:
            query += """ and warranty.customer_id = %s """
            params.append(customer_id)

        if start_date:
            query += """ and warranty.date >= %s """
            params.append(start_date)

        if end_date:
            query += """ and warranty.date <= %s """
            params.append(end_date)

        if product_ids:
            query += """ and warranty.product_id in %s """
            params.append(tuple(product_ids))

        self.env.cr.execute(query, tuple(params))
        report = self.env.cr.dictfetchall()
        print(report)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '10px', 'align': 'right'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px', 'border': 1})
        txt = workbook.add_format(
            {'font_size': '10px', 'align': 'center', 'bold': True})
        date_style = workbook.add_format(
            {'text_wrap': True, 'num_format': 'dd-mm-yyyy', 'align': 'center'})
        heading = workbook.add_format(
            {'font_size': '11px', 'align': 'center', 'bold': True,
             'bg_color': '#FF9933'})
        filter_date = workbook.add_format(
            {'num_format': 'dd-mm-yyyy', 'font_size': '10px', 'align': 'center',
             'bold': True})
        style = workbook.add_format({'align': 'center'})

        sheet.merge_range('A2:E3', 'PRODUCT WARRANTY', head)

        sheet.write('A5', 'Print Date:', cell_format)
        sheet.write('B5', datetime.date.today(), filter_date)

        if start_date:
            sheet.write('A8', 'From Date:', cell_format)
            sheet.write('B8', start_date, txt)
        if end_date:
            sheet.write('C8', 'To Date:', cell_format)
            sheet.write('D8', end_date, txt)

        if customer and len(product_ids) == 1:
            sheet.merge_range('A2:C3', 'PRODUCT WARRANTY', head)

            sheet.write('A6', 'Customer:', cell_format)
            sheet.write('B6', customer, txt)

            sheet.write('A7', 'Product:', cell_format)
            sheet.write('B7',
                        self.env['product.product'].browse(product_ids).name,
                        txt)

            sheet.write('A10', 'Warranty', heading)
            sheet.set_column(10, 0, 30)
            sheet.write('B10', 'Requested Date', heading)
            sheet.write('C10', 'Expiry Date', heading)

            row = 11
            col = 0

            for dict in report:
                sheet.write(row, col, dict.get('warranty'), style)
                sheet.write(row, col + 1, dict.get('date'), date_style)
                sheet.write(row, col + 2, dict.get('warranty_expire_date'),
                            date_style)
                row += 1

        elif customer:
            sheet.merge_range('A2:D3', 'PRODUCT WARRANTY', head)

            sheet.write('A6', 'Customer:', cell_format)
            sheet.write('B6', customer, txt)

            sheet.write('A10', 'Warranty', heading)
            sheet.set_column(10, 0, 30)
            sheet.write('B10', 'Product', heading)
            sheet.write('C10', 'Requested Date', heading)
            sheet.write('D10', 'Expiry Date', heading)

            row = 11
            col = 0

            for dict in report:
                sheet.write(row, col, dict.get('warranty'), style)
                sheet.write(row, col + 1, dict.get('product'), style)
                sheet.write(row, col + 2, dict.get('date'), date_style)
                sheet.write(row, col + 3, dict.get('warranty_expire_date'),
                            date_style)
                row += 1

        elif len(product_ids) == 1:
            sheet.merge_range('A2:D3', 'PRODUCT WARRANTY', head)

            sheet.write('A7', 'Product:', cell_format)
            sheet.write('B7',
                        self.env['product.product'].browse(product_ids).name,
                        txt)

            sheet.write('A10', 'Warranty', heading)
            sheet.set_column(10, 0, 30)
            sheet.write('B10', 'Customer', heading)
            sheet.write('C10', 'Requested Date', heading)
            sheet.write('D10', 'Expiry Date', heading)

            row = 11
            col = 0

            for dict in report:
                sheet.write(row, col, dict.get('warranty'), style)
                sheet.write(row, col + 1, dict.get('customer'), style)
                sheet.write(row, col + 2, dict.get('date'), date_style)
                sheet.write(row, col + 3, dict.get('warranty_expire_date'),
                            date_style)
                row += 1

        else:

            sheet.write('A10', 'Warranty', heading)
            sheet.set_column(10, 0, 30)
            sheet.write('B10', 'Customer', heading)
            sheet.write('C10', 'Product', heading)
            sheet.write('D10', 'Requested Date', heading)
            sheet.write('E10', 'Expiry Date', heading)

            row = 11
            col = 0

            for dict in report:
                sheet.write(row, col, dict.get('warranty'), style)
                sheet.write(row, col + 1, dict.get('customer'), style)
                sheet.write(row, col + 2, dict.get('product'), style)
                sheet.write(row, col + 3, dict.get('date'), date_style)
                sheet.write(row, col + 4, dict.get('warranty_expire_date'),
                            date_style)
                row += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
