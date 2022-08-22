from odoo import fields, models, api

class EnginDiagnostic(models.Model):

    _name = 'engin.diagnostic'
    
    name = fields.Char(string="Fiche diagnostic")
    is_default = fields.Boolean(string="Par défaut")
    active = fields.Boolean(string="Active")
    engin_diagnostic_line = fields.One2many('engin.diagnostic.line','diagnostic_id')


class EnginDiagnosticLine(models.Model):

    _name = 'engin.diagnostic.line'
    name = fields.Char(string="Fiche diagnostic")
    sequence = fields.Integer(string="Séquence")
    description = fields.Text(string="Description de la tâche")