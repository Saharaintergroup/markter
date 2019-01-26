# -*- coding: utf-8 -*-
{
    'name': "Marketer",



    'author': "Sahra co.ltd",
    'website': "http://www.odoo.com",
    'category': 'custom',
    'version': '1.0',
    'depends': [
        'base','sale'    
        ],

    'data': [
        'views/res_partner_view.xml',
        'views/partner_complain_view.xml',
        'security/ir.model.access.csv'
    ],    
}
