# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
from odoo.exceptions import UserError, ValidationError


class TruckCheckInCheckOut(models.Model):
    _name = "truck.check.in.check.out"
    _description = "Truck Check In Check Out History"
    _order = 'ref DESC'
    _rec_name = 'ref'

    ref = fields.Char("Ticket No", default="New")
    type = fields.Selection([('loading', 'Loading'), ('unloading', 'Unloading')], "Type", required=True)
    date = fields.Date('Date', default=lambda self: fields.Datetime.now().date(), required=True)
    check_in_datetime = fields.Datetime('Check In Datetime', default=lambda self: datetime.datetime.now(), required=True)
    check_out_datetime = fields.Datetime('Check Out Datetime')
    truck_number = fields.Many2one('weight.scale.truck', 'Truck Number')
    full_truck_number = fields.Char("Truck Number", related="truck_number.full_truck_number")

    check_in_weight = fields.Float('Check In Weight', default=0)
    check_out_weight = fields.Float('Check Out Weight', default=0)
    tare_weight = fields.Float('Tare Weight', default=0)
    gross_weight = fields.Float('Gross Weight', default=0)
    net_weight = fields.Float('Net Weight', default=0)
    dummy_check_out_weight = fields.Float('Check Out Weight')
    dummy_net_weight = fields.Float('Net weight', compute="_compute_net_weight")
    uom_id = fields.Many2one('uom.uom', 'Unit of Measure',
                             default=lambda self: self.env['uom.uom'].search([('name', '=', 'kg')], limit=1)[0])

    driver = fields.Char('Driver Name', compute="_compute_truck_number", inverse="_inverse_dummy", required=True, store=True)
    gate = fields.Char("Gate", compute="_compute_truck_number", inverse="_inverse_dummy", store=True)
    price = fields.Float('Charges')
    product_id = fields.Many2one('product.product', 'Product')
    customer_id = fields.Many2one('res.partner', 'Customer', domain=[('customer_ranking', '=', 1)],
                                  related="truck_number.customer_id", store=True)
    supplier_id = fields.Many2one('res.partner', 'Supplier', domain=[('supplier_ranking', '=', 1)])

    @api.depends('truck_number')
    def _compute_truck_number(self):
        for rec in self:
            if rec.truck_number:
                rec.driver = rec.truck_number.driver
                rec.gate = rec.truck_number.gate

    def _inverse_dummy(self):
        pass

    @api.depends_context('check_out_weight')
    @api.depends('check_in_weight', 'dummy_check_out_weight')
    def _compute_net_weight(self):
        if self.check_in_weight and self.dummy_check_out_weight:
            self.dummy_net_weight = abs(self.dummy_check_out_weight - self.check_in_weight)
            self.check_out_datetime = fields.Datetime.now()
        else:
            self.dummy_net_weight = 0

    def _validation(self, vals):
        return self.env['truck.check.in.check.out'].search(
            [('truck_number', '=', vals['truck_number']),
             ('date', '=', vals['date']),
             ('check_out_weight', '=', 0)], limit=1)

    @api.model
    def create(self, vals):
        search_truck_in = self._validation(vals)
        if search_truck_in:
            raise ValidationError("Truck Number [{}] has not checked out!".format(
                search_truck_in[0].full_truck_number
            ))
        vals['ref'] = self.env['ir.sequence'].next_by_code('truck.in.out')
        if vals['type'] == 'loading':
            vals['tare_weight'] = vals['check_in_weight']
        else:
            vals['gross_weight'] = vals['check_in_weight']
        return super(TruckCheckInCheckOut, self).create(vals)

    @api.model
    def get_form_view(self):
        return self.env.ref('weight_scale_check_in_out.view_truck_check_in_out_form_truck_in_mode').id

    def _show_success_notification(self):
        action = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'target': 'new',
            'params': {
                'type': 'success',
                'message': "Saved successfully.",
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
        return action

    def button_create(self):
        return self._show_success_notification()

    def button_write(self):
        [vals] = self.read()
        if vals['type'] == 'loading':
            vals['gross_weight'] = vals['check_out_weight'] = self.dummy_check_out_weight
        else:
            vals['tare_weight'] = vals['check_out_weight'] = self.dummy_check_out_weight
        vals['net_weight'] = self.dummy_net_weight
        vals['check_out_datetime'] = fields.Datetime.now()
        self.write(vals)
        return self._show_success_notification()

