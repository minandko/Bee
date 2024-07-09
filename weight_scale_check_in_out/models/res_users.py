from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    gate_id = fields.Many2one('gate.ip.address', string='Gate')




