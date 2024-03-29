# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Diagnostic(http.Controller):
    @http.route('/ps_rezoroute/ps_rezoroute',type="http", website=True ,auth='public')
    def index(self, **kw):
        sale_id = request.env['sale.order'].search([('id','=',kw.get('sale_order'))])

        print("@@@@ Hello " +str(kw.get('sale_order')))
        print("@@@@ Hello " +str(sale_id))
        return http.request.render('ps_rezoroute.update_diagnostic_template', {'sale_id':sale_id})

    @http.route('/update/diagnostic',type="http", website=True ,auth='public')
    def update_diagnostic(self, **kw):

        line_list = request.httprequest.form.getlist('line_id')
        comment_list = request.httprequest.form.getlist('comment')
        next_reminder_list = request.httprequest.form.getlist('next_reminder')
        # done_list = request.httprequest.form.getlist('done_diagnostic')
        done_list = request.httprequest.form.to_dict(flat=False)
        
        done_list_dict = list(done_list.values())[4]

       

        for i in range(len(line_list)):
            line_diagnostic = request.env['engin.diagnostic.line'].search([('id','=',line_list[i])])
            is_done = False
            if(line_list[i] in done_list_dict):
                is_done = True

            print("@@@@####### Reminder " +str(next_reminder_list[i]))


            line_diagnostic.write({'comment':comment_list[i],
                                    'next_reminder': str(next_reminder_list[i]),
                                    'done':is_done,
                                    })

       
        return http.request.render('ps_rezoroute.update_diagnostic_done', {})

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
