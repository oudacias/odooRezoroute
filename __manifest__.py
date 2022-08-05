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
    'depends': ['base','pos_sale','sale','purchase','account','fleet','stock'],

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
        'views/forfaits.xml',
        'views/ligne_commande.xml',
        'views/pos_view.xml',
        'views/pos_user_view.xml',
        'data/cronvalidate.xml',
        'report/report_xcaisse.xml',
        'report/report_posreport.xml',
        
        'report/report_devis_template.xml',
        'report/report_devis.xml',
        'views/purchase.xml',
        'views/payment.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

   
    'assets': {
        'web.assets_backend' [
            'ps_rezoroute/static/src/css/test.css',
        ]},
}
