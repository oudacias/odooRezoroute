from odoo import fields, models,api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class AcoountMoveExtra(models.Model):

    _inherit = 'account.move'
    session_id = fields.Many2one('pos.session',string="Session id")

    @api.model
    def create(self,vals):

        print("Creating new account")

        session = self.env['pos.session'].search([('state','=','opening_control'),('user_id','=',self.env.uid)],order="id desc", limit =1)

        print(str(session.id))

        vals['session_id'] = session.id


        q= super(AcoountMoveExtra, self).create(vals) 
        return q


class StockPickingExtra(models.Model):

    _inherit = 'stock.picking'
    session_id = fields.Many2one('pos.session',string="Session id")

    @api.model
    def create(self,vals):

        session = self.env['pos.session'].search([('state','=','opening_control'),('user_id','=',self.env.uid)],order="id desc", limit =1)
        vals['session_id'] = session.id
         
        q= super(StockPickingExtra, self).create(vals) 

        print("Sessions created successfully    for " + str(q.purchase_id.session_id.id))
        if q.purchase_id:
            q.session_id = q.purchase_id.session_id.id
        return q


    def button_validate(self):
        
        if self.purchase_id:
            self.write({'session_id':self.purchase_id.session_id.id})
        return super(StockPickingExtra, self).button_validate()

    
       
        

class RegelementExtra(models.Model):

    _inherit = 'account.payment'
    session_id = fields.Many2one('pos.session',string="Session id")

    @api.model
    def create(self,vals):

        session = self.env['pos.session'].search([('state','=','opening_control'),('user_id','=',self.env.uid)],order="id desc", limit =1)

        vals['session_id'] = session.id

        q= super(RegelementExtra, self).create(vals) 
        return q


class PosData(models.Model):

    _inherit = 'pos.session'

    facture_count = fields.Integer(compute='_compute_facture_count')
    stock_count = fields.Integer(compute='_compute_stock_count')
    sale_count = fields.Integer(compute='_compute_sale_count')  
    reglement_count = fields.Integer(compute='_compute_reglement_count')

    reglement_id = fields.One2many('account.payment','session_id')

    def _compute_facture_count(self):
        orders_data = self.env['account.move'].read_group([('session_id', 'in', self.ids),('state', '=', 'posted')], ['session_id'], ['session_id'])
        sessions_data = {order_data['session_id'][0]: order_data['session_id_count'] for order_data in orders_data}
        for session in self:
            session.facture_count = sessions_data.get(session.id, 0)


    def _compute_stock_count(self):
        orders_data = self.env['stock.picking'].read_group([('session_id', 'in', self.ids)], ['session_id'], ['session_id'])
        sessions_data = {order_data['session_id'][0]: order_data['session_id_count'] for order_data in orders_data}
        for session in self:
            session.stock_count = sessions_data.get(session.id, 0)

    def _compute_sale_count(self):
        orders_data = self.env['sale.order'].read_group([('session_id', 'in', self.ids)], ['session_id'], ['session_id'])
        sessions_data = {order_data['session_id'][0]: order_data['session_id_count'] for order_data in orders_data}
        for session in self:
            session.sale_count = sessions_data.get(session.id, 0)


    def _compute_reglement_count(self):

        orders_data = self.env['account.payment'].read_group([('session_id', 'in', self.ids)], ['session_id'], ['session_id'])
        sessions_data = {order_data['session_id'][0]: order_data['session_id_count'] for order_data in orders_data}
        for session in self:
            session.reglement_count = sessions_data.get(session.id, 0)



    def action_view_facture(self):
        return {
            # 'name': _('Factures'),
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            # 'views': [
            #     (self.env.ref('point_of_sale.view_pos_order_tree_no_session_id').id, 'tree'),
            #     (self.env.ref('point_of_sale.view_pos_pos_form').id, 'form'),
            #     ],
            'type': 'ir.actions.act_window',
            'domain': [('session_id', 'in', self.ids)],
        }
    
    def action_view_stock(self):
        return {
            # 'name': _('Factures'),
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            # 'views': [
            #     (self.env.ref('point_of_sale.view_pos_order_tree_no_session_id').id, 'tree'),
            #     (self.env.ref('point_of_sale.view_pos_pos_form').id, 'form'),
            #     ],
            'type': 'ir.actions.act_window',
            'domain': [('session_id', 'in', self.ids)],
        }
    
    def action_view_sale(self):
        return {
            # 'name': _('Factures'),
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            # 'views': [
            #     (self.env.ref('point_of_sale.view_pos_order_tree_no_session_id').id, 'tree'),
            #     (self.env.ref('point_of_sale.view_pos_pos_form').id, 'form'),
            #     ],
            'type': 'ir.actions.act_window',
            'domain': [('session_id', 'in', self.ids)],
        }
    
    def action_view_reglement(self):
        return {
            # 'name': _('Factures'),
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
            # 'views': [
            #     (self.env.ref('point_of_sale.view_pos_order_tree_no_session_id').id, 'tree'),
            #     (self.env.ref('point_of_sale.view_pos_pos_form').id, 'form'),
            #     ],
            'type': 'ir.actions.act_window',
            'domain': [('session_id', 'in', self.ids)],
        }
    