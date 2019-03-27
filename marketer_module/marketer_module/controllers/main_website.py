from datetime import datetime,timedelta,date
from odoo import http, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.http import request
from odoo import fields, models, api, exceptions, _
from odoo.exceptions import ValidationError, AccessError
import psycopg2, psycopg2.extras
from dateutil.relativedelta import relativedelta
import datetime
from dateutil import parser
import base64
from passlib.context import CryptContext
import werkzeug
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from collections import OrderedDict
from werkzeug.urls import url_decode, iri_to_uri


class MyController(http.Controller):

  @http.route(['/federal_request'], auth="public", website=True)
  def federal_form(self , **kw):
    # ctx = execjs.compile("""
    #   function add(x, y) {
    #   window.alert('message');
    #   return x + y;
    #   }
    #   """)
    # ctx.call("add", 1, 2)
    # print(":::::::::::",ctx.call("add", 1, 2))
    return request.render("federal_website.federal_request" , {'national_n':  kw.get('national_number') ,  'req_type': kw.get('req_type') , 'nationality': kw.get('nationality') , 'passport':kw.get('passport'),'session_start':kw.get('session_start')})

  @http.route(['/hospital_login'], auth="public", website=True)
  def federal_login(self, **kw):
    return request.render("federal_website.federal_login")


  @http.route(['/request_login'], redirect=None,auth="none",csrf=True,website=True,method='POST')
  def request_login(self, **kw):
    try:
      request.params['login_success'] = False
      if request.httprequest.method == 'GET' and redirect and request.session.uid:
        return http.redirect_with_hash(redirect)

      if request.httprequest.method == 'POST':
        old_uid = request.uid
        uid = request.session.authenticate(request.session.db, request.params['username'], request.params['pass'])
        
        if uid is not False:
          request.params['login_success'] = True
          hospital_info = request.env['hospital.treatment'].sudo().search([('user_id' ,'=' , uid )])        
          response = request.render("federal_website.federal_request",{'hospital_name':hospital_info.name})
          response.headers['X-Frame-Options'] = 'DENY'
          return response

        else:
          request.uid = old_uid
          response = request.render("federal_website.federal_login",{'login_success':'اسم المستخدم أو كلمة المرور غير صحيح'})
          response.headers['X-Frame-Options'] = 'DENY'
          return response
    except:
      pass


  @http.route(['/thank_you'], auth="public", website=True)
  def federal_thanks(self, **kw):
    return request.render("federal_website.federal_thanks")

  @http.route(['/federal_following'], csrf=False, auth="public", website=True)
  def federal_following(self, **kw):
    try:
      if kw.get('natio_validate') == 'False':
        pass

      else:
        has_request = []
        result = []
        if kw.get('n_nat') == 'natio':
          result = request.env['res.partner'].sudo().search([('national_number' ,'=' , kw.get('national_folow') )])
          has_request = request.env['zakat.federaltreatment.request'].sudo().search([('partner_id' ,'=' , result.id)])
          if has_request:
            return request.render("federal_website.federal_following",{'fol_req':has_request , 'partner_info': result})
          else:
            return request.render("federal_website.federal_request" , {'wrong_natio_fol': 'natio_wrong' , 'natio_n': kw.get('national_folow')})

        if kw.get('n_nat') == 'passp':
          result = request.env['res.partner'].sudo().search([('passport' ,'=' , kw.get('pass_fol') )])
          has_request = request.env['zakat.federaltreatment.request'].sudo().search([('partner_id' ,'=' , result.id)])
          if has_request:
            return request.render("federal_website.federal_following",{'fol_req':has_request , 'partner_info': result})
          else:
            return request.render("federal_website.federal_request" , {'wrong_pass_fol': 'passp_wrong' , 'pass_n': kw.get('pass_fol')})

        if kw.get('n_nat') == 'ref':
          has_request = request.env['zakat.federaltreatment.request'].sudo().search([('code' ,'=' , kw.get('follow_num') )])          
          result = request.env['res.partner'].sudo().search([('id' ,'=' , has_request.partner_id.id )])
          if has_request:
            return request.render("federal_website.federal_following",{'fol_req':has_request , 'partner_info': result})
          else:
            return request.render("federal_website.federal_request" , {'wrong_ref_fol': 'ref_wrong' , 'foll_n': kw.get('follow_num')})

    except:
      pass
    

  @http.route(['/federal_request_submit'], auth="public",csrf=True, website=True)
  def federal_submit(self, **kw ):
    try:
        # if kw.get('session_start') != 'True':
        #   return request.render("federal_website.federal_request" , {'session_start': 'False'})
      
      if kw.get('national_validate') == 'False' or kw.get('passport_validate') == 'False':
        pass
      else:
        result = request.env['res.partner'].sudo().search([('national_number' ,'=' , kw.get('national_number') )])
        states = request.env['zakat.state'].sudo().search([])
        if result:
          stored_date_parse = datetime.datetime.strptime(kw.get('b_date'), '%Y-%m-%d')
          b_date_parse = parser.parse(result.birth_date)
          """
          To Do:Integration with national number and get birth date
          """
          if b_date_parse.day == stored_date_parse.day and b_date_parse.month == stored_date_parse.month and b_date_parse.year == stored_date_parse.year:
            has_request = request.env['zakat.federaltreatment.request'].sudo().search([('partner_id' ,'=' , result.id)])
            
            if has_request:
              c_date = has_request[-1].create_date
              r_state = has_request[-1].state
              cc = parser.parse(c_date)
              b = datetime.datetime.now()
              if b.day == cc.day and b.month == cc.month or r_state == 'draft':
                update_allowness = request.env['zakat.federaltreatment.request'].sudo().write({
                  'website_req_allowness':  'False',
                  'partner_id':result.id,})
                return request.render("federal_website.federal_request" , {'request_duration':'عذراً .. لايمكنك تقديم اكثر من طلب في اليوم الواحد، قم بمتابعة الطلبات لإلغاء الطلب السابق غير المصدق'})
                pass
            return request.render("federal_website.registered_data" , {'result':result , 'req_type': kw.get('req_type') ,'session_start':kw.get('session_start')})
          else:
            return request.render("federal_website.federal_request" , {'b_date_error':'تاريخ الميلاد غير صحيح'})
            pass
         
        else:
          return request.render("federal_website.new_registration" , {'national_n':  kw.get('national_number') , 'req_type': kw.get('req_type') , 'nationality': kw.get('nationality'),'passport':kw.get('passport') , 'states':states, 'session_start':kw.get('session_start') })
      
    except:
      pass


  @http.route(['/request_submit'], auth="public", website=True)
  def federal_thanks(self, **kw):
    req_id = []
    if kw.get('amount_v') == 'False' :
        pass
    else:
      try:
        re = request.env['res.partner'].sudo().search([('national_number' ,'=' , kw.get('national_number') )])
        req = request.env['zakat.federaltreatment.request'].sudo().create({
          'first_name':  kw.get('first_name'),
          'second_name': kw.get('second_name') ,
          'third_name':  kw.get('third_name'),
          'forth_name': kw.get('forth_name'),
          'partner_id' :re.id,
          'type': kw.get('req_type') ,
          'birth_date':  kw.get('birth_date'),
          'gender': kw.get('gender'),
          'phone': kw.get('phone'),
          'zakat_state': kw.get('state_id'),
          'national_number': kw.get('national_number'),
          'treatment_amount': kw.get('treatment_amount'),
          'note': kw.get('note'),
          # 'bill': kw.get('bill'),
          # 'medical': kw.get('medical'),
          # 'review': kw.get('review'),
          # 'check': kw.get('check'),
          # 'commission': kw.get('commission'),
          # 'abroad_cost': kw.get('abroad_cost'),
          # 'passport_co': kw.get('passport_co'),
          # 'tickets': kw.get('tickets'),
          # 'visa': kw.get('visa'),
          # 'conversion_replacement': kw.get('conversion_replacement'),
          'website_request_validate':True,

          })

        req_id = request.env['zakat.federaltreatment.request'].sudo().search([('id','=',req.id)])
      except:
        pass 
      return request.render("federal_website.federal_thanks",{'req_ref':req_id.code , 'connection_reset':kw.get('connection_reset')})


  @http.route(['/registration'], auth="public", website=True)
  def federal_register(self, **kw):
    req_id = []
    at = []
    attach = []
    # if kw.get('connection_reset') != 'False':
    #   return request.render("federal_website.federal_request" , {'session_start': 'False'})
    try:
      if kw.get('session_start') != 'True':
        return request.render("federal_website.federal_request" , {'session_start': 'False'})

      if kw.get('name_v') == 'False' or kw.get('phone_v') == 'False' :
        pass

      else:
        if kw.get('nationality') == 'sd':
          partner = request.env['res.partner'].sudo().create({
          'first_name':  kw.get('first_name'),
          'second_name': kw.get('second_name') ,
          'third_name':  kw.get('third_name'),
          'forth_name': kw.get('forth_name'),
          'national_number': kw.get('national_number'),
          'zakat_state': kw.get('state_id'),
          'phone': kw.get('phone'),
          # 'passport': '',
          'birth_date': kw.get('birth_date'),
          # 'city': kw.get('city'),
          'nationality': kw.get('nationality'),
          # 'local_state_id': kw.get('local_state'),
          # 'admin_unit': kw.get('administrative_unit'),
          'job': kw.get('job'),
          # 'house_no': kw.get('house_no'),
          # 'Village': kw.get('village'),
          'zakat_partner':'TRUE',
          })


        if kw.get('nationality') == 'other':
          partner = request.env['res.partner'].sudo().create({
          'first_name':  kw.get('first_name'),
          'second_name': kw.get('second_name') ,
          'third_name':  kw.get('third_name'),
          'forth_name': kw.get('forth_name'),
          # 'national_number': '',
          'zakat_state': kw.get('state_id'),
          'phone': kw.get('phone'),
          'passport': kw.get('passport'),
          'birth_date': kw.get('birth_date'),
          # 'city': kw.get('city'),
          'nationality': kw.get('nationality'),
          # 'local_state_id': kw.get('local_state'),
          # 'admin_unit': kw.get('administrative_unit'),
          'job': kw.get('job'),
          # 'house_no': kw.get('house_no'),
          # 'Village': kw.get('village'),
          'zakat_partner':'TRUE',
          })

        req = request.env['zakat.federaltreatment.request'].sudo().create({
          'first_name':  kw.get('first_name'),
          'second_name': kw.get('second_name') ,
          'third_name':  kw.get('third_name'),
          'forth_name': kw.get('forth_name'),
          'partner_id' :partner.id,
          'type': kw.get('req_type') ,
          'birth_date':  kw.get('birth_date'),
          'gender': kw.get('gender'),
          'phone': kw.get('phone'),
          'zakat_state': kw.get('state_id'),
          # 'national_number': kw.get('national_number'),
          'treatment_amount': kw.get('treatment_amount'),
          'note': kw.get('note'),
          # 'bill': kw.get('bill'),
          # 'medical': kw.get('medical'),
          # 'review': kw.get('review'),
          # 'check': kw.get('check'),
          # 'commission': kw.get('commission'),
          # 'abroad_cost': kw.get('abroad_cost'),
          # 'passport_co': kw.get('passport_co'),
          # 'tickets': kw.get('tickets'),
          # 'visa': kw.get('visa'),
          # 'conversion_replacement': kw.get('conversion_replacement'),
          'website_request_validate':True,
          
          })
        if kw.get('req_type') == 'it':
          if kw.get('attachment1',False):
            Attachments = request.env['ir.attachment']
            name = kw.get('attachment1').filename      
            file = kw.get('attachment1')
            attachment = file.read() 
            attachment_id = Attachments.sudo().create({
                'name':name,
                'datas_fname': name,
                'res_name': name,
                'type': 'binary',   
                'res_model': 'zakat.federaltreatment.request',
                'res_id':req.id,
                'datas': base64.b64encode(attachment),
            })

          if kw.get('attachment2',False):
            Attachments = request.env['ir.attachment']
            name = kw.get('attachment2').filename      
            file = kw.get('attachment2')
            attachment = file.read() 
            attachment_id = Attachments.sudo().create({
                'name':name,
                'datas_fname': name,
                'res_name': name,
                'type': 'binary',   
                'res_model': 'zakat.federaltreatment.request',
                'res_id':req.id,
                'datas': base64.b64encode(attachment),
            })

          if kw.get('attachment3',False):
            Attachments = request.env['ir.attachment']
            name = kw.get('attachment3').filename      
            file = kw.get('attachment3')
            attachment = file.read() 
            attachment_id = Attachments.sudo().create({
                'name':name,
                'datas_fname': name,
                'res_name': name,
                'type': 'binary',   
                'res_model': 'zakat.federaltreatment.request',
                'res_id':req.id,
                'datas': base64.b64encode(attachment),
            })

          if kw.get('attachment4',False):
            Attachments = request.env['ir.attachment']
            name = kw.get('attachment4').filename      
            file = kw.get('attachment4')
            attachment = file.read() 
            attachment_id = Attachments.sudo().create({
                'name':name,
                'datas_fname': name,
                'res_name': name,
                'type': 'binary',   
                'res_model': 'zakat.federaltreatment.request',
                'res_id':req.id,
                'datas': base64.b64encode(attachment),
            })
        if kw.get('req_type') == 'at':
          if kw.get('attachment5',False):
            Attachments = request.env['ir.attachment']
            name = kw.get('attachment5').filename      
            file = kw.get('attachment5')
            attachment = file.read() 
            attachment_id = Attachments.sudo().create({
                'name':name,
                'datas_fname': name,
                'res_name': name,
                'type': 'binary',   
                'res_model': 'zakat.federaltreatment.request',
                'res_id':req.id,
                'datas': base64.b64encode(attachment),
            })

          if kw.get('attachment6',False):
            Attachments = request.env['ir.attachment']
            name = kw.get('attachment6').filename      
            file = kw.get('attachment6')
            attachment = file.read() 
            attachment_id = Attachments.sudo().create({
                'name':name,
                'datas_fname': name,
                'res_name': name,
                'type': 'binary',   
                'res_model': 'zakat.federaltreatment.request',
                'res_id':req.id,
                'datas': base64.b64encode(attachment),
            })

          if kw.get('attachment7',False):
            Attachments = request.env['ir.attachment']
            name = kw.get('attachment7').filename      
            file = kw.get('attachment7')
            attachment = file.read() 
            attachment_id = Attachments.sudo().create({
                'name':name,
                'datas_fname': name,
                'res_name': name,
                'type': 'binary',   
                'res_model': 'zakat.federaltreatment.request',
                'res_id':req.id,
                'datas': base64.b64encode(attachment),
            })

          if kw.get('attachment8',False):
            Attachments = request.env['ir.attachment']
            name = kw.get('attachment8').filename      
            file = kw.get('attachment8')
            attachment = file.read() 
            attachment_id = Attachments.sudo().create({
                'name':name,
                'datas_fname': name,
                'res_name': name,
                'type': 'binary',   
                'res_model': 'zakat.federaltreatment.request',
                'res_id':req.id,
                'datas': base64.b64encode(attachment),
            })
          
          if kw.get('attachment9',False):
            Attachments = request.env['ir.attachment']
            name = kw.get('attachment9').filename      
            file = kw.get('attachment9')
            attachment = file.read() 
            attachment_id = Attachments.sudo().create({
                'name':name,
                'datas_fname': name,
                'res_name': name,
                'type': 'binary',   
                'res_model': 'zakat.federaltreatment.request',
                'res_id':req.id,
                'datas': base64.b64encode(attachment),
            })

          if kw.get('attachment10',False):
            Attachments = request.env['ir.attachment']
            name = kw.get('attachment10').filename      
            file = kw.get('attachment10')
            attachment = file.read() 
            attachment_id = Attachments.sudo().create({
                'name':name,
                'datas_fname': name,
                'res_name': name,
                'type': 'binary',   
                'res_model': 'zakat.federaltreatment.request',
                'res_id':req.id,
                'datas': base64.b64encode(attachment),
            })

        req_id = request.env['zakat.federaltreatment.request'].sudo().search([('id','=',req.id)])

        if partner:
          return request.render("federal_website.federal_thanks",{'req_ref':req_id.code , 'connection_reset':kw.get('connection_reset')})

        else:
          return request.render("federal_website.federal_request")
    except:
      pass
  
  # @http.route('/website/reset_templates', type='http', auth='user', methods=['POST'], website=True)
  #   def reset_template(self, templates, redirect='/'):
  #       templates = request.httprequest.form.getlist('templates')
  #       modules_to_update = []
  #       for temp_id in templates:
  #           view = request.env['ir.ui.view'].browse(int(temp_id))
  #           if view.page:
  #               continue
  #           view.model_data_id.write({
  #               'noupdate': False
  #           })
  #           if view.model_data_id.module not in modules_to_update:
  #               modules_to_update.append(view.model_data_id.module)

  #       if modules_to_update:
  #           modules = request.env['ir.module.module'].sudo().search([('name', 'in', modules_to_update)])
  #           if modules:
  #               modules.button_immediate_upgrade()
  #       return request.redirect(redirect)
