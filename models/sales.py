from sre_parse import State
from datetime import date

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

        vals['session_id'] = session.id

        q= super(SaleOrderExtra, self).create(vals) 
        return q


    @api.onchange('partner_id')
    def additional_info(self):
        if(self.partner_id):
            for rec in self:
                partner = rec.env['res.partner'].search([('id','=',rec.partner_id.id)])

                rec.mobile = partner.mobile


    @api.depends('is_repair_order')
    def hide_repair_order(self):
        print("Status      @@@@@@@   "  +str(self.state))

        if(self.is_repair_order and self.state == 'repair_order'):
            self.hide_confirm = True           

    @api.onchange('is_repair_order')
    def hide_repair_order(self):
        print("Status      @@@@@@@   "  +str(self.state))

        if(self.is_repair_order and self.state == 'repair_order'):
            self.hide_confirm = True




    
    def sale_order_to_prepare(self):
        self.write({'state':'to_prepare'})
        
        

    def sale_order_to_repair_order(self):
        self.hide_confirm = True
        self.write({'state':'repair_order','hide_confirm' : True})

    def sale_order_making(self):
        self.write({'state':'making'})

    def action_button_confirm_repair_order(self):
        self.write({'state':'progress'})


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
        # account_move = self.env['account.move'].sudo().create({
        #                                     'partner_id': self.partner_id.id,
        #                                     'move_type': 'out_invoice',
        #                                     'invoice_date': date.today(),
        #                                     'journal_id': 1, 
        #                                     'state': 'draft'
        #                                 })

        data = []
        
        for rec in self.order_line:
            data.append((0,0,{  
                            "price_unit":rec.price_unit,
                            # "product_uom_id":rec.product_id.id,
                            "quantity":rec.product_uom_qty,
                            "name":rec.product_id.name,"product_id":rec.product_id.id,
                            # "ref_article":rec.product_id.default_code
                        }))

        session = self.env['pos.session'].search([('user_id','=',self.env.uid),('state','=','opened')])  

        print(self.env.uid)

        print("Session Saved: @@@££££££" + str(session.id))

       
        a=self.env['account.move'].create({
                    'invoice_date_due':date.today(),
                    'partner_id':self.partner_id.id, 
                    'invoice_date':date.today(),
                    # 'condition_paiment':1, 

                    # 'date_limite_paiment':line.abonnement_id.date_paiment,
                    'move_type':"out_invoice",
                    # 'session_id': 1,
                    # 'echeance_id':line.id, 
                    # 'taux':line.abonnement_id.devis_id.taux,
                    # 'montant':line.abonnement_id.devis_id.amount_total*line.abonnement_id.devis_id.taux,
                    # 'montant_vendeur':line.abonnement_id.devis_id.amount_total,
                    "invoice_line_ids":data
                })






        a.write({'session_id': '1'}) 

        # return {
        #     'view_mode': 'form',
        #     'res_model': 'account.payment',
        #     'target' : 'new',
        #     'views' : [(False, 'form')],
        #     'type': 'ir.actions.act_window',
        #     'context' : {'default_move_id' : account_move.id }
        # }                                               
       

