from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ProductTemplateExtraa(models.Model):

    _inherit = 'product.template'


    # ----------------temp fields

    category_product = fields.Text(string="Catégorie du produit")
    product_code = fields.Text(string="Code du produit")


    # ----------------temp fields end

    image1 = fields.Image(String="Image 1")
    image2 = fields.Image(String="Image 2")

    manufacturer_id = fields.Many2one('engine.manufacturer',string="Constructeur")

    ps_code_article = fields.Char('Code Article')
    is_reconditionned = fields.Boolean('Reconditionne')
    is_sell_first = fields.Boolean("Vendre d'abord")
    is_special_order = fields.Boolean("Commande speciale")
    is_outdated = fields.Boolean("Provisionne")
    is_manage_in_stock = fields.Boolean("Reapprovisionnable")


    is_group_reference = fields.Boolean("Reference d'equivalence")

    nbr_stock_minimum = fields.Float("Nbr de stock minimum (Qte reappro)")
    nbr_stock_atteindre = fields.Float("Nbr de stock a atteindre (Qte reappro)")
    replace = fields.Many2one("ps.product.remplace", string="Remplace par")
    lst_price = fields.Float(string="Prix public")



    is_tire = fields.Boolean("Pneumatique")
    tecdoc_details = fields.Html(string="Details")


    external_information_url = fields.Char("URL d'information externe")
    short_codes = fields.Char("Ref. catalogue")

    manufacturer_ids = fields.One2many("ps.product.manufacturer","manufacturers_id" ,string="")
    full_images_ids = fields.One2many("ps.product.fullimage","images_id" ,string="")

    price_ht = fields.Float(string="Prix HT")
    price_ttc = fields.Float(string="Prix TTC")

    qty_available = fields.Float(string="En stock")
    outgoing_qty = fields.Float(string="Sortants")
    real_qty_available = fields.Float(string="Disponible")
    incoming_qty = fields.Float(string="Entrant")
    virtual_available = fields.Float(string="Stock a terme")


    warranty = fields.Float(string="Garantie")
    sale_delay = fields.Float(string="Delai de livraison au client")






    state = fields.Selection([('draft','En developpement'),('sellable','Normal'),('end','Fin de cycle de vie'),('obsolete','Obsolete')],string="Etat")
    product_manager = fields.Many2one("res.users", string="Remplace par")

    loc_rack = fields.Char(string="Rayon")
    loc_row = fields.Char(string="Rangee")
    loc_case = fields.Char(string="Case")
    weight_net = fields.Float(string="Poids net")



    golda_price_init = fields.Float(string="Golda price init")
    price_rate_upselling = fields.Float(string="Coeff applique avant coeff liste de prix")
    
    replace = fields.Many2one("product.template", string="Remplace par")
    
    product_pricelist_item = fields.One2many("product.pricelist.item","product_tmpl_id","Pricelist Items")
    _sql_constraints = [('ps_code_article_unique', ' unique (ps_code_article)','Ce code article existe deja !')]


    reference_code = fields.Text()

    engine_list = fields.Many2many("ps.product.engine","product_engine_rel","engine_id","template_id",string="",default_order="name asc")

    @api.model
    def create(self, values):

        reference_new = ""
        type_new = ""
        maxi_rec = self.env['sequence.product'].search([])
        last_sequence = len(maxi_rec) + 1
        category_pr = self.env['product.category'].search([('id','=',values['categ_id'])])
        type_pr = values['detailed_type'].split()

        if(len(type_pr) == 1):
            type_new = values['detailed_type'][0:2].upper()
        else:
            for type in type_pr:
                type = type.lstrip().upper()
                type_new += type[0:2]

        reference = category_pr.complete_name.split('/')
        for ref in reference:
            ref = ref.lstrip().upper()
            reference_new += ref[0:2] + "."
        
        reference_new = reference_new[:-1]

       

        values['default_code'] = str(type_new) +"."+ str(reference_new) +"-"+ str(last_sequence)
        maxi_rec.create({'sequence_id': last_sequence})

        q= super(ProductTemplateExtraa, self).create(values) 
        return q
        







class ProductEngine(models.Model):
    _name = "ps.product.engine"
    
    constructeur = fields.Char('Constructeur')
    modele = fields.Char('Modele')
    display_name = fields.Char('Display Name')
    product_ids = fields.Many2many('product.template')


class ProductRemplace(models.Model):
    _name = "ps.product.remplace"
    name = fields.Char("Nom")


class ProductManufacturer(models.Model):
    _name="ps.product.manufacturer"
    reference = fields.Char("Reference")
    marque = fields.Char(string="Marque/Constructer")
    is_oe = fields.Boolean(string = "Is OE")
    reference_catalogue = fields.Char(string="Reference Catalogue")
    is_tecdoc = fields.Boolean(string="Is TecDoc")

    manufacturers_id = fields.Many2one("product.template")


class ProductFullImage(models.Model):
    _name = "ps.product.fullimage"

    image = fields.Image("image")
    sequence = fields.Char("Sequence")
    picture_url = fields.Char("Picture Url")
    full_picture_url = fields.Char("Full Picture URL")
    images_id = fields.Many2one("product.template")



class ProductPriceListExtra(models.Model):
    _inherit = "product.pricelist.item"

    sequence = fields.Integer(string="Sequence")
    r1 = fields.Char(string="R1")
    version_liste_prix = fields.Char(string="Version de liste de prix")
    r2 = fields.Char(string="R2")
    prix_net = fields.Float(string="Prix Net")
    prix_ht = fields.Float(string="Prix HT")
    prix_ttc = fields.Float(string="Prix TTC")



class ReferenceIntern(models.Model):
    _name = "refernce.intern"
    model_name = fields.Char()
    reference_id = fields.Integer()


class ProductTemplateExtra(models.Model):

    _inherit = 'product.category'

    seuil = fields.Float(string="Seuil de remise")
    marge = fields.Float(string="Marge")


class ProductExtra(models.Model):
    _inherit = "product.product"

    qty_location = fields.Float(string="Quantité Disponible", compute="_get_qty_location")

    @api.model
    def create(self, vals):
        print("@@@@ Group UserError  - create "  +str(self.env.user.has_group('ps_rezoroute.group_gestionnaire')))
        if self.env.user.has_group('ps_rezoroute.group_gestionnaire'):
            raise ValidationError(
                ('Vous ne pouvez pas créer un nouveau produit'),
            )
        else:
            return super(ProductExtra, self).create(vals)



    def _get_qty_location(self):

        # location = self.env['pos.session'].search([('state','=','opening_control'),('user_id','=',self.env.uid)],order="id desc", limit =1)
        
        location = self.env['pos.config'].search([('user_id','=',self.env.uid)], limit=1)
        for rec in self:
            
            stock_quant = self.env["stock.quant"].search([('product_id','=',rec.id),('location_id','=',location.location_id.id)])
            qty = 0
            for line_qty in stock_quant:

                qty += line_qty.quantity
            
            rec.qty_location = qty


class SequenceArticle(models.Model):

    _name = 'sequence.product'

    sequence_id = fields.Integer()

        

        
