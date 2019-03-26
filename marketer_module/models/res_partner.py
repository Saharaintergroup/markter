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
# import firebase_admin
# import datetime
# from firebase_admin import credentials
# from firebase_admin import auth
# from firebase_admin import messaging

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
    @api.model
    def create(self, values):
        # cred = CreateCred()
        # user = auth.create_user(
        # email=values['email'],
        # email_verified=False,
        # phone_number=values['phone'],
        # password=values['gaith'],
        # display_name=values['name'],
        # photo_url='http://www.example.com/12345678/photo.png',
        # disabled=False)

        return super(Customer, self).create(values)
    
    # def CreateCred(self):
    #     cred = credentials.Certificate(
    #         {
    #         "type": "service_account",
    #         "project_id": "new-project-441fd",
    #         "private_key_id": "ac6d292af627a2fac5cdc5ae52151d1a8acc8f8f",
    #         "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDXMD8aqNlartYL\n/vBBVicnrqCp4T/FJmkMvUMxsDJC0SKPEZ/PH7/y8E37WnPdrN0I2KjSlfNuG1u9\nH7JUossTKeesJ5KbdPuYdC+ZplM7PeZlpwunyos6pl1FAFUjHzMUiItvXY+t+elD\nhHYYFpWE6xhrlxeu4j4riSn0eIsFtKkAzhISZDyW6SRqKr9iOABAkiTihr48XF4n\nE7nMvJI5ismTPop/AQ/DysctnQW3Bvlq4fnoPX+T1DKxtKAQrIWW6GUB67eZP96R\nRhv8kjhzFKDa14NE9/n05XoQo8BRM1nu4gucedgiKSQetiqcMKm4cnoorMpVz/8C\nAZBofeGJAgMBAAECggEAEpPtvsV5DmUtwZde8qUXeEuRP1ldAg5Q33KvjGijzjT0\nANoKq/0Xu0eX0+15N1gnNQ5PdO7RN15RS0CjSr9LPPpPMAOymo0882qEeYVshh7P\n91K2pOPNpWCbiMuAjimxZUJsl07CisiapOOYtnesrO8HCrLerpCFwYh0ANEvX2yS\n4fs/5xOCBqZrSxTEdgPsJVdAStYfWbZKBuhr4q/Yr9k52DLy3r7dTvxAbTduEwo7\nfjoextbWYvXzD4zaXbhQu1T9hUMNxCLatjGM6jA157OHNFuCtkM4yVG6VjsddlEL\nyfso2k5A9nLBzbBZBhzyKMJa6wpmded25yZJHaDJCQKBgQD1JFDlriVG+OeDD7y7\nyNAtAn4MD7ictHzhUzBLe9gn1OU6VoZnOjh0/8Nizj6qnYSqkFk4f0rn9/jsXoLm\nacFxwqUwxLm772opHo8+8/BKKWiOcii/n3CJWCJwkNcdE0hFfELwKlB9ICcj8W2+\nps110JAmnWvz7nJ0kyDP2enoxwKBgQDguElTvZZqKbRxmK9emR3i7krcXwxKQmRX\nODkXH2fWXPV6LcCYeAODEFU9wb05Dbsz9PmkrkgNE2FhxDjJjXWZaQr4abDlWUT5\nimlDHqlYzNHbNuFM7qYo1AdfphoctPtdENkTDfAEYDjTubf3HQYqU7n7V50SHUGi\nBgkCQe+zLwKBgEjp7Vnzi0jp3cqA0s0z9J9+n0ktH+cUVBSdLr807d0jGK9abw2j\nJom+TTpFSCRtR7mHx9HjIr+OZS7BCcRI7m3MzF+OFASPOI9UdJzv56fXWy8LS417\nefiQC2ZZ3nHae2OXiz1uCJS/DIVHWTIc4P3K9CVYK3TZlpeP73GDSmyfAoGAYsXd\nxScB5Cvsmjmoa4YVstdWpEJK3qEMBaI6xcUSGRDG/Sr7ColF0eft77UmfNtiO1Yk\nHJRWKxknppde9ohs9j9LiSC7ljOEs8J4vf3OJa/xVc9rfCsxcaSwkQQrWg7apW9w\nWoW3x9SbZcSt7boeKaCfkLBT49BkNtk8QHfG6hUCgYBvHLj4kHKRkpFoVWM12NTV\nBtn9LEJXKSojWJ1YilAW+u3JK8YwBdeb/Y8nRILwWLlSCmPUjSpdujCgEM+cOPiy\nmRYdQQLGI7wIJslir8gC3QkibFgmIx0uk4MN+aaNUXueX1OjXTvhAIjHlPzpvB0n\nq2Bnzsv8QEEU5ykB7yyKeQ==\n-----END PRIVATE KEY-----\n",
    #         "client_email": "firebase-adminsdk-j0p1h@new-project-441fd.iam.gserviceaccount.com",
    #         "client_id": "114594193021862535707",
    #         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    #         "token_uri": "https://oauth2.googleapis.com/token",
    #         "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    #         "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-j0p1h%40new-project-441fd.iam.gserviceaccount.com"
    #         }
    #     )
    #     return firebase_admin.initialize_app(cred)


class UsesMarketer(models.Model):
    _inherit = 'res.users'

    is_delivery = fields.Boolean(default=False)
    @api.model
    def search_read(self, domain=None, fields=None, offset=0,limit=None, order=None):
        if self._context.get('is_portal') == True:
            domain = [('groups_id','=',9)]
        if self._context.get('is_delivery') == True:
            domain = ['&',('groups_id','=',9),('is_delivery','=',True)]
        res = super(UsesMarketer, self).search_read(domain, fields, offset, limit, order)
        return res
    
    @api.model
    def create(self, values):
        if self._context.get('is_portal') == True:
            values['sel_groups_1_9_10'] = 9
        if self._context.get('is_delivery') == True:
            values['is_delivery'] = True
        return super(UsesMarketer, self).create(values)


class EmployeeInPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_agent = fields.Many2one('res.users')


    