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

        