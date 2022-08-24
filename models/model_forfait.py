from odoo import fields, models, api

class PurchaseForfait(models.Model):

    _name = 'purchase.forfait'

    code = fields.Char(string="Code")
    nom = fields.Char(string="Nom")
    start_date = fields.Date(string="Date de début")
    end_date = fields.Date(string="Date de fin")
    total_forfait = fields.Float(string="Total", compute="_get_total")
    line_ids = fields.One2many('product.forfait.line','forfait_line_ids')


    def _get_total(self):
        self.total_forfait = 0
        for rec in self:
            for line in rec.line_ids:
                rec.total_forfait += line.prix_forfait



class ProductForfaitLine(models.Model):

    _name = 'product.forfait.line'

    product_id = fields.Many2one('product.product',string="Article")
    prix_product = fields.Float(string="Prix du Produit")
    facultatif = fields.Boolean(string="Facultatif")
    prix_forfait = fields.Float(string="Prix Forfait")
    # is_tecdoc = fields.Boolean(string="TecDoc")
    # gen_art_id = fields.Many2one('tecdoc.generic.article',string="Piece")
    # categ_id = fields.Many2one('product.category',string="Categorie")
    # brand_ids = fields.Many2many("ps.product.engine","forfait_line_engine_rel","engine_id","forfait_line_id",string="",default_order="name asc")
    quantity = fields.Float(string="Quantité")
    # is_price_zero = fields.Boolean(string="Inclus/Offert")
    # pricelist_id = fields.Many2one('product.pricelist',string="Liste de prix")
    forfait_line_ids = fields.Many2one('purchase.forfait')

    forfait_sale_id = fields.Many2one('sale.order')

    # def _get_prix_product(self):
    #     self.prix_product = self.product_id.list_price

    @api.onchange('product_id')
    def _get_price(self):
        if(self.product_id.id):
            self.prix_product = self.product_id.list_price




# class TecdocGenericArticle(models.Model):
#     _name = "tecdoc.generic.article"

#     nom = fields.Char(string="Nom")
#     groupe_assemblage = fields.Char(string="Groupe d'assemblage")
#     vl = fields.Boolean(string="VL")
#     pl = fields.Boolean(string="PL")
#     universel = fields.Boolean(string="Universel")
#     reference_tecdoc = fields.Integer(string="Reference TecDoc")



class DevisForfait(models.Model):

    _inherit = 'sale.order'
    forfait_sale = fields.One2many('product.forfait.line','forfait_sale_id')

    def add_forfait(self):
        return {

            'res_model': 'forfait.wizard',
            'view_mode': 'form',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'views' : [(False, 'form')],
            'context' : {'default_sale_id' : self.id }
            
        }  


class ForfaitWizard(models.Model):

    _name = 'forfait.wizard'
    forfait_id = fields.Many2one('purchase.forfait', string="Fiche Forfait")
    sale_id = fields.Many2one('sale.order')


    @api.model
    def create(self, values):
        forfait_id = self.env['purchase.forfait'].search([('id','=',values['forfait_id'])])
        sale_id = self.env['sale.order'].search([('id','=',values['sale_id'])])
        for rec in forfait_id.line_ids:
            sale_id.order_line.create({
                                        'product_id': rec.product_id.id,
                                        'name': rec.product_id.name,
                                        'order_id': sale_id.id,
                                        'product_uom' : rec.product_id.uom_id.id,
                                        'product_uom_qty' : rec.quantity,
                                        'price_unit' : rec.prix_forfait,
                                    })    

            # sale_id.order_line.update({'product_id':rec.product_id.id})

            # sale_id.update({'forfait_sale': [(0, 0, {'product_id':rec.name, 'sequence': rec.sequence, 'description': rec.description})]})
                


        q= super(ForfaitWizard, self).create(values) 
        return q
        