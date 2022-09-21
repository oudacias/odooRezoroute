from sre_parse import State
from datetime import datetime, timedelta, date
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

from odoo import fields, models,api

class UsersExtra(models.Model):

    _inherit = 'res.users'

    is_mecanic = fields.Boolean(string="Mécanicien ?")
    pos_location = fields.Many2one('pos.config', string="Emplacement")
    pos_config_id = fields.One2many('pos.config','user_id')
