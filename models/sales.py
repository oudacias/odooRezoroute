from odoo import fields, models,api

class SaleOrderExtra(models.Model):

    _inherit = 'sale.order'

    hide_action_picking = fields.Boolean()

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



    
    def repair_order(self,vals):
        vals['state'] = 'repair_order'
        return super(SaleOrderExtra,self).write(vals)
        


    def sale_order_to_prepare(self,vals):
        vals['state'] = 'repair_order'
        return super(SaleOrderExtra,self).write(vals)