from odoo import fields, models, api

class ProductTemplateExtra(models.Model):

    _inherit = 'product.template'

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


    sale_line_warn = fields.Selection([('no-message','Aucun Message'),('warning','Avertissement'),('block','Message Bloquant')],string="Ligne de commande de vente")
    sale_line_warn_msg = fields.Text(string="Message a la ligne de commande de vente")

    purchase_line_warn = fields.Selection([('no-message','Aucun Message'),('warning','Avertissement'),('block','Message Bloquant')],string="Ligne de commande d'achat")
    purchase_line_warn_msg = fields.Text(string="Message a la ligne de commande")


    golda_price_init = fields.Float(string="Golda price init")
    price_rate_upselling = fields.Float(string="Coeff applique avant coeff liste de prix")
    
    replace = fields.Many2one("res.company", string="Remplace par")
    
    product_pricelist_item = fields.One2many("product.pricelist.item","product_tmpl_id","Pricelist Items")
    _sql_constraints = [('ps_code_article_unique', ' unique (ps_code_article)','Ce code article existe deja !')]


    reference_code = fields.Text()

    engine_list = fields.Many2many("ps.product.engine","product_engine_rel","engine_id","template_id",string="",default_order="name asc")

    # @api.model
    # def create(self, values):
    #     reference = ""
    #     if(len(values['detailed_type'].split()) == 1):
            
    #         reference += values['detailed_type'][0:1]
    #     else:
    #         reference += values['detailed_type'].split()[0][0] + values['detailed_type'].split()[1][0]
        

    #     category_pr = self.env['product.category'].search([('id','=',values['categ_id'])])
    #     # category = self.env('product.category').search([('id','=',values['categ_id'])])
    #     # category = self.env('product.template').browse(1)

    #     reference +="." + category_pr.name[0:1]

    #     values['reference_code'] = reference
        
    #     q= super(ProductTemplateExtra, self).create(values) 
    #     return q
        







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


class ProductExtra(models.Model):
    _inherit = "product.product"

    qty_location = fields.Float(string="Quantité Disponible", compute="_get_qty_location")



    def _get_qty_location(self):
        qty = 0
        location = self.env['pos.config'].search([('user_id','=',self.env.uid)], limit=1)
        for rec in self:
            
            stock_quant = self.env["stock.quant"].search([('product_id','=',rec.id),('location_id','=',location.location_id.id)])
            
            for line_qty in stock_quant:
                if(rec.id == 19):
                    print("@@@@@@@@################################################################################")
                    print(str(rec.id))
                    print(str(location.location_id.id))
                    print(str(line_qty.quantity))
                qty += line_qty.quantity
            print(qty)

            
            rec.qty_location = 10

        

        
