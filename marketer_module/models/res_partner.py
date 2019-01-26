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

USER_PRIVATE_FIELDS = []

DEFAULT_CRYPT_CONTEXT = passlib.context.CryptContext(
    # kdf which can be verified by the context. The default encryption kdf is
    # the first of the list
    ['pbkdf2_sha512', 'plaintext'],
    # deprecated algorithms are still verified as usual, but ``needs_update``
    # will indicate that the stored hash should be replaced by a more recent
    # algorithm. Passlib 1.6 supports an `auto` value which deprecates any
    # algorithm but the default, but Ubuntu LTS only provides 1.5 so far.
    deprecated=['plaintext'],
)

class res_parter(models.Model):
    _inherit = 'res.partner'

    longtuide=fields.Char(string="longtuide")
    latutiate=fields.Char(string="latutiate")



    password = fields.Char(
        compute='_compute_password', inverse='_set_password',
        invisible=True, copy=False,store=True,
        help="Keep empty if you don't want the user to be able to connect on the system.")


    def _crypt_context(self):
        """ Passlib CryptContext instance used to encrypt and verify
        passwords. Can be overridden if technical, legal or political matters
        require different kdfs than the provided default.

        Requires a CryptContext as deprecation and upgrade notices are used
        internally
        """
        return DEFAULT_CRYPT_CONTEXT
    def _compute_password(self):
        for user in self:
            user.password = ''
            user.new_password = ''

    def _set_password(self):
        ctx = self._crypt_context()
        for user in self:
            self._set_encrypted_password(user.id, ctx.encrypt(user.password))

    def _set_encrypted_password(self, uid, pw):
        assert self._crypt_context().identify(pw) != 'plaintext'

        self.env.cr.execute(
            'UPDATE res_partner SET password=%s WHERE id=%s',
            (pw, uid)
        )
        self.invalidate_cache(['password'], [uid])