import string
from odoo import fields, models,api

class PosSession(models.Model):

    _inherit = 'pos.session'


    def open_sessions(self):
        self.env['pos.session'].create({'user_id': self.env.uid,
                'config_id': 1})





    def auto_close_pos_session(self):

        print("HELLO: Auto close session")

        """ Method called by scheduled actions to close currently open sessions """

        return self.search([('state', '=', 'opening_control')]).action_pos_session_closing_control()




class UserPos(models.Model):

    _inherit = 'res.users'
    pos_id = fields.Many2one('pos.config',string="Nom du POS")

    @api.onchange('pos_id','id')
    def test_pos(self):
        if(self.pos_id):
            for rec in self:
                print("LLLL")
                print(rec.id)
                obj =  rec.env['res.users'].search_count([('pos_id','=',rec.pos_id.id),('id','=',rec.user_id.id)])  
                print(obj)
