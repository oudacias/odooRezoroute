from odoo import fields, models,api

class SaleOrderExtra(models.Model):

    _inherit = 'sale.order'

    hide_action_picking = fields.Boolean(store=False)
    hide_action_makde_picking = fields.Boolean(store=False)
    hide_action_tecrmi = fields.Boolean(store=False)
    hide_action_processed = fields.Boolean(store=False)
    hide_action_invoice = fields.Boolean(store=False)

    account_payment_type_id = fields.Many2one('pos.payment.method',string="Type de paiement")


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



    
    def repair_order(self):
        self.write({'state':'to_prepare'})
        
        

    def sale_order_to_prepare(self):
        self.write({'state':'repair_order'})

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