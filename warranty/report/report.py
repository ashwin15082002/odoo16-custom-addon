# -*- coding: utf-8 -*-

from odoo import api, models


class ReportWarranty(models.AbstractModel):
    _name = 'report.warranty.report_warranty'

    @api.model
    def _get_report_values(self, docids, data=None):
        print(data)
        docs = self.env['warranty'].browse(docids)

        customer_id = data.get('customer_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        product_ids = data.get('product_ids')

        query = """ select warranty.name as warranty , res_partner.name as customer , 
                    warranty.date, warranty.product_id , product_template.name::json->'en_US' as product
                    from warranty
                    join res_partner on warranty.customer_id = res_partner.id 
                    join product_product on warranty.product_id = product_product.id 
                    join product_template on product_product.product_tmpl_id = product_template.id  """

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

        if not report:
            raise models.ValidationError('No Maching Records Found')

        return {
            'data': data,
            'report': report,
        }
