from requests import session
from odoo import fields, models,api


class purchase_custom(models.Model):
    _inherit = 'purchase.order'
    session_id = fields.Many2one('pos.session',string="Session id")
    location_name = fields.Char(string="Emplacement")
    location_id = fields.Integer(string="Emplacement")

    is_received = fields.Boolean(compute="_isReceived")
    

    @api.model
    def create(self,vals):
        location_dest_id = self.env['pos.config'].search([('user_id','=',self.env.uid)], limit=1)
        self.location_name = location_dest_id.location_id.complete_name
        self.location_id = location_dest_id.location_id.id

        vals['location_name'] = location_dest_id.location_id.complete_name
        vals['location_id'] = location_dest_id.location_id.id



        q= super(purchase_custom, self).create(vals) 
        return q

   



    def _isReceived(self):
        
        picking_id = self.env['stock.picking'].search([('purchase_id','=',self.id)])
        if(picking_id.state == 'done'):
            self.is_received = True
        else: 
            self.is_received = False




    def button_confirm(self):
        res = super(purchase_custom, self).button_confirm()

        # location_dest_id = self.env['pos.config'].search([('user_id','=',self.env.uid)], limit=1)

        print("Location destination id: " + str(self.location_id))



        picking_id = self.env['stock.picking'].search([('purchase_id','=',self.id)])
        picking_id.write({'location_dest_id':self.location_id})

        stock_move = self.env['stock.move'].search([('picking_id','=',picking_id.id)])
        stock_move.write({'location_dest_id':self.location_id})

        
        for line in stock_move.move_line_ids:
            line.write({'location_dest_id':self.location_id})

        return res 

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_new_picking_values(self):
        res = super(StockMove, self)._get_new_picking_values()
        return res



class purchase_custom_line(models.Model):
    _inherit = 'purchase.order.line'

    @api.model
    def write(self,vals):
        self.ensure_one()
        order_id_state = self.order_id.state

        order_id = self.order_id

        

        if(order_id_state =='done' or order_id_state=='purchase'):
            for rec in order_id.order_line:
                if rec.id == self.id:
                    if(self.price_unit == rec.price_unit):

            # for line in self:

                        print("Hello Hello   "  +str(self.price_unit))
                        print("Hello Hello   "  +str(self.id))


        q= super(purchase_custom_line, self).write(vals) 
        return q


    