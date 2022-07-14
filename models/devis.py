from xmlrpc.client import Boolean
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
    is_central_company = fields.Boolean()
    inter_company_purchase_order_id = fields.Boolean()
    warehouse_id = fields.Many2one('stock.warehouse', string='Entrepot', domain="[('company_id', '=', company_id)]")


    is_repair_order = fields.Boolean(string="Ordre de reparation")
    user_repair_id = fields.Many2one('res.users')
    repair_order_note = fields.Text(string="Ordre de reparation")
    recover_your_used_parts = fields.Boolean(string="Souhaitez-vous recuperer vos pieces usages")
    repair_with_re_used_parts = fields.Boolean(string="Souhaitez-vous")
    is_can_change_pricelist  = fields.Boolean(string="Souhaitez-vous")
    categ_ids = fields.Many2many('crm.case.categ','devis_categ_rel','devis_id','categ_id',string="Tags")

class CrmCaseCateg(models.Model):
    _name="crm.case.categ"


    name = fields.Char(string="Nom du segemnt")

