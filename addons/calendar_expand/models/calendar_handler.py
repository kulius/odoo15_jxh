# -*- coding:utf-8 -*-
from odoo import api, models, fields


class CalendarHandler(models.Model):
    _name = 'calendar.handler'
    _description = '處理單位/客戶簡稱'

    name = fields.Char(string='名稱', required=True)
