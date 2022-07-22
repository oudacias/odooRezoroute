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

    def repair_order(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'repair_order'}, context=context)
        return True