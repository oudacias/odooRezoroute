# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ps_rezoroute(models.Model):
#     _name = 'ps_rezoroute.ps_rezoroute'
#     _description = 'ps_rezoroute.ps_rezoroute'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
