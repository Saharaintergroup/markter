# -*- coding: utf-8 -*-
{
    'name': "Marketer",



    'author': "Sahra co.ltd",
    'website': "http://www.odoo.com",
    'category': 'custom',
    'version': '1.0',
    'depends': [
        'base','sale_management','stock'   
        ],   

    'data': [
        'views/partner_complain_view.xml',
        'views/res_partner_view.xml',
        'views/messaging.xml',
        'security/ir.model.access.csv'
    ],    
}
