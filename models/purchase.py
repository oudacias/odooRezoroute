from odoo import fields, models,api


class purchase_custom(models.Model):
    _inherit = 'purhcase.order'


    # def button_confirm(self):
    #     res = super(purchase_custom, self).button_confirm()
    #     res.write('')
    #     return res 

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_new_picking_values(self):
        res = super(StockMove, self)._get_new_picking_values()

        print("TEST TEST TEST TEST MOVE LINE ID @@@@@@")
        # Pass value of note field from Sales Order to Picking
        # res.update({'note': self.group_id.sale_id.note})
        return res
