from odoo import fields, models, api

class ProductForfait(models.Model):

    _name = 'product.forfait'

    code = fields.Char(string="Code")
    nom = fields.Char(string="Nom")
    category_id = fields.Many2one('product.forfait.category',string="Catégorie")
    note = fields.Text(string="Note")
    company_ids = fields.Many2one('res.company',string="Companies")
    active = fields.Boolean(string="Actif")

    price_from_ht = fields.Float(string="A partir de H.T.")
    sequence = fields.Integer(string="Sequence")
    checklist_ids = fields.Many2many('product.forfait.checklist','forfait_checklist_rel','forfait_id','checklist_id')
    line_ids = fields.One2many('product.forfait.line','forfait_line_ids')

class ProductForfaitCategory(models.Model):

    _name = 'product.forfait.category'

    nom = fields.Char(string="Nom")
    sequence = fields.Integer(string="Sequence")
    active = fields.Boolean(string="Actif")


class ProductForfaitChecklist(models.Model):

    _name = 'product.forfait.checklist'

    nom = fields.Char(string="Nom")
    

class ProductForfaitLine(models.Model):

    _name = 'product.forfait.line'

    sequence = fields.Integer(string="Sequence")
    product_id = fields.Many2one('product.product',string="Article")
    is_tecdoc = fields.Boolean(string="TecDoc")
    gen_art_id = fields.Many2one('tecdoc.generic.article',string="Piece")
    categ_id = fields.Many2one('product.category',string="Categorie")
    brand_ids = fields.Many2many("ps.product.engine","forfait_line_engine_rel","engine_id","forfait_line_id",string="",default_order="name asc")
    quantity = fields.Float(string="Quantite")
    is_price_zero = fields.Boolean(string="Inclus/Offert")
    pricelist_id = fields.Many2one('product.pricelist',string="Liste de prix")
    forfait_line_ids = fields.Many2one('product.forfait')



class TecdocGenericArticle(models.Model):
    _name = "tecdoc.generic.article"

    nom = fields.Char(string="Nom")
    groupe_assemblage = fields.Char(string="Groupe d'assemblage")
    vl = fields.Boolean(string="VL")
    pl = fields.Boolean(string="PL")
    universel = fields.Boolean(string="Universel")
    reference_tecdoc = fields.Integer(string="Reference TecDoc")
