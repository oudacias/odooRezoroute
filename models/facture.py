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
    