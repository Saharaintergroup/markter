# -*- coding: utf-8 -*-
import odoo.http as http
from odoo.http import Response
from odoo import SUPERUSER_ID
import sys, json
import logging
_logger = logging.getLogger(__name__)
from odoo.http import request
from datetime import datetime,timedelta,date
from dateutil.relativedelta import relativedelta
from odoo import models,fields,api,_
from openerp import fields
from passlib.context import CryptContext
from passlib.context import CryptContext
class WebFormController(http.Controller):    
    
    default_crypt_contex = CryptContext(
    # kdf which can be verified by the context. The default encryption kdf is
    # the first of the list
    ['pbkdf2_sha512', 'md5_crypt'],
    # deprecated algorithms are still verified as usual, but ``needs_update``
    # will indicate that the stored hash should be replaced by a more recent
    # algorithm. Passlib 1.6 supports an `auto` value which deprecates any
    # algorithm but the default, but Ubuntu LTS only provides 1.5 so far.
    deprecated=['md5_crypt'],
    )


    def hash(password):
        password = hashlib.md5()
        password.hexdigest()
        return password

    @http.route('/check_login/<string:user_name>/<string:password>/<string:model>', type='http', auth='public', csrf=False)
    def check_login(self,user_name,password,model,**args):
        # default_crypt_contex = CryptContext(['pbkdf2_sha512', 'md5_crypt'],deprecated=['md5_crypt'],)
        default_crypt_contex = CryptContext(['pbkdf2_sha512']).encrypt(password)
        # get object 
        target=request.env[model]
        # check user name
        user=target.search([('name','=',user_name),('password','=',password)])
        result=False
        if user:
            result=True
        return str(result)
    
    @http.route('/customer_login/<string:email>/<string:password>',type='http', auth='public', csrf=False)
    def customer_login(self, email, password,**args):
      
      target=request.env['res.partner']
      password = hash(hash)
      user = target.search([
        ('email','=',email)
      ])
      Success = "Success :"+str(user.password)
      Failure = "Failure :"+ str(password)
      if user:
        return Success
      else:
        return Failure

    @http.route('/marketer_orders/<int:user_id>/', type='http', auth='public', csrf=False)
    def marketer_orders_details(self,user_id,**args):
    	#orders


        query='''select hr_employee_id from hr_employee_mk_mosque_rel where mk_mosque_id IN %(mosque)s'''

        query=''' 
				select 
				  sale_order.name as order, 
				  sale_order.partner_id as customer_id, 
				  sale_order.state as order_state, 
				  sale_order.date_order , 
				  account_payment.state as payment_state, 
				  sale_order.user_id as marketer, 
				  account_payment.payment_type, 
				  account_payment.amount, 
				  res_partner.name as customer_name
				from
				  public.sale_order, 
				  public.account_invoice, 
				  public.account_payment, 
				  public.res_partner
				where 
				  sale_order.name = account_invoice.origin AND
				  sale_order.partner_id = res_partner.id AND
				  account_invoice.reference = account_payment.communication
				  And sale_order.user_id=%(marketer)s
				 ;
        '''



        cr=request.env.cr
        sup_ids=cr.execute(query,{'marketer':(user_id)})
        sup = request.env.cr.dictfetchall()
        for rec in sup:
        	date=str(rec['date_order'])[:10]
        	time=str(rec['date_order'])[10:]
        	rec['date_order']=date
        	rec['time_order']=time
        return str(sup)