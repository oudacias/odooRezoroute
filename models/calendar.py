from odoo import fields, models,api

class CalendarExtra(models.Model):

    _inherit = 'calendar.event'
    sale_id = fields.Many2one('sale.order',string="Commande de vente")
    engin_id = fields.Many2one('fleet.vehicle',string="Véhicule")

