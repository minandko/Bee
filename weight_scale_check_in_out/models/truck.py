from odoo import fields, models, api


class WeightScaleTruck(models.Model):
    _name = "weight.scale.truck"
    _rec_name = 'full_truck_number'

    _sql_constraints = [
        ('truck_number_unique', 'UNIQUE(prefix, suffix)',
         'Truck Number already exist.'),
    ]

    prefix = fields.Char("Truck Number Prefix", required=True)
    suffix = fields.Char("Truck Number Suffix", required=True)
    full_truck_number = fields.Char("Truck Number", compute="_compute_full_truck_number", store=True)
    customer_id = fields.Many2one('res.partner', domain=[('customer_ranking', '=', 1)])
    gate = fields.Char("Gate Name")
    driver = fields.Char("Driver")

    @api.depends('prefix', 'suffix')
    def _compute_full_truck_number(self):
        for rec in self:
            if rec.prefix and rec.suffix:
                rec.full_truck_number = rec.prefix + "/" + rec.suffix

