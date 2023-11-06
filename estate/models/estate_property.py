from datetime import timedelta

from dateutil import relativedelta
from duplicity.tempdir import default

from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "property"
    _description = "EstateProperty"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Datetime.now() + relativedelta.relativedelta(months=3), copy=False)
    expected_price = fields.Float()
    selling_price = fields.Float(default=100, readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Garden Orientation',
        selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(string='Status',
        selection =[('new', 'New'), ('offer received', 'Offer Received'), ('east', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')], default='new', copy=False)

    property_types = fields.Many2one("property.types", string="Property Types")
    Seller = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    Buyer = fields.Many2one("res.partner", string="Buyer", copy=False)

    tags = fields.Many2many("property.tags", string="Tags")

    price_id = fields.One2many("property.offer", "property_id")
    best_offer = fields.Char(compute='_compute_best_offer')
    Total_area = fields.Float(compute="_compute_area", readonly=True)

    @api.depends('price_id.price')
    def _compute_best_offer(self):
        for best in self:
            if best.price_id:
                best.best_offer = max(best.price_id.mapped('price'))
            else:
                best.best_offer = 0

    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for line in self:
            line.Total_area = line.living_area + line.garden_area

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

class PropertyTypes(models.Model):
    _name = "property.types"
    _description = "property_types"

    name = fields.Char(required=True)


class PropertyTags(models.Model):
    _name = "property.tags"
    _description = "property_tags"

    name = fields.Char(required=True)


class PropertyOffer(models.Model):
    _name = "property.offer"
    _description = "property_offer"

    price = fields.Float()
    status = fields.Selection(string="Status",
                              selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("property", required=True)
    validity = fields.Integer(default=7)
    deadline = fields.Date(string='Deadline', compute='_compute_date', inverse='_compute_inverse_date')
    @api.depends('create_date', 'validity')
    def _compute_date(self):
        for record in self:
            if record.create_date:
                record.deadline = record.create_date + timedelta(days=record.validity)

    def _compute_inverse_date(self):
        for record in self:
            if record.deadline and record.create_date:
                record.validity = (record.deadline - record.create_date.date()).days
