# -*- coding:utf-8 -*-
from odoo import models, fields


class CalendarExpandType(models.Model):
    _name = 'calendar.expand.type'
    _description = '行事曆展開類型'

    name = fields.Char(
        string='名稱',
        required=True,
    )
    handler_id = fields.Many2one(
        comodel_name='calendar.handler',
        string='預設處理單位/客戶簡稱',
        required=True,
    )
    description = fields.Char(string='類型說明')

    line_ids = fields.One2many(
        comodel_name='calendar.expand.line',
        inverse_name='parent_id',
        string='行事曆類型待辦明細'
    )
