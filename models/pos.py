from odoo import fields, models,api

class PosSession(models.Model):

    _inherit = 'pos.order'



    @api.model
    def auto_close_pos_session(self):

        """ Method called by scheduled actions to close currently open sessions """

        return self.search([('state', '=', 'opened')]).action_pos_session_closing_control()