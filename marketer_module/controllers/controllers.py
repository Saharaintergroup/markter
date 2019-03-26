# -*- coding: utf-8 -*-
import odoo.http as http
import smtplib
from random import randint
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
from odoo.exceptions import UserError
from odoo.addons.auth_signup.models.res_users import SignupError
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
    reset_password_data = []

    @http.route('/web/reset_pasord', type='json', auth='public', website=True, csrf=False, sitemap=False)
    def web_auth_reset_password(self, **kw):
      data = {}
      try:
        login = kw.get('login')
        request.env['res.users'].sudo().reset_password(login)
        data['message'] = _("An email has been sent with credentials to reset your password")
        data['result'] = "True"
      except UserError as e:     
        data['message'] = e.name or e.value
        data['result'] = "False"
      except SignupError:
        data['message'] = _("Could not reset your password")
        data['result'] = "False"
      except Exception as e:
        data['message'] = str(e)
        data['result'] = "False"
      res = {
        "message" : data['message'],
        "status" :data['result']
      }
      return res

    @http.route(['/reset_pass_marketer'], redirect=None,auth="public",csrf=False,website=True,method='POST')
    def reset_password(self, **kw):
      model = kw.get('model')
      email = kw.get('email')
      target = request.env[model]
      user = target.search([
        ('email','=',email)
      ])
      result = ''       
      if user:
        try:
          n = 4
          range_start = 10**(n-1)
          range_end = (10**n)-1
          context = randint(range_start, range_end)
          mail = smtplib.SMTP('smtp.gmail.com',587)
          mail.ehlo()
          mail.starttls()
          mail.login('mosabawad4949@gmail.com','1234567mm')
          mail.sendmail('mosabawad4949@gmail.com',email,str(context))
          mail.close()
          result = str(context)
        except Exception as identifier:
          result = "Exception"
      else:
        result = "this emaill is not used in this application"
      return result

    @http.route(['/new_password_marketer'], redirect=None,auth="public",csrf=False,website=True,method='POST')
    def new_password_marketer(self, **kw):
      model = kw.get('model')
      email = kw.get('email')
      password = kw.get('password')
      target = request.env[model]
      user = target.search([
        ('email','=',email)
      ])
      result = ""
      try:
        if model == 'res.users':
          user.write({
            'password':password
          })
          result = "done"
        elif model == 'res.partner':
          user.write({
            'gaith':password
          })
          result = "done"
      except Exception as identifier:
        result = "Exception"
      return str(result)
    
    # @http.route('/set_new_password/<string:model>/<string:email>/<string:newPassword>')
    # def set_new_password(self,model,email , newPassword, **args):
    #   target = request.env[model]
    #   user = target.search([
    #     ('email','=',email)
    #   ])
    #   result = ""
    #   try:
    #     if model == 'res.users':
    #       user.write({
    #         'password':newPassword
    #       })
    #       result = "done"
    #     elif model == 'res.partner':
    #       user.write({
    #         'gaith':newPassword
    #       })
    #       result = "done"
    #   except Exception as identifier:
    #     result = "Exception"
    #   return str(result)
    