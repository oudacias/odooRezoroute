from odoo import fields, models,api

class AcoountMoveExtra(models.Model):

    _inherit = 'account.move'
    session_id = fields.Many2one('pos.session',string="Session id")

    @api.model
    def create(self,vals):

        print("Creating new account")

        session = self.env['pos.session'].search([('user_id','=',self.env.uid),('state','=','opening_control')])  

        print(str(session.id))

        vals['session_id'] = session.id


        q= super(AcoountMoveExtra, self).create(vals) 
        return q


class PosData(models.Model):

    _inherit = 'pos.session'

    facture_count = fields.Integer(compute='_compute_facture_count')


    def _compute_facture_count(self):
        orders_data = self.env['account.move'].read_group([('session_id', 'in', self.ids)], ['session_id'], ['session_id'])
        sessions_data = {order_data['session_id'][0]: order_data['session_id_count'] for order_data in orders_data}
        for session in self:
            session.facture_count = sessions_data.get(session.id, 0)


    def action_view_facture(self):
        return {
            'name': _('Factures'),
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('point_of_sale.view_pos_order_tree_no_session_id').id, 'tree'),
                (self.env.ref('point_of_sale.view_pos_pos_form').id, 'form'),
                ],
            'type': 'ir.actions.act_window',
            'domain': [('session_id', 'in', self.ids)],
        }
    