from odoo import fields, models,api

class PartnerExtra(models.Model):

    _inherit = 'res.partner'


    partner_ref = fields.Char(string="Code Client")
    
    siret = fields.Char(string="SIRET")
    ape = fields.Char(string="APE")
    capital = fields.Float(string="Capital")
    partner_invoice_id = fields.Many2one('res.partner','Adresse de facturation')
    partner_adress_on_invoice_id = fields.Many2one('res.partner','Adresse a imprimer sur les factures')

    is_cheque_flotte = fields.Boolean(string = 'Chèque flotte ?')
    pourcentage_remise = fields.Float(string = 'Pourcentage de la Remise ')


    @api.model
    def create(self, values):

        max_nbr_digits = 5

        maxi_rec = self.env['sequence.partner'].search([])
        last_sequence = len(maxi_rec) + 1

        print("@@@@ Last sequence: " + str(last_sequence))

        current_nbr_digits = max_nbr_digits - len(str(last_sequence))

        code = str(int(last_sequence).zfill(current_nbr_digits)) + str(last_sequence)
        
        
        print("@@@@ Last sequence Code: " + str(code))

        values['partner_ref'] = "C" +"-"+ str(last_sequence)

        print("@@@@ Last value Code: " + str(values['partner_ref']))
        # maxi_rec.create({'sequence_id': last_sequence})

        # q= super(PartnerExtra, self).create(values) 
        # return q
        

 



    
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


class SequencePartner(models.Model):

    _name = 'sequence.partner'

    sequence_id = fields.Integer()

