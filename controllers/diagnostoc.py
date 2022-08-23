# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Diagnostic(http.Controller):
    @http.route('/ps_rezoroute/ps_rezoroute',type="http", website=True ,auth='public')
    def index(self, **kw):
        sale_id = request.env['sale.order'].search([('id','=',kw.get('sale_id'))])

        print("@@@@ Hello")
        print("@@@@ Hello " +str(sale_id))
        return http.request.render('ps_rezoroute.update_diagnostic_template', {'sale_id':sale_id})

    # @http.route('/ps_rezoroute/ps_rezoroute/objects', auth='public')
    # def list(self, **kw):
    #     return http.request.render('ps_rezoroute.listing', {
    #         'root': '/ps_rezoroute/ps_rezoroute',
    #         'objects': http.request.env['ps_rezoroute.ps_rezoroute'].search([]),
    #     })

    # @http.route('/ps_rezoroute/ps_rezoroute/objects/<model("ps_rezoroute.ps_rezoroute"):obj>', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('ps_rezoroute.object', {
    #         'object': obj
    #     })
