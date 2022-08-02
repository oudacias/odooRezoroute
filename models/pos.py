import string
from urllib.parse import uses_relative
from odoo import fields, models,api
from odoo.exceptions import ValidationError

class PosSession(models.Model):

    _inherit = 'pos.session'
    POS_SESSION_STATE = [
        ('opening_control', 'Opening Control'),  # method action_pos_session_open
        ('opened', 'In Progress'),               # method action_pos_session_closing_control
        ('closing_control', 'Closing Control'),  # method action_pos_session_close
        ('valider_session', 'Validée'),
        ('closed', 'Closed & Posted'),
    ]
    # bon_achat = fields.Integer(compute='_compute_bon_achat')
    # bon_promo = fields.Integer(compute='_compute_promo')
    # cb = fields.Integer(compute='_compute_cb')
    cheque = fields.Integer(compute='_compute_cheque')
    # cheque_flotte = fields.Integer(compute='_compute_cheque_flotte')
    espece = fields.Integer(compute='_compute_espece')
    # pe_arfriquia = fields.Integer(compute='_compute_tpe_arfriquia')
    # tpe_bancaire = fields.Integer(compute='_compute_tpe_bancaire')
    total_compute = fields.Integer(compute='_total_compute')


    


    def open_sessions(self):
        self.env['pos.session'].create({'user_id': self.env.uid,
                'config_id': 1})

    def check_cash_funds(self):
        print("Checking cash_control    ids for cash_control    inline  data    in"  + str(self.id))
        self.write({'state':'valider_session'})
        

    



    def auto_close_pos_session(self):
        return {
            'view_mode': 'form',
            'res_model': 'pos.session.cloture',
            'view_id': self.env.ref('ps_rezoroute.pos_fond_wizard_form').id,
            'target' : 'inline',
            'type': 'ir.actions.act_window',
            # 'active_ids': a.id,
            'context' : {'default_pos_session_id' : self.id }
        }

        # self.write({'state':'closed'})
        # print("HELLO: Auto close session    "  +str(self.id))

        """ Method called by scheduled actions to close currently open sessions """
        # return self.search([('id', '=', self.id)]).action_pos_session_closing_control()

    def _compute_espece(self):
        payment_method_id = self.env['account.payment.method'].search([('code', '=', 'manual'),('payment_type', '=', 'inbound')]).ids
        

        print("Payment Method ID: " + str(payment_method_id))

        payment_ids = self.env['account.payment'].search([('payment_method_line_id', '=', payment_method_id),('session_id', '=', self.id)])
        total = 0
        
        for payment in payment_ids:

            total += payment.amount

        self.espece = total 


    def _compute_cheque(self):
        payment_method_id = self.env['account.payment.method'].search([('code', '=', 'check_printing')]).ids

        print("Payment Method ID: " + str(payment_method_id))

        payment_ids = self.env['account.payment'].search([('payment_method_line_id', '=', payment_method_id),('session_id', '=', self.id)])
        total = 0
        
        for payment in payment_ids:

            total += payment.amount

        self.cheque = total 

    def _total_compute(self):

        for rec in self:

            total = 0

            payment_ids = self.env['account.payment'].search([('session_id', '=', self.id)])

            for payment in payment_ids:

                total += payment.amount
            
            rec.total_compute = total

    



class PosConfig(models.Model):

    _inherit = 'pos.config'
    user_id = fields.Many2one('res.users',string="Affecter Utilisateur")
    location_id = fields.Many2one('stock.location',string="Affecter Emplacement")

    total_compute = fields.Integer(compute='_total_compute')


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


    def _total_compute(self):

        for rec in self:

            total = 0

            session_ids = self.env['pos.session'].search([('config_id', '=', rec.id)]).ids       
            payment_ids = self.env['account.payment'].search([('session_id', 'in', session_ids)])

            for payment in payment_ids:

                total += payment.amount
            
            rec.total_compute = total


class PosSession(models.Model):

    _name = 'pos.session.cloture'

    pos_session_id = fields.Many2one('pos.session')
    fond_caisse = fields.Float('Fond de Caisse Espèces')

    def check_cash_funds_after(self):
        print("Checking cash funds after transaction    before" )
        if(self.fond_caisse == self.pos_session_id.espece):

            # self.pos_session_id.search([('id', '=', self.pos_session_id.id)]).action_pos_session_closing_control()
            self.pos_session_id.write({'state':'closing_control'})

            
        else:
            raise ValidationError("Le montant de fond de caisse est différent de la somme calculée")


