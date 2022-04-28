# -*- coding:utf-8 -*-
from odoo import api, models, fields
from odoo.exceptions import UserError
from datetime import date, timedelta

SAT, SUN = 5, 6


class CalendarExpand(models.Model):
    _name = 'calendar.expand'
    _description = '行事曆會議展開'

    name = fields.Char(string='名稱')
    start_date = fields.Date(string='開始日期', required=True)
    expand_type_id = fields.Many2one(
        comodel_name='calendar.expand.type',
        string='行事曆展開類型',
        required=True
    )
    handler_id = fields.Many2one(
        comodel_name='calendar.handler',
        string='處理單位/客戶簡稱',
        required=True
    )
    attendees1 = fields.Many2many(
        comodel_name='res.partner',
        relation='rel_calendar_expand_attendees_primary',
        string='執行者1名單'
    )
    attendees2 = fields.Many2many(
        comodel_name='res.partner',
        relation='rel_calendar_expand_attendees_secondary',
        string='執行者2名單'
    )
    out_attendees1 = fields.Many2many(
        comodel_name='res.partner',
        relation='rel_calendar_expand_out_attendees_primary',
        string='外部窗口1名單'
    )
    out_attendees2 = fields.Many2many(
        comodel_name='res.partner',
        relation='rel_calendar_expand_out_attendees_secondary',
        string='外部窗口2名單'
    )
    calendar_event_ids = fields.One2many(
        comodel_name='calendar.event',
        inverse_name='expand_id',
        string='展開後的行事曆'
    )

    @api.onchange('expand_type_id')
    def _onchange_expand_type(self):
        if not self.expand_type_id:
            return
        else:
            self.handler_id = self.expand_type_id.handler_id

    @staticmethod
    def _name_get(line):
        date_start = line.start_date.strftime('%Y/%m/%d')
        return f'{date_start} : {line.handler_id.name} : {line.expand_type_id.name}'

    def name_get(self):
        return [(line.id, self._name_get(line)) for line in self]

    def combine_partner_ids(self, line):
        partner_ids = self.env['res.partner']

        if line.attendees1:
            partner_ids += self.attendees1

        if line.attendees2:
            partner_ids += self.attendees2

        if line.out_attendees1:
            partner_ids += self.out_attendees1

        if line.out_attendees2:
            partner_ids += self.out_attendees2

        return [(6, 0, partner_ids.ids)]

    @staticmethod
    def _calc_workday(date_start: date, add_days: int, later: bool = False) -> (date, date):
        """ 依照 add_days 來推算 date_start 與 date_stop (不包含特殊假日)
            :param date date_start : 起始日期
            :param int add_days : 經過多少工作天
            :param boolean later : 遇週末後推日期

            思路:
                先把起始日若為六、日時依照前推或後推規則先進行偏移，
                扣除第一個禮拜的工作天(remain_workdays = add_days - (5 - weekday))
                    - 若起始日為禮拜一 (weekday = 0)，則第一個禮拜會有 5 個工作天 [5 = 5 - 0]
                    - 若起始日為禮拜五 (weekday = 4)，則第一個禮拜會有 1 個工作天 [1 = 5 - 4]
                接著把剩餘階段天數整除 5(一週五天工作天)
                    - 其(商 * 2) 為會經過幾組六、日
                    - 其餘若大於 0 則會多經過一組六、日
                最後把起始日期 + 工作階段 + 周末偏移 - 1(階段起始天也算)，就是結束日期
        """

        weekday = date_start.weekday()
        if weekday == SAT:
            date_start += timedelta(2 if later else -1)
            weekday = date_start.weekday()
        elif weekday == SUN:
            date_start += timedelta(1 if later else -2)
            weekday = date_start.weekday()

        if add_days == 0:
            return date_start, date_start
        elif add_days > 0:
            remain_workdays = add_days - (5 - weekday)
            if remain_workdays > 0:
                weekend_offset = (remain_workdays // 5) * 2
                if remain_workdays % 5:
                    weekend_offset += 2
            else:
                weekend_offset = 0

            date_stop = date_start + timedelta(add_days + weekend_offset - 1)
            return date_start, date_stop
        else:
            remain_workdays = add_days + (weekday + 1)
            if remain_workdays < 0:
                weekend_offset = (remain_workdays // 5) * 2
                if remain_workdays % 5:
                    weekend_offset -= 2
            else:
                weekend_offset = 0

            date_stop = date_start + timedelta(add_days + weekend_offset + 1)
            return date_start, date_stop

    def expand_to_event(self):
        """ 展開至 calendar.event """
        if not self.expand_type_id.line_ids:
            raise UserError('請增加展開明細')

        history_event = self.env['calendar.event']
        prev_event = self.env['calendar.event']
        date_start = self.start_date
        handler_name = self.handler_id.name
        for line in self.expand_type_id.line_ids:
            date_start, date_stop = self._calc_workday(date_start, line.add_date)
            #date_stop = date_start + timedelta(line.add_date)
            prev_event = prev_event.create({
                'name': f'{date_stop.strftime("%Y/%m/%d")} : {handler_name} : {line.name}',
                'partner_ids': self.combine_partner_ids(line),
                'start_date': date_stop,
                'stop_date': date_stop,
                'allday': True,
                'expand_id': self.id,
                'expand_line_id': line.id,
                'description': line.detail or '',
            })
            history_event += prev_event

        self.calendar_event_ids += history_event
        return True

    def revert_expand_event(self):
        """ 刪除所有關聯的 calendar.event """
        self.calendar_event_ids.unlink()
        return True
