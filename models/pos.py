import string
from odoo import fields, models,api
from odoo.exceptions import ValidationError

class PosSession(models.Model):

    _inherit = 'pos.session'


    def open_sessions(self):
        self.env['pos.session'].create({'user_id': self.env.uid,
                'config_id': 1})





    def auto_close_pos_session(self):

        print("HELLO: Auto close session")

        """ Method called by scheduled actions to close currently open sessions """

        return self.search([('state', '=', 'opening_control')]).action_pos_session_closing_control()




class PosConfig(models.Model):

    _inherit = 'pos.config'
    user_id = fields.Many2one('res.users',string="Affecter Utilisateur")

    @api.onchange('user_id')
    def test_pos(self):
        if(self.user_id):
            for rec in self:
                obj =  rec.env['pos.config'].search_count([('user_id','=',rec.user_id.id)])  
                if(obj > 0):
                    rec.user_id = ""
                    raise ValidationError("Utilisateur déjà affecté à une autre caisse")
