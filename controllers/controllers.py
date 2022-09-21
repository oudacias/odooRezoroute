# -*- coding: utf-8 -*-
# from odoo import http


# class PsRezoroute(http.Controller):
#     @http.route('/ps_rezoroute/ps_rezoroute', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ps_rezoroute/ps_rezoroute/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ps_rezoroute.listing', {
#             'root': '/ps_rezoroute/ps_rezoroute',
#             'objects': http.request.env['ps_rezoroute.ps_rezoroute'].search([]),
#         })

#     @http.route('/ps_rezoroute/ps_rezoroute/objects/<model("ps_rezoroute.ps_rezoroute"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ps_rezoroute.object', {
#             'object': obj
#         })
