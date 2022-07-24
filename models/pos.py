import string
from odoo import fields, models,api
from odoo.exceptions import ValidationError

class PosSession(models.Model):

    _inherit = 'pos.session'

    # bon_achat = fields.Integer(compute='_compute_bon_achat')
    # bon_promo = fields.Integer(compute='_compute_promo')
    # cb = fields.Integer(compute='_compute_cb')
    # cheque = fields.Integer(compute='_compute_cheque')
    # cheque_flotte = fields.Integer(compute='_compute_cheque_flotte')
    espece = fields.Integer(compute='_compute_espece')
    # pe_arfriquia = fields.Integer(compute='_compute_tpe_arfriquia')
    # tpe_bancaire = fields.Integer(compute='_compute_tpe_bancaire')



    def open_sessions(self):
        self.env['pos.session'].create({'user_id': self.env.uid,
                'config_id': 1})

    def auto_close_pos_session(self):

        print("HELLO: Auto close session    "  +self.id)

        """ Method called by scheduled actions to close currently open sessions """
        return self.search([('id', '=', self.id),('user_id', '=', self.env.uid)]).action_pos_session_closing_control()

    def _compute_espece(self):
        payment_method_id = self.env['account.payment.method'].search([('name', '=', 'Manual'),('payment_type', '=', 'inbound')]).ids
        payment_ids = self.env['account.payment'].search([('payment_method_line_id', '=', payment_method_id)])
        total = 0
        
        for payment in payment_ids:

            total += payment.amount
            
        self.espece = total 





class PosConfig(models.Model):

    _inherit = 'pos.config'
    user_id = fields.Many2one('res.users',string="Affecter Utilisateur")

    @api.onchange('user_id')
    def test_pos(self):
        if(self.user_id):
            for rec in self:
                obj =  rec.env['pos.config'].search([('user_id','=',rec.user_id.id)])  
                
                if(len(obj) > 0):
                    rec.user_id = rec.user_id.id
                    raise ValidationError("Utilisateur déjà affecté à une autre caisse")


    def open_session_cb(self):
        self.ensure_one()
        if not self.current_session_id:
            self._check_pricelists()
            self._check_company_journal()
            self._check_company_invoice_journal()
            self._check_company_payment()
            self._check_currencies()
            self._check_profit_loss_cash_journal()
            self._check_payment_method_ids()
            self.env['pos.session'].create({
                'user_id': self.env.uid,
                'config_id': self.id
            })
