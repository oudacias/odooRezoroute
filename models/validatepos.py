from odoo import models, fields

class ValidateSession(models.Model):
   _name = 'pos.session'
   def action_done(self):
       for rec in self:
            if (rec.state == "opening_control"):
                rec.write({'state':'closing_control'})