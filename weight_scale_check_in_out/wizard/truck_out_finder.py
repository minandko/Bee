from odoo import models, fields
from odoo.exceptions import UserError

class TruckOutFinder(models.TransientModel):
    _name = "truck.out.finder"
    _description = "Truck Out Finder Wizard"

    truck_number = fields.Many2one('weight.scale.truck', string="Truck Number")

    date = fields.Date('Date', default=lambda self: fields.Datetime.now().date(), readonly=True)

    def find_truck(self):
        search_truck_in = self.env['truck.check.in.check.out'].search(
            [('truck_number', '=', self.truck_number.id), ('date', '=', self.date), ('check_out_weight', '=', 0)], limit=1)

        if not search_truck_in:
            raise UserError("No check in record found for truck number [{}].".format(
                self.truck_number.full_truck_number))

        context = self.env.context
        search_truck_in.dummy_check_out_weight = context.get('check_out_weight', 0)
        search_truck_in.check_out_datetime = fields.Datetime.now()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Truck OUT',
            'view_mode': 'form',
            'res_model': 'truck.check.in.check.out',
            'target': 'new',
            'views': [
                (self.env.ref('weight_scale_check_in_out.view_truck_check_in_out_form_truck_out_mode').id, 'form')],
            'res_id': search_truck_in.id,
        }
