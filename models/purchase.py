from odoo import fields, models,api


class purchase_custom(models.Model):
    _inherit = 'purchase.order'


    def button_confirm(self):
        res = super(purchase_custom, self).button_confirm()
        print("@@@@self Order: " + str(self.id))
        purchase_line = self.env['purchase.order.line'].search([('order_id','=',self.id)])

        picking_id = self.env['stock.picking'].search([('purchase_id','=',self.id)])
        picking_id.write({'location_dest_id':9})
        
        # for line in purchase_line:
        #     print('Purchase line_ids   '+ str(line.id))
        #     stock_move = self.env['stock.move'].search([('purchase_line_id','=',line.id)])
        #     print('Stock Move   '+ str(stock_move.location_dest_id))
        #     stock_move.write({'location_dest_id':9})
        #     stock_move = self.env['stock.move'].search([('purchase_line_id','=',line.id)])
        #     print('Stock Move new   '+ str(stock_move.location_dest_id))


            # stock_move_line = self.env['stock.move.line'].search([('move_id','=',stock_move.id)])
            # for line in stock_move_line:
            #     print('Stock Move  Line  '+ str(line.id))

            #     line.write({'location_dest_id':9})

            #     picking_id = self.env['stock.picking'].search([('move_id','=',stock_move.id)])
                
            #     picking_id.write({'location_dest_id':9})

            #     print('Picking line_ids   '+ str(picking_id.id))


        return res 

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_new_picking_values(self):
        res = super(StockMove, self)._get_new_picking_values()

        print("TEST TEST TEST TEST MOVE LINE ID @@@@@@")
        # Pass value of note field from Sales Order to Picking
        # res.update({'note': self.group_id.sale_id.note})
        return res
