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
    diagnostic_id = fields.Many2one('engin.diagnostic')
    diagnostic_sale_id = fields.Many2one('sale.order')


class DevisDiagnostic(models.Model):

    _inherit = 'sale.order'
    engin_diagnostic_sale = fields.One2many('engin.diagnostic.line','diagnostic_sale_id')

    def add_diagnostic(self):
        return {
            'res_model': 'engin.diagnostic.wizard',
            'view_mode': 'form',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'views' : [(False, 'form')],
            'context' : {'default_sale_id' : self.id }
            
            }  
class DiagnosticWizard(models.Model):

    _name = 'engin.diagnostic.wizard'
    diagnostic_id = fields.Many2one('engin.diagnostic', string="Fiche diagnostic")
    sale_id = fields.Many2one('sale.order')


    @api.model
    def create(self, values):
        diagnostic_id = self.env['engin.diagnostic'].search([('id','=',values['diagnostic_id'])])
        sale_id = self.env['sale.order'].search([('id','=',values['sale_id'])])

        for rec in diagnostic_id.engin_diagnostic_line:
            print("@@@@ DiagnosticWizard format 1: " + str(values['sale_id']))
            print("@@@@ DiagnosticWizard format: " + str(sale_id.id))
            sale_id.write({
                'engin_diagnostic_sale': [(0, 0, {rec.id})],
            })
            


        q= super(DiagnosticWizard, self).create(values) 
        return q
        
