from odoo import models, fields, api
from odoo.exceptions import AccessError, ValidationError, UserError


class GateIpAddress(models.Model):
    _name = "gate.ip.address"

    name = fields.Char('Name', required=True)
    ip_address = fields.Char('IP Address', required=True)
    port = fields.Char('Port', required=True)
    user = fields.Many2one("res.users", "User")
    uid = fields.Integer(related='user.id')

    @api.constrains('user')
    def _unique_user(self):
        Gate = self.env['gate.ip.address']
        for rec in self:
            is_same_user = Gate.search_count([('user.id', '=', rec.user.id), ('id', '!=', rec.id)])
            if is_same_user:
                raise ValidationError("User already assigned to a Gate!")
