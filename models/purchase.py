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
    @api.model
    def write(self,vals):
        print("00000000000000 @@@@@@@@@@@@   Picking write write ")

        for rec in (vals['order_line']):
            print("Hello Hello")

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

        print("TEST TEST TEST TEST MOVE LINE ID @@@@@@")
        # Pass value of note field from Sales Order to Picking
        # res.update({'note': self.group_id.sale_id.note})
        return res
