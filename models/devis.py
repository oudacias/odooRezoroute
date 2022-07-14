from odoo import fields, models

class Devis(models.Model):

    _inherit = 'sale.order'


    odometer = fields.Float(string="Kilometrage")

    partner_ref = fields.Char(string="Code Client")
    mobile = fields.Char(string="Tel. portable")
    phone = fields.Char(string="Tel. fixe")

    engin_id = fields.Many2one('fleet.vehicle',string="Vehicule")
    next_distri_date = fields.Date(string="Prochaine Distri.")
    next_ct_date = fields.Date(string="Prochain C.T.")


    is_repair_order = fields.Boolean(string="Ordre de reparation")
    repair_order_note = fields.Text(string="Ordre de reparation")
    recover_your_used_parts = fields.Boolean(string="Souhaitez-vous recuperer vos pieces usages")