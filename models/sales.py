from functools import partial
from sre_parse import State
from datetime import date
import string
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError



from odoo import fields, models,api

class SaleOrderExtra(models.Model):

    _inherit = 'sale.order'

    hide_action_picking = fields.Boolean(store=False)
    hide_action_makde_picking = fields.Boolean(store=False)
    hide_action_tecrmi = fields.Boolean(store=False)
    hide_action_processed = fields.Boolean(store=False)
    hide_action_invoice = fields.Boolean(store=False)
    hide_confirm = fields.Boolean(store=True)
    hide_repair_order = fields.Boolean(store=False)

    account_payment_type_id = fields.Many2one('pos.payment.method',string="Type de paiement")
    amount_residual = fields.Float()

    session_id = fields.Many2one('pos.session',string="Session id")

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('repair_order','Réparation en cours'),
        ('to_prepare','A preparer'),
        ('making','En préparation'),
        ('prepared','Préparée'),
        ('customer_validated','Validé client'),
        ('waiting_replenishment','A réappro.'),
        ('purchase_finished','Achat effectué'),
        ('waiting_date','Attente de planification'),
        ('progress','A livrer/A facturer'),
        ('manual','A facturer'),
        ('shipping_except',"Incident d'expédition"),
        ('invoice_except','Incident de facturation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')


    @api.model
    def create(self,vals):

        session = self.env['pos.session'].search([('user_id','=',self.env.uid),('state','=','opening_control')])  
        if(len(session) == 1):

            vals['session_id'] = session.id

            q= super(SaleOrderExtra, self).create(vals) 
            return q
        else:
            raise ValidationError('Vous devez ouvrir une nouvelle session !!!!')


    @api.onchange('partner_id')
    def additional_info(self):
        if(self.partner_id):
            for rec in self:
                partner = rec.env['res.partner'].search([('id','=',rec.partner_id.id)])

                rec.mobile = partner.mobile


    @api.depends('is_repair_order')
    def hide_repair_order(self):
        
        if(self.is_repair_order and self.state == 'repair_order'):
            self.hide_confirm = True           

    @api.onchange('is_repair_order')
    def hide_repair_order(self):
        

        if(self.is_repair_order and self.state == 'repair_order'):
            self.hide_confirm = True


    def action_confirm(self):

        print("CONFIRMATION ACTION  @@@@@@@@@@@@@  1111")
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write(self._prepare_confirmation_values())

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()

        print("CONFIRMATION ACTION  @@@@@@@@@@@@@ CENTER")


        # Change stock location
        location_id = self.env['pos.config'].search([('user_id','=',self.env.uid)], limit=1)
        picking_id = self.env['stock.picking'].search([('sale_id','=',self.id)])
        picking_id.write({'location_id':location_id.id})

        stock_move = self.env['stock.move'].search([('picking_id','=',picking_id.id)])
        stock_move.write({'location_id':location_id.id})

        
        for line in stock_move.move_line_ids:
            line.write({'location_id':location_id.id})

        # Change stock location -- END

        print("CONFIRMATION ACTION  @@@@@@@@@@@@@ END")

        return True




    
    def sale_order_to_prepare(self):
        self.write({'state':'to_prepare'})
        
        

    def sale_order_to_repair_order(self):
        self.hide_confirm = True
        self.write({'state':'repair_order','hide_confirm' : True})
        # self.env['sale.order'].action_confirm()

    def sale_order_making(self):
        self.write({'state':'making'})

    def action_button_confirm_repair_order(self):
        # self.write({'state':'progress'})
        # return super(SaleOrderExtra, self).action_confirm()
        return {
                'res_model': 'order.repair.confirm',
                'view_mode': 'form',
                'target': 'new',
                'type': 'ir.actions.act_window',
                'views' : [(False, 'form')],
            }  


    def action_order_deposit(self):
        return {
            'view_mode': 'form',
            'res_model': 'order.deposit.wizard',
            'target' : 'new',
            'views' : [(False, 'form')],
            'type': 'ir.actions.act_window',
            # 'context' : {'default_partner_id' : self.id }
        }

    def create_payment_move(self):
        self.ensure_one()
        session = self.env['pos.session'].search([('user_id','=',self.env.uid),('state','=','opening_control')])  

        if(len(session) == 1):

            data = []
            
            for rec in self.order_line:
                data.append((0,0,{  
                                "price_unit":rec.price_unit,
                                # "product_uom_id":rec.product_id.id,
                                "quantity":rec.product_uom_qty,
                                "name":rec.product_id.name,"product_id":rec.product_id.id,
                                # "ref_article":rec.product_id.default_code
                            }))
        
            a=self.env['account.move'].create({
                        'invoice_date_due':date.today(),
                        'partner_id':self.partner_id.id, 
                        'invoice_date':date.today(),
                        # 'condition_paiment':1, 

                        # 'date_limite_paiment':line.abonnement_id.date_paiment,
                        'move_type':"out_invoice",
                        'session_id': '1',

                        # 'echeance_id':line.id, 
                        # 'taux':line.abonnement_id.devis_id.taux,
                        # 'montant':line.abonnement_id.devis_id.amount_total*line.abonnement_id.devis_id.taux,
                        # 'montant_vendeur':line.abonnement_id.devis_id.amount_total,
                        "invoice_line_ids":data
                    })






            a.write({'session_id':  str(session.id)}) 
            a.write({'state':  'posted'}) 

            return {
                'res_model': 'account.payment.register',
                'view_mode': 'form',
                'context': {
                    'active_model': 'account.move',
                    'active_ids': a.id,
                },
                'target': 'new',
                'type': 'ir.actions.act_window',
            }  
            # return {
            #     'view_mode': 'form',
            #     'res_model': 'account.payment.register',
            #     'target' : 'new',
            #     'views' : [(False, 'form')],
            #     'type': 'ir.actions.act_window',
            #     'context' : {'default_move_id' : a.id,'default_partner_id' : self.partner_id.id }
            #     # 'context' : {'default_partner_id' : self.partner_id.id }
            # }  

            
        else:

            raise ValidationError("Aucune caisse n'est ouverte")


class ConfirmRepairOrder(models.Model):

    _name = "order.repair.confirm"
    
    client_id = fields.Many2one('res.partner',string="Client")
    engin_id = fields.Many2one('fleet.vehicle',string="Véhicule")
    
    odometer = fields.Float(string="Kilométrage")
    next_distri_date = fields.Date(strign="Prochaine Distri.")
    next_ct_date = fields.Date(strign="Prochaine C.T.")


    user_repair_id = fields.Many2one('res.users',string="Mécanicien")
    repair_order_note = fields.Text(string="Note de réparation")


