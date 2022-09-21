from odoo import fields, models,api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_document_approve = fields.Boolean(config_parameter='sale.sale_document_approve')


class SaleOrderLine(models.Model):
    """In this class we are inheriting the model sale.order and adding
        a new field for signature"""

    _inherit = 'sale.order'

    sale_person_signature = fields.Binary(string='Signature', help="Field for adding the signature of the sales person")
    check_signature = fields.Boolean(compute='_compute_check_signature')

    @api.depends('sale_person_signature')
    def _compute_check_signature(self):
        """In this function computes the value of the boolean field check signature
        which is used to hide/unhide the validate button in the current document"""
        if self.env['ir.config_parameter'].sudo().get_param('sale.sale_document_approve'):
            if self.sale_person_signature:
                self.check_signature = True
            else:
                self.check_signature = False
        else:
            self.check_signature = True
