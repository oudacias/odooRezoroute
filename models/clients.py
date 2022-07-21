from odoo import fields, models,api

class PartnerExtra(models.Model):

    _inherit = 'res.partner'


    partner_ref = fields.Char(string="Code Client")
    
    siret = fields.Char(string="SIRET")
    ape = fields.Char(string="APE")
    capital = fields.Float(string="Capital")
    partner_invoice_id = fields.Many2one('res.partner','Adresse de facturation')
    partner_adress_on_invoice_id = fields.Many2one('res.partner','Adresse a imprimer sur les factures')

 



    
    def creer_devis(self):
        self.ensure_one()
        
        return {
        'view_mode': 'form',
        'res_model': 'sale.order',
        'target' : 'new',
        'views' : [(False, 'form')],
        'type': 'ir.actions.act_window',
        'context' : {'default_partner_id' : self.id }
        
    }

    def creer_ordre_reparation(self):
        self.ensure_one()
        
        return {
        'view_mode': 'form',
        'res_model': 'sale.order',
        'target' : 'new',
        'views' : [(False, 'form')],
        'type': 'ir.actions.act_window',
        'context' : {'default_partner_id' : self.id , 'default_is_repair_order' : True}
        
    }


