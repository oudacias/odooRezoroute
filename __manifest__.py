# -*- coding: utf-8 -*-
{
    'name': "ps_rezoroute",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','pos_sale','purchase_requisition','sale','purchase','account','fleet','stock','website'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/products.xml',
        'views/golda.xml',
        'views/clients.xml',
        'views/vehicules.xml',
        'views/devis.xml',
        'views/type_paiement.xml',
        'views/ligne_commande.xml',
        'views/pos_view.xml',
        'views/pos_user_view.xml',
        'data/cronvalidate.xml',
        'report/report_xcaisse.xml',
        'report/report_posreport.xml',
        
        'report/report_devis_template_or.xml',
        'report/report_devis_template.xml',
        'report/report_test.xml',


        'report/report_demande_prix.xml',
        'report/report_demande_prix_template.xml',

       

        'report/report_bon_livraison.xml',
        'report/report_bon_livraison_template.xml',

        'report/report_facture.xml',
        'report/report_facture_template.xml',


        'report/report_bon_commande.xml',
        'report/report_bon_commande_template.xml',

        'report/report_devis.xml',
        'report/hide_reports.xml',
        'views/purchase.xml',
        'views/payment.xml',
        'views/stock_picking.xml',
        'views/calendar.xml',
        'views/diagnostic.xml',
        'views/website_diagnostic.xml',
        'views/forfaits.xml',

        
    ],
    'assets': {
        'web._assets_primary_variables': [
            
        ],
        'web.assets_backend': [
            'ps_rezoroute/static/src/css/test.css',
        ]
    },
    # 'assets': {
    #     'web.assets_backend' [
    #         'ps_rezoroute/static/src/css/test.css',
    #     ]},

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

   
   
}
