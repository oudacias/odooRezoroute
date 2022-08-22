from odoo import fields, models, api

class EnginDiagnostic(models.Model):

    _name = 'engin.diagnostic'
    
    name = fields.Char(string="Fiche diagnostic")
    is_default = fields.Boolean(string="Par défaut")
    active = fields.Boolean(string="Active")
    engin_diagnostic_line = fields.One2many('engin.diagnostic.line','diagnostic_id')
    diagnostic_sale_id = fields.Many2one('sale.order')


class EnginDiagnosticLine(models.Model):

    _name = 'engin.diagnostic.line'
    name = fields.Char(string="Fiche diagnostic")
    sequence = fields.Integer(string="Séquence")
    description = fields.Text(string="Description de la tâche")
    diagnostic_id = fields.Many2one('engin.diagnostic')

class DevisDiagnostic(models.Model):

    _inherit = 'sale.order'
    engin_diagnostic_sale = fields.One2many('engin.diagnostic','diagnostic_sale_id')

    def add_diagnostic(self):
        return {
            'res_model': 'engin.diagnostic.wizard',
            'view_mode': 'form',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'views' : [(False, 'form')],
            
            }  
class DiagnosticWizard(models.Model):

    name = 'engin.diagnostic.wizard'
    diagnostic_id = fields.Many2one('engin.diagnostic')
    sale_id = fields.Many2one('sale.order')

