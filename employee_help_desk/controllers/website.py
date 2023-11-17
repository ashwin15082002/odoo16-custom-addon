# -*- coding: utf-8 -*-

from odoo.http import Controller, request, route


class EmployeeHelpDesk(Controller):
    @route(route='/helpdesk', auth='public', website=True)
    def helpdesk(self):
        print(request.env.user.name)
        employee_ids = request.env['hr.employee'].search([])
        return request.render('employee_help_desk.website_help_desk_template',
                              {'employee_ids': employee_ids})

    @route(route='/create/ticket', auth='public', website=True, csrf=False)
    def create_ticket(self, **kw):
        print("create ticket", kw)
        request.env['employee.ticket'].create({
            'employee_id': kw.get('employee'),
            'subject': kw.get('subject'),
        })
        return request.render('employee_help_desk.employee_ticket_success_template')
