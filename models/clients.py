from odoo import fields, models,api
from datetime import date
from odoo.exceptions import ValidationError



class PartnerExtra(models.Model):

    _inherit = 'res.partner'

    partner_ref = fields.Char(string="Code Client")

    ice = fields.Char(string="ICE")
    
    # siret = fields.Char(string="SIRET")
    # ape = fields.Char(string="APE")
    capital = fields.Float(string="Capital")
    partner_invoice_id = fields.Many2one('res.partner','Adresse de facturation')
    partner_adress_on_invoice_id = fields.Many2one('res.partner','Adresse a imprimer sur les factures')

    is_flotte = fields.Boolean(string = 'Client flotte ?')
    pourcentage_remise = fields.Float(string = 'Pourcentage de la Remise ')

    is_repair_user = fields.Boolean(string='Mécanicien ?')

    unpaid_invoices = fields.One2many('account.move', 'partner_id',readonly=True,domain=[('invoice_date_due', '<', date.today()), ('state', '=', 'posted'), ('payment_state', '=', 'not_paid')])
    fleet_id = fields.One2many('fleet.vehicle','partner_id')

    
    @api.onchange('name')
    def upper_name(self):
        if(self.name):
            self.name = (self.name).upper()


    def get_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'id': self.id,
            },
        }

        # ref `module_name.report_id` as reference.
        return self.env.ref('ps_rezoroute.action_report_vehicle_order').report_action(self, data=data)



    @api.model_create_multi
    def create(self, values):     
        search_partner_mode = self.env.context.get('res_partner_search_mode')
        is_supplier = search_partner_mode == 'supplier'   
        
        if self.env.user.has_group('ps_rezoroute.group_gestionnaire'):
            
            if search_partner_mode:
                for vals in values: 
                    if is_supplier and 'supplier_rank' not in vals:
                        
                        raise ValidationError(
                            ('Vous ne pouvez pas créer un nouveau fournisseur'),
                        )
            
        for vals in values: 
            max_nbr_digits = 5
            if is_supplier and 'supplier_rank' not in vals:
                maxi_rec = self.env['sequence.vendor'].search([])
                last_sequence = len(maxi_rec) + 1
                current_nbr_digits = max_nbr_digits - len(str(last_sequence))

                code = str(int(last_sequence)).zfill(current_nbr_digits) 
                vals['partner_ref'] = "F" +"-"+ str(code)
               
            else:
                maxi_rec = self.env['sequence.partner'].search([])
                last_sequence = len(maxi_rec) + 1
                current_nbr_digits = max_nbr_digits - len(str(last_sequence))
                code = str(int(last_sequence)).zfill(current_nbr_digits) 
                vals['partner_ref'] = "C" +"-"+ str(code)
            
            maxi_rec.create({'sequence_id': last_sequence})

        q= super(PartnerExtra, self).create(values) 
        return q

    def write(self, values):
        search_partner_mode = self.env.context.get('res_partner_search_mode')
        is_supplier = search_partner_mode == 'supplier'   
        
        if self.env.user.has_group('ps_rezoroute.group_gestionnaire'):
            
            if search_partner_mode:
                for vals in values: 
                    if is_supplier and 'supplier_rank' not in vals:
                        
                        raise ValidationError(
                            ('Vous ne pouvez pas modifier un fournisseur'),
                        )
        else:
            return super(PartnerExtra, self).write(values)
        

 



    
    def creer_devis(self):
        self.ensure_one()
        
        return {
        'view_mode': 'form',
        'res_model': 'sale.order',
        'target' : 'self',
        'views' : [(False, 'form')],
        'type': 'ir.actions.act_window',
        'context' : {
            'default_partner_id' : self.id, 
            'default_mobile' : self.mobile, 
            'default_phone' : self.phone, 
            'default_partner_ref' : self.partner_ref,
        }
        
    }

    def creer_ordre_reparation(self):
        self.ensure_one()
        
        return {
        'view_mode': 'form',
        'res_model': 'sale.order',
        'target' : 'self',
        'views' : [(False, 'form')],
        'type': 'ir.actions.act_window',
        'context' : {
            'default_partner_id' : self.id, 
            'default_mobile' : self.mobile, 
            'default_phone' : self.phone, 
            'default_partner_ref' : self.partner_ref,
            'default_is_repair_order' : True
        }
        
    }

    def get_sale_flotte(self):
        
        return {
        'name' : 'Devis non facturés',
        'view_mode': 'tree,form',
        'res_model': 'sale.order',
        # 'target' : 'new',
        # 'views' : [(False, 'form')],
        'type': 'ir.actions.act_window',
        'context' : {
            'create' : False,
            'default_partner_id' : self.id,  
        },
        'domain' : [('partner_id','=',self.id),('invoice_status','=','to invoice')]

        
    }

    def mail_partner_invoice(self):
 
        template_id = self.env.ref('ps_rezoroute.email_template_name').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
       

class SequencePartner(models.Model):

    _name = 'sequence.partner'

    sequence_id = fields.Integer()


class SequenceVendor(models.Model):

    _name = 'sequence.vendor'

    sequence_id = fields.Integer()

