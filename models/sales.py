from odoo import fields, models,api

class SaleOrderExtra(models.Model):

    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('repair_order','Réparation en cours'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')



    
    def repair_order(self,vals):
        vals['state'] = 'repair_order'
        return super(SaleOrderExtra,self).write(vals)
        