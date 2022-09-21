# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EnginManufacturerGolda(models.Model):
    _name = "engin.manufacturer.golda"

    name = fields.Char(string="Nom")
    golda_ref = fields.Char(string="Reference Golda")
    active = fields.Boolean(string="Actif")



class EnginManufacturerGoldaDiscount(models.Model):
    _name = "engin.manufacturer.golda.discount"

    name = fields.Char(string="Nom")
    sequence = fields.Char(string="Sequence")
    active = fields.Boolean(string="Actif")



class EnginManufacturerGoldaCategory(models.Model):
    _name = "engin.manufacturer.golda.category"

    name = fields.Char(string="Nom")
    golda_ref = fields.Char(string="Reference Golda")
    sequence = fields.Char(string="Sequence")
    active = fields.Boolean(string="Actif")
    parent_id = fields.Many2one('engin.manufacturer.golda.category','Categorie parente')