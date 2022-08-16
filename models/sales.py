from functools import partial
from sre_parse import State
from datetime import date
import string
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round




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

    repair_order_id = fields.One2many('order.repair.confirm','sale_order_id',string="Numéro de devis")

    invoice_compute = fields.Integer(compute="_compute_invoice_count")

    paid_check = fields.Boolean(compute="_paid_check")

    def _paid_check(self):

        if(len(self.invoice_ids) > 0):

            self.paid_check = False
        

        if(len(self.invoice_ids) == 0):
            self.paid_check = False

        elif(self.invoice_ids.payment_state == 'not_paid'):

            self.paid_check = True


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

        session = self.env['pos.session'].search([('state','=','opening_control'),('user_id','=',self.env.uid)],order="id desc", limit =1)
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
        

        if(self.is_repair_order):
            self.hide_confirm = True


    def action_confirm(self):
        print("CONFIRMATION ACTION  @@@@@@@@@@@@@  00000")
        for rec in self.order_line:
            if(rec.product_id.qty_location <= 0):
                print("ProductTemplateExtra ACTIONS: %s" % rec.product_id.qty_location)
                raise ValidationError('Quantité non disponible pour le produit ' + str(rec.product_id.name))

        for rec in self.order_line:
            if(rec.margin_percent * 100 < rec.product_id.product_tmpl_id.categ_id.marge and rec.product_id.product_tmpl_id.categ_id.marge > 0):   
                print("Margin Percentage: " + str(rec.margin_percent * 100))                
                print("Margin Percentage Product: %d" % rec.product_id.product_tmpl_id.categ_id.marge)                 
                raise ValidationError('Impossible de confirmer la commande, merci de revoir les prix')

        for rec in self.order_line:
            if(rec.margin_percent < 0):                    
                raise ValidationError('La marge du prix pour le produit ' + str(rec.product_id.name) + ' ne peut pas être négative')

        for rec in self.order_line:
            if(rec.discount > rec.product_id.product_tmpl_id.categ_id.seuil and rec.product_id.product_tmpl_id.categ_id.seuil > 0):                    
                raise ValidationError('Vous avez dépassé le seuil de la remise   ' )


            

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

        print("CONFIRMATION ACTION  @@@@@@@@@@@@@  2222")
        context = self._context.copy()
        context.pop('default_name', None)

        
        self.with_context(context)._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()

        print("CONFIRMATION ACTION  @@@@@@@@@@@@@  3333")

        # Change stock location

        picking_id = self.env['stock.picking'].search([('sale_id','=',self.id)])
        location_id = self.env['pos.config'].search([('user_id','=',self.env.uid)], limit=1)
        picking_id.write({'location_id':location_id.location_id.id})

        stock_move = self.env['stock.move'].search([('picking_id','=',picking_id.id)])
        stock_move.write({'location_id':location_id.location_id.id})

        
        for line in stock_move.move_line_ids:
            line.write({'location_id':location_id.location_id.id})
        # Change stock location -- END

        
        for rec in picking_id.move_ids_without_package:
            print("CONFIRMATION ACTION  @@@@@@@@@@@@@  4444  " +str(rec.product_uom_qty))
            rec.write({'quantity_done':rec.product_uom_qty})


        print("CONFIRMATION ACTION  @@@@@@@@@@@@@ END")

        return True




    
    def sale_order_to_prepare(self):
        self.write({'state':'to_prepare'})
        
        

    def sale_order_to_repair_order(self):
        self.hide_confirm = True
        self.write({'state':'repair_order','hide_confirm' : True})
        

    def sale_order_making(self):
        self.write({'state':'making'})

    def action_button_confirm_repair_order(self):
        # self.write({'state':'progress'})
        

        print("Engine actions should    be implemented  before  this actions    are implemented." + str(self.engin_id.id))  
        
        return {
                'res_model': 'order.repair.confirm',
                'view_mode': 'form',
                'target': 'new',
                'type': 'ir.actions.act_window',
                'views' : [(False, 'form')],
                'context' : {   
                                'default_client_id' : self.partner_id.id,
                                'default_engin_order_id' : 1,
                                'default_odometer': self.odometer,
                                'default_next_distri_date' : self.next_distri_date,
                                'default_next_ct_date' : self.next_ct_date,
                                'default_user_repair_id' : self.user_repair_id.id,
                                'default_sale_order_id' : self.id,
                            }
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
        # self.ensure_one()
        session = self.env['pos.session'].search([('state','=','opening_control'),('user_id','=',self.env.uid)],order="id desc", limit =1)


        print("ProductTemplateExtra is Available    for ProductTemplateExtra    and ProductTemplateExtra with_context   variable")

        if(len(session) == 1):
            print("ProductTemplateExtra is Available    for ProductTemplateExtra    and ProductTemplateExtra with_context   variable 2")
            
            data = []

            if(len(self.invoice_ids) == 0):

                print("ProductTemplateExtra is Available    for ProductTemplateExtra    and ProductTemplateExtra with_context   variable 3")

            
                for rec in self.order_line:
                    data.append((0,0,{  
                                    "price_unit":rec.price_unit,
                                    # "product_uom_id":rec.product_id.id,
                                    "quantity":rec.product_uom_qty,
                                    "name":rec.product_id.name,
                                    "product_id":rec.product_id.id,
                                    
                                    "sale_line_ids": [(6, 0, [rec.id])],


                                    'group_tax_id':  [(6, 0, rec.tax_id.ids)],
                                    'price_subtotal': rec.price_subtotal,
                                    'price_total': rec.price_total,
                                    'currency_id': rec.currency_id.id,
                                }))
            
                a=self.env['account.move'].create({
                            'invoice_date_due':date.today(),
                            'partner_id':self.partner_id.id, 
                            'invoice_date':date.today(),
                            # 'condition_paiment':1, 

                            # 'date_limite_paiment':line.abonnement_id.date_paiment,
                            'move_type':"out_invoice",
                            'session_id': session.id,
                            'payment_reference': self.name,

                            # 'echeance_id':line.id, 
                            # 'taux':line.abonnement_id.devis_id.taux,
                            # 'montant':line.abonnement_id.devis_id.amount_total*line.abonnement_id.devis_id.taux,
                            # 'montant_vendeur':line.abonnement_id.devis_id.amount_total,
                            "invoice_line_ids":data
                        })






                a.write({'session_id':  str(session.id)}) 
                a.write({'state':  'posted'}) 

                stock_picking = self.env['stock.picking'].search([('sale_id','=',self.id)])



                print("Product prices   ids " +str(stock_picking))
                stock_picking.move_lines._set_quantities_to_reservation()
                stock_picking.button_validate()

                
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
            elif(self.invoice_ids.payment_state == 'not_paid'):


                print("Product prices   ids TEST TEST TEST" +str(self.invoice_ids.id))
               
                return {
                    # 'name': _('Register Payment'),
                    'res_model': 'account.payment.register',
                    'view_mode': 'form',
                    'context': {
                        'active_model': 'account.move',
                        'active_ids': self.invoice_ids.id,
                    },
                    'target': 'new',
                    'type': 'ir.actions.act_window',
                }
                    

            
        else:

            raise ValidationError("Aucune caisse n'est ouverte")


class ConfirmRepairOrder(models.Model):

    _name = "order.repair.confirm"

    sale_order_id = fields.Many2one('sale.order')
    
    client_id = fields.Many2one('res.partner',string="Client")
    engin_order_id = fields.Many2one('fleet.vehicle',string="Véhicule")
    
    odometer = fields.Integer(string="Kilométrage")
    next_distri_date = fields.Date(strign="Prochaine Distri.")
    next_ct_date = fields.Date(strign="Prochaine C.T.")


    user_repair_id = fields.Many2one('res.users',string="Mécanicien")
    repair_order_note = fields.Text(string="Note de réparation")

    def confirm_order(self):

        rec =  self.env['sale.order'].search([],order="id desc", limit =1)  
        # for h in rec:
        #     h.write({'state':'sale'})

        # rec = self.env['sale.order'].search([('id','=',self.id)], limit=1)

        # sale_id = self.env['sale'].search([('id','=',self.id)], limit=1)

        # sale_id.write({'state':'progress'})
        # super(SaleOrderExtra, self.sale_order_id).action_confirm()

        for rec in self.sale_order_id.order_line:
            if(rec.product_id.qty_location <= 0):
                print("ProductTemplateExtra ACTIONS: %s" % rec.product_id.qty_location)
                raise ValidationError('Quantité non disponible pour le produit ' + str(rec.product_id.name))
            

        print("CONFIRMATION ACTION  @@@@@@@@@@@@@  1111")
        if self.sale_order_id._get_forbidden_state_confirm() & set(self.sale_order_id.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self.sale_order_id._get_forbidden_state_confirm())))

        for order in self.sale_order_id.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.sale_order_id.write(self.sale_order_id._prepare_confirmation_values())

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.

        print("CONFIRMATION ACTION  @@@@@@@@@@@@@  2222")
        context = self.sale_order_id._context.copy()
        context.pop('default_name', None)

        
        self.sale_order_id.with_context(context)._action_confirm()
        if self.sale_order_id.env.user.has_group('sale.group_auto_done_setting'):
            self.sale_order_id.action_done()

        print("CONFIRMATION ACTION  @@@@@@@@@@@@@  3333")

        # Change stock location

        picking_id = self.env['stock.picking'].search([('sale_id','=',self.sale_order_id.id)])
        location_id = self.env['pos.config'].search([('user_id','=',self.env.uid)], limit=1)
        picking_id.write({'location_id':location_id.location_id.id})

        stock_move = self.env['stock.move'].search([('picking_id','=',picking_id.id)])
        stock_move.write({'location_id':location_id.location_id.id})

        
        for line in stock_move.move_line_ids:
            line.write({'location_id':location_id.location_id.id})
        # Change stock location -- END

        
        for rec in picking_id.move_ids_without_package:
            print("CONFIRMATION ACTION  @@@@@@@@@@@@@  4444  " +str(rec.product_uom_qty))
            rec.write({'quantity_done':rec.product_uom_qty})


        print("CONFIRMATION ACTION  @@@@@@@@@@@@@ END")

        return True












        # print("Sale order CONFIRMATION SUCCESSFUL!  "  +str(self.sale_order_id))
        
        # self.sale_order_id.action_confirm()




class PaymentRegister(models.TransientModel):

    _inherit = 'account.payment.register'

    cash_amount = fields.Float(string="Montant payé")
    cash_amount_residual = fields.Float(string="Monnaie rendu")
    is_cash = fields.Boolean(string="iscash")
    cheque_titulaire = fields.Char(string="Titulaire du chèque")
    is_cheque = fields.Char(string="is_cheque")

    @api.onchange('journal_id')
    def on_journal_change(self):
        
        if(self.journal_id):
            
            if(self.journal_id.name == 'Espèces'):
                print("Changing journal_id to " + str(self.journal_id.name ))
                self.is_cash = True
                print("Changing journal_id to " + str(self.is_cash ))
            else:

                
                print("Changing journal_id to 2" + str(self.journal_id.name ))
                self.is_cash = False
                print("Changing journal_id to 2" + str(self.is_cash ))
        
        self.is_cheque = self.journal_id.name
            

    @api.onchange('cash_amount')
    def on_cash_amount(self):
        if(self.cash_amount):
            self.cash_amount_residual = self.amount - self.cash_amount