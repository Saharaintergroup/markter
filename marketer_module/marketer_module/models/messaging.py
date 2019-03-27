#-*- coding:utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
from lxml import etree
from odoo.tools.translate import _
import uuid


class Messages(models.Model):
    _name = 'marketer.messages'

    from_id = fields.Many2one('res.partner')
    to_id = fields.Many2one('res.partner')
    text = fields.Text(size=250)
    date = fields.Datetime(default=datetime.now())
    seen = fields.Boolean(default=False)
    channel_id = fields.Many2one('marketer.channel')
    uuid = fields.Char(compute='Uuid')

    def Uuid(self):
        var = str(uuid.uuid1())
        # print("\n\n\n",var,"\n\n\n")
        for rec in self:
            rec.uuid = var
        

class Channel(models.Model):
    _name = 'marketer.channel'

    from_id = fields.Many2one('res.partner')
    to_id = fields.Many2one('res.partner')
    date = fields.Datetime(default=datetime.now())
    messages_ids = fields.One2many('marketer.messages','channel_id')