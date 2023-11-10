# -*- coding: utf-8 -*-

import base64
import datetime

from odoo import models, fields


class StockReport(models.TransientModel):
    _name = 'stock.report.wizard'

    def stock_email_with_attachment(self):
        """action to send email with stock report"""
        query = """select product_product.id, product_template.name, product_template.list_price, stock_quant.quantity
      	            from product_template
                    inner join product_product on product_product.product_tmpl_id = product_template.id
                    inner join stock_quant on stock_quant.product_id = product_product.id """
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        data = {'report': report}
        print('data == ', data)
        current_date = datetime.date.today()
        print(current_date)
        stock_report = self.env.ref('stock_report.action_report_stock')

        data_record = base64.b64encode(
            self.env['ir.actions.report'].sudo()._render_qweb_pdf(
                stock_report, data=data)[0])
        ir_values = {
            'name': "Stock Report",
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/x-pdf',
        }
        managers = self.env.ref('stock.group_stock_manager').users

        manager = [record.email for record in managers]
        data_id = self.env['ir.attachment'].sudo().create(ir_values)
        mail_template = self.env.ref(
            'stock_report.stock_report_email_template')
        mail_template.attachment_ids = [fields.Command.set(data_id.ids)]
        email_values = {
            'email_from': self.env.user.email,
            'email_to': manager[0],
            'email_cc': manager[1:],
            'subject': f'Daily Stock Report {current_date}'}
        mail_template.send_mail(self.id, email_values=email_values,
                                force_send=True)
        mail_template.attachment_ids = [fields.Command.unlink(data_id.id)]
