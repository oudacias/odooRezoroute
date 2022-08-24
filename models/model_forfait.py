from odoo import fields, models, api

class ProductForfait(models.Model):

    _name = 'product.forfait'

    code = fields.Char(string="Code")
    nom = fields.Char(string="Nom")
    start_date = fields.Date(string="Date de début")
    end_date = fields.Date(string="Date de fin")
    line_ids = fields.One2many('product.forfait.line','forfait_line_ids')

