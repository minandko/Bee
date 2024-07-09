from odoo import fields, models, api

class Partner(models.Model):
    _inherit = "res.partner"

    supplier_ranking = fields.Integer(default=0, copy=False)
    customer_ranking = fields.Integer(default=0, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        search_partner_mode = self.env.context.get('res_partner_search_mode')
        is_customer = search_partner_mode == 'customer'
        is_supplier = search_partner_mode == 'supplier'
        if search_partner_mode:
            for vals in vals_list:
                if is_customer and 'customer_rank' not in vals:
                    vals['customer_ranking'] = 1
                elif is_supplier and 'supplier_rank' not in vals:
                    vals['supplier_ranking'] = 1
        return super().create(vals_list)
