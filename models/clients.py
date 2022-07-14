from odoo import fields, models

class PartnerExtra(models.Model):

    _inherit = 'res.partner'


    partner_ref = fields.Char(string="Code Client")
    
    siret = fields.Char(string="SIRET")
    ape = fields.Char(string="APE")
    capital = fields.Float(string="Capital")
    partner_invoice_id = fields.Many2one('res.partner','Adresse de facturation')
    partner_adress_on_invoice_id = fields.Many2one('res.partner','Adresse a imprimer sur les factures')

 

