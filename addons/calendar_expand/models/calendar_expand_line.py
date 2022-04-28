# -*- coding:utf-8 -*-
from odoo import api, models, fields


class CalendarExpandLine(models.Model):
    _name = 'calendar.expand.line'
    _description = '行事曆細項設定'

    name = fields.Char(string='行事曆內容', required=True)
    detail = fields.Html(string='說明')
    add_date = fields.Integer(string='階段天數', required=True)
    attendees1 = fields.Boolean(string='載入執行者1為與會者', default=False)
    attendees2 = fields.Boolean(string='載入執行者2為與會者', default=False)
    out_attendees1 = fields.Boolean(string='載入外部窗口1為與會者', default=False)
    out_attendees2 = fields.Boolean(string='載入外部窗口2為與會者', default=False)
    holiday_adjust = fields.Selection(
        selection=[('before', '前推'), ('after', '後推')],
        string='遇假日之行事曆時程調整',
    )
    is_important = fields.Boolean(string='為重點提醒客戶事項', default=False)
    parent_id = fields.Many2one(comodel_name='calendar.expand.type', string='主檔')
