from xmlrpc.client import Boolean
from odoo import fields, models

class Devis(models.Model):

    _inherit = 'sale.order'


    odometer = fields.Float(string="Kilometrage")

    partner_ref = fields.Char(string="Code Client")
    mobile = fields.Char(string="Tel. portable")
    phone = fields.Char(string="Tel. fixe")

    engin_id = fields.Many2one('fleet.vehicle',string="Véhicule")
    next_distri_date = fields.Date(string="Prochaine Distri.")
    next_ct_date = fields.Date(string="Prochain C.T.")
    is_central_company = fields.Boolean()
    inter_company_purchase_order_id = fields.Boolean()
    warehouse_id = fields.Many2one('stock.warehouse', string='Entrepot', domain="[('company_id', '=', company_id)]")


    is_repair_order = fields.Boolean(string="Ordre de reparation")
    user_repair_id = fields.Many2one('res.users',string="Mécanicien")
    repair_order_note = fields.Text(string="Ordre de reparation")
    recover_your_used_parts = fields.Boolean(string="Souhaitez-vous recupérer vos pieces usages")
    repair_with_re_used_parts = fields.Boolean(string="Souhaitez-vous une réparation avec des pieces de réemploi")
    is_can_change_pricelist  = fields.Boolean()
    categ_ids = fields.Many2many('crm.case.categ','devis_categ_rel','devis_id','categ_id',string="Tags")

    is_quotation_sent = fields.Boolean(string="Devis envoyé")
    date_quotation_sent = fields.Datetime(string="Devis envoyé le")
    is_invoice_sent = fields.Boolean(string="Facture envoyée")
    date_invoice_sent = fields.Datetime(string="Facture envoyée le")
    # new_campaign_id = fields.Many2one('crm.tracking.campaign',string="Campaign")
    # new_source_id = fields.Many2one('crm.tracking.source',string="Source")
    start_datetime = fields.Datetime(string="Début de réparartion")
    end_datetime = fields.Datetime(string="Fin de réparartion")
    is_client_order_ref_required = fields.Boolean(string="Référence client requise")
    invoiced = fields.Boolean(string="Payé")
    shipped = fields.Boolean(string="Livré")
    residual_sale_order_id = fields.Many2one('sale.order',string="Bon de commande reliquat")
    is_outstanding_sale = fields.Boolean(string="Vente exceptionnelle")
    
    signer_url = fields.Char(string="Signer Url")
    signer_name = fields.Char(string="Nom du signataire")
    signer_date = fields.Datetime(string="Date de signature")

    order_policy = fields.Selection([('manual','A la demande'),('picking','Sur le bon de livraison'),('prepaid','Avant livraison')], string="Créer facture")
    is_customer_account = fields.Boolean(string="Client en compte")
    customer_invoice_type = fields.Selection([('direct_invoice','Facturation Directe'),('mensual_invoice','Facturation Mensuelle'),('bi_mensual_invoice','Facturation Bi Mensuelle')],string="Type de facturation")

    payment_method_ids = fields.Many2one('pos.payment.method',string="Type de paiement")


    picking_policy = fields.Selection([
        ('direct', 'Livrer chaque article des disponible'),
        ('one', 'Livre tous les articles en une fois')],
        string='Shipping Policy', required=True, readonly=True, default='direct',
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}
        ,help="If you deliver all products at once, the delivery order will be scheduled based on the greatest ")
    





class CrmCaseCateg(models.Model):
    _name = "crm.case.categ"
    name = fields.Char(string="Nom du segemnt")

class CrmTrackingCampaign(models.Model):
    _name = "crm.tracking.campaign"
    name = fields.Char(string="Nom de la campagne")


class CrmTrackingSource(models.Model):
    _name = "crm.tracking.source"
    name = fields.Char(string="Nom de l'origine'")


class PosPaiement(models.Model):
    _inherit = "pos.payment.method"
    code = fields.Char(string="Code")
    cash_control = fields.Boolean(string="Gestion du controle de caisse")
    account_id = fields.Many2one('account.account',string="Compte de transfert interne")
    account_cash_in_id = fields.Many2one('account.account',string="Compte (Entrée de caisse))")
    account_cash_out_id = fields.Many2one('account.account',string="Compte (Sortie de caisse))")
    journal_in_id = fields.Many2one('account.journal',string="Journal (Entrée de caisse))")
    journal_out_id = fields.Many2one('account.journal',string="Journal (Sortie de caisse))")
    journal_ecart_id = fields.Many2one('account.journal',string="Journal (Ecart de caisse))")
