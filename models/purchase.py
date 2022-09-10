from requests import session
from odoo import fields, models,api
import base64



class purchase_custom(models.Model):
    _inherit = 'purchase.order'
    session_id = fields.Many2one('pos.session',string="Session id")
    location_name = fields.Char(string="Emplacement")
    location_id = fields.Integer(string="Emplacement")

    is_received = fields.Boolean(compute="_isReceived")

    def test(self):
        
        return (("Hé") )
    

    @api.model
    def create(self,vals):
        location_dest_id = self.env['pos.config'].search([('user_id','=',self.env.uid)], limit=1)
        self.location_name = location_dest_id.location_id.complete_name
        self.location_id = location_dest_id.location_id.id

        vals['location_name'] = location_dest_id.location_id.complete_name
        vals['location_id'] = location_dest_id.location_id.id
        session_id = self.env['pos.session'].search([('state','=','opening_control'),('user_id','=',self.env.uid)],order="id desc", limit =1)


        print("@@@@@@@    Session: " + str(session_id))
        vals['session_id'] = session_id.id



        q= super(purchase_custom, self).create(vals) 
        return q

   



    def _isReceived(self):
        
        picking_id = self.env['stock.picking'].search([('purchase_id','=',self.id),('state','!=','cancel')])

        print("@@@@@@@@@@@@@@@@Stock Pickings: " + str(picking_id))
        if(not picking_id):
            self.is_received = False
        
        
        for rec in picking_id:
            if(rec.state == 'done'):
                self.is_received = True
            else: 
                self.is_received = False
        print("@@@@@@@@@@@@@@@@ Stock Pickings Result: " + str(self.is_received))




    def button_confirm(self):
        res = super(purchase_custom, self).button_confirm()

        location_dest_id = self.env['pos.config'].search([('user_id','=',self.env.uid)], limit=1)




        picking_id = self.env['stock.picking'].search([('purchase_id','=',self.id),('state','!=','cancel')])

        print("@@@@@  Location destination id: " + str(picking_id))

        for rec in picking_id:

            
            rec.write({'location_dest_id':self.location_id})

            stock_move = self.env['stock.move'].search([('picking_id','=',rec.id)])
            stock_move.write({'location_dest_id':self.location_id})

        
        for line in stock_move.move_line_ids:
            line.write({'location_dest_id':self.location_id})

        super(purchase_custom, self).button_unlock()


        return res 

    # @api.multi
    # def amount_to_text(self, amount, currency='Euro'):
    #    return amount_to_text(amount, currency)


class StockMove(models.Model):
    _inherit = 'stock.move'
    confirm_price = fields.Float(string="Prix")
    

    def _get_new_picking_values(self):
        res = super(StockMove, self)._get_new_picking_values()
        return res
    



class purchase_custom_line(models.Model):
    _inherit = 'purchase.order.line'

    @api.model
    def write(self,vals):
        # self.ensure_one()
        order_id_state = self.order_id.state

        order_id = self.order_id
        if('price_unit' in vals and vals['price_unit'] != self.price_unit):

            picking_id = self.env['stock.picking'].search([('purchase_id','=',self.order_id.id),('state','!=','cancel')])

            for rec in picking_id:
                print("LocationId   @@@@@= " + str(rec.id))
                rec.action_cancel()

            self.order_id.state = 'draft'

                

               

        q= super(purchase_custom_line, self).write(vals) 
        return q


    