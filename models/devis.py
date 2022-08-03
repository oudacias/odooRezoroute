from nis import cat
from xmlrpc.client import Boolean
from odoo import fields, models,api
from odoo.exceptions import ValidationError


class Devis(models.Model):

    _inherit = 'sale.order'


    odometer = fields.Float(string="Kilométrage")

    partner_ref = fields.Char(string="Code Client")
    mobile = fields.Char(string="Tel. portable")
    phone = fields.Char(string="Tel. fixe")

    engin_id = fields.Many2one('fleet.vehicle',string="Véhicule")
    next_distri_date = fields.Date(string="Prochaine Distri.")
    next_ct_date = fields.Date(string="Prochain C.T.")
    is_central_company = fields.Boolean()
    inter_company_purchase_order_id = fields.Boolean()
    warehouse_id = fields.Many2one('stock.warehouse', string='Entrepôt', domain="[('company_id', '=', company_id)]")


    is_repair_order = fields.Boolean(string="Ordre de reparation")
    user_repair_id = fields.Many2one('res.users',string="Mécanicien")
    repair_order_note = fields.Text(string="Note de réparation")
    recover_your_used_parts = fields.Boolean(string="Souhaitez-vous recupérer vos pièces usages")
    repair_with_re_used_parts = fields.Boolean(string="Souhaitez-vous une réparation avec des pièces de réemploi")
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
    

    manufacturer_id = fields.Many2one('engine.manufacturer','Constructeur')

    carrier_id = fields.Many2one('delivery.carrier',string="Méthode de livraison")




class CrmCaseCateg(models.Model):
    _name = "crm.case.categ"
    name = fields.Char(string="Nom du segment")

class CrmTrackingCampaign(models.Model):
    _name = "crm.tracking.campaign"
    name = fields.Char(string="Nom de la campagne")


class CrmTrackingSource(models.Model):
    _name = "crm.tracking.source"
    name = fields.Char(string="Nom de l'origine'")


class PosPaiement(models.Model):
    _inherit = "pos.payment.method"
    code = fields.Char(string="Code")
    cash_control = fields.Boolean(string="Gestion du contrôle de caisse")
    account_id = fields.Many2one('account.account',string="Compte de transfert interne")
    account_cash_in_id = fields.Many2one('account.account',string="Compte (Entrée de caisse))")
    account_cash_out_id = fields.Many2one('account.account',string="Compte (Sortie de caisse))")
    journal_in_id = fields.Many2one('account.journal',string="Journal (Entrée de caisse))")
    journal_out_id = fields.Many2one('account.journal',string="Journal (Sortie de caisse))")
    journal_ecart_id = fields.Many2one('account.journal',string="Journal (Ecart de caisse))")


class SaleLine(models.Model):

    _inherit = 'sale.order.line'

    manufacturer_id = fields.Many2one('engine.manufacturer','Marque')
    real_qty_available = fields.Float(string="Qté Dispo")
    price_unit_public = fields.Float(string="P.U. Public")

    qty_location = fields.Float(string="Quantité Disponible", compute="_get_qty_location")
    type_remise = fields.Boolean(related='order_id.partner_id.is_cheque_flotte')





    def _get_qty_location(self):
        
        # location = self.env['pos.config'].search([('user_id','=',self.env.uid)], limit=1)
        location = self.env['pos.config'].search([('user_id','=',2)], limit=1)
        for rec in self:
            
            rec.qty_location = rec.product_id.qty_location



    @api.onchange('product_id')
    def additional_info(self):
        if(self.product_id):
            for rec in self:
                if(self.product_id.qty_location <= 0):
                    print("ProductTemplateExtra ACTIONS: %s" % self.product_id.qty_location)
                    raise ValidationError('Quantité non disponible')
            
                    
                else:
                    product = rec.env['product.product'].search([('id','=',rec.product_id.id)])

                    rec.manufacturer_id = product.product_tmpl_id.manufacturer_id.id
                    rec.real_qty_available = product.product_tmpl_id.real_qty_available
                    rec.price_unit_public = product.product_tmpl_id.lst_price
                    rec.qty_location = product.qty_location
                    if(self.order_id.partner_id.is_cheque_flotte):
                        rec.discount = self.order_id.partner_id.pourcentage_remise
                    


    @api.onchange('discount')
    def check_discount(self):
        if(self.product_id):
            print("PPPPPPPPPPPP Product" +str(self.product_id))
            if(self.discount):
                for rec in self:
                    if(rec.discount > self.product_id.product_tmpl_id.categ_id.seuil and self.product_id.product_tmpl_id.categ_id.seuil > 0):                    
                        self.discount = 0
                        raise ValidationError('Vous avez dépassé le seuil de la remise   ' )
                    

                
class DeliveryCarrier(models.Model):
    _name = "delivery.carrier"

    name = fields.Char(string="Methode de livraison")
    image_medium = fields.Image()
    active = fields.Boolean(string="actif")
    partner_id = fields.Many2one('res.partner',string="Transporteur")
    product_id = fields.Many2one('product.product',string="Article de livraison")
    sequence = fields.Integer(string="Séquence")
    is_relay = fields.Boolean(string="Point de relais")
    normal_price = fields.Float(string="Prix normal")
    free_if_more_than = fields.Boolean(string="Gratuit si le montant total de la commande est superieur a")
    use_detailed_pricelist = fields.Boolean(string="Tarification avancee en fonction de la destination")



class OrderDeposit(models.Model):
    _name = "order.deposit.wizard"

    journal_id = fields.Many2one('account.journal', string = "Journal")
    account_payment_id = fields.Many2one('pos.payment.method',string="Type de paiement")
    amount = fields.Float(string = "Montant payé")
    date = fields.Date(string = "Date")
    date_maturity = fields.Date(string = "Date d'échéance")
    ref_payment = fields.Char(string = "Ref. du règlement")
    memo = fields.Char(string = "Mémo")
    customer_check_name = fields.Char(string = "Titulaire du chèque")


