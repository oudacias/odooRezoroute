import string
from urllib.parse import uses_relative
from odoo import fields, models,api
from odoo.exceptions import ValidationError

class payments_model(models.Model):
    _name ="payements"

    payment_id = fields.Many2one('account.payment')
    pos_session_id = fields.Many2one('pos.session')

    total_payment = fields.Float( )

    

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

    method_id = fields.Text(string="Méthode de Paiement", compute='_get_method_name')
    payment_id = fields.One2many('account.payment','session_id')
    payment_ids = fields.One2many('payements','pos_session_id')
    total_payment = fields.Float()

    def _get_method_name(self):
        self.method_id = self.payment_id.payment_method_line_id
        for rec in self.payment_id:
            print("Payment Method ID: 2" + str(rec.journal_id.name))
        print("@@@@@ Methode  de method_id   2 : " + str(self.method_id.name))

       




    # @api.onchange('payment_ids','write_date')
    # def total(self):
    #     print("@@@ Checking Total Payment Amount")
    #     data=[]
    #     for a in self.env('account.payment').search([]) : 
    #         total = 0
    #         for ligne in  self.pos_session_id.payment_id:
    #             if ligne.id==a.id:
    #                 total +=ligne.amount 

            
    #         data.append((0,0 ,{'payment_id':a.id,'total_payment':total})) 
    #         print (data)
    #         self.total_payment = total
    #         total=0
    #     self.write({'payment_ids':data})


    def open_sessions(self):
        self.env['pos.session'].create({'user_id': self.env.uid,
                'config_id': 1})

    def check_cash_funds(self):
        print("Checking cash_control    ids for cash_control    inline  data    in"  + str(self.id))
        self.write({'state':'closing_control'})
        

    



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

    def _compute_espece(self):
        payment_method_id = self.env['account.payment.method'].search([('code', '=', 'manual'),('payment_type', '=', 'inbound')]).ids


        print("Payment Method ID: " + str(payment_method_id))
        

        payment_ids = self.env['account.payment'].search([('payment_method_line_id', '=', payment_method_id),('session_id', '=', self.id)])
        total = 0
        
        for payment in payment_ids:

            total += payment.amount

        self.espece = total 


        # data=[(0, 0, {'payment_id': 23, 'total_payment': 2201.2}), (0, 0, {'payment_id': 22, 'total_payment': 2201.2}), (0, 0, {'payment_id': 21, 'total_payment': 2201.2})]
        # data = []
        # for ligne in  self.payment_id:
        #     total = 0
        #     for a in self.env['account.payment'].search([('session_id', '=', self.id)]) : 
        #         if ligne.journal_id.id==a.journal_id.id:
        #             total +=ligne.amount 

        #     data.append({'payment_id':a.journal_id.id,'total_payment':total})
        # res = {}
        # for v,b in data.item():
        #     res[b]=[v] if b not in res.keys() else res[b]+ v
        # self.total_payment = total
        # total=0
        # print (str(res))


        data = {}
        for ligne in  self.payment_id:
            total = 0
            for a in self.env['account.payment'].search([('session_id', '=', self.id)]) : 
                if ligne.journal_id.id==a.journal_id.id:
                    if ligne.journal_id.id in data:
                        print("@@@@ Journal: " + str(data[ligne.journal_id.id]))
                        data[ligne.journal_id.id] += float(ligne.amount)
                    else:
                        
                        data[ligne.journal_id.id] = float(ligne.amount)
                        print("@@@@ Journal:2 " + str(data[ligne.journal_id.id]))



        print(str(data))

        self.write({'payment_ids':data})



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

            self.pos_session_id.search([('id', '=', self.pos_session_id.id)]).action_pos_session_closing_control()
            return {
                'view_mode': 'kanban',
                'res_model': 'pos.config',
                # 'target' : 'new',
                'views' : [(False, 'kanban')],
                'type': 'ir.actions.act_window',
             }
            # self.pos_session_id.write({'state':'closed'})



            
        else:
            raise ValidationError("Le montant de fond de caisse est différent de la somme calculée")




# class PosSessionPaiement(models.Model):

#     name = 'pos.session.paiement'

#     method_id = fields.Many2one('account.payment.method')
#     payment_id = fields.Many2one('account.payment')



