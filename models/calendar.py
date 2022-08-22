from odoo import fields, models,api

class CalendarExtra(models.Model):

    _inherit = 'calendar.event'
    sale_id = fields.Many2one('sale.order',string="Commande de vente")
    engin_id = fields.Many2one('fleet.vehicle',string="Véhicule")
    calendar_count = fields.Integer(compute="_compute_calendar")

    def _compute_calendar(self):
        Calendar = self.env['calendar.event']
        for record in self:
            record.calendar_count = Calendar.search_count([('engin_id', '=', record.id)])

