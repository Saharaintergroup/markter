#-*- coding:utf-8 -*-

##############################################################################
#
#    Copyright (C) Appness Co. LTD **hosam@app-ness.com**. All Rights Reserved
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
from lxml import etree
from odoo.tools.translate import _

class res_parter(models.Model):
    _name = 'mar.partner.complians'

    partner_id=fields.Many2one("res.partner",string="partner")
    discribtion=fields.Char(string="discribtion")
    date=fields.Datetime(string="Date time")

class Visit(models.Model):
    _name = 'customer.visits'

    partner_id = fields.Many2one('res.partner', string="Customer")
    discription=fields.Char(string="discription")
    address = fields.Char(related='partner_id.street',store=True)
    phone_number = fields.Char(related='partner_id.phone', store=True)