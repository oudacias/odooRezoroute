from odoo import fields, models,api

class AcoountMoveExtra(models.Model):

    _inherit = 'account.move'



    def create(self,vals):

        session = self.env['pos.session'].search([('user_id','=',self.env.uid),('state','=','opening_control')])  

        vals['session_id'] = session.id.id


        q= super(AcoountMoveExtra, self).create(vals) 
        return q
    