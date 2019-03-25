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
import passlib.context
import hashlib

USER_PRIVATE_FIELDS = []


class Customer(models.Model):
    _inherit = 'res.partner'

    longtude = fields.Float()
    lutude = fields.Float()
    gaith = fields.Char(default="123")
    persone_type = fields.Selection([
        ('customer','Customer'),
        ('prospect','Prospect'),
        ('delivery','Delivery')
    ],default='prospect')


class UsesMarketer(models.Model):
    _inherit = 'res.users'

    @api.model
    def search_read(self, domain=None, fields=None, offset=0,limit=None, order=None):
        if self._context.get('is_portal') == True:
            domain = [('groups_id','=',9)]
        res = super(UsesMarketer, self).search_read(domain, fields, offset, limit, order)
        return res
    
    @api.model
    def create(self, values):
        if self._context.get('is_portal') == True:
            values['sel_groups_1_9_10'] = 9
        return super(UsesMarketer, self).create(values)