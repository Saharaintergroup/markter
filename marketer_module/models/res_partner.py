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


class res_parter(models.Model):
    _inherit = 'res.partner'

    longtuide=fields.Char(string="longtuide")
    latutiate=fields.Char(string="latutiate")
    password = fields.Char()

    # overwrite create function 
    @api.model
    def create(self, vals):
        vals['password'] = hash(vals['password'])
        return super(res_parter, self).create(vals)
 
    # the hashing function 
    def hash(password):
        password = hashlib.md5()
        password.hexdigest()
        return password