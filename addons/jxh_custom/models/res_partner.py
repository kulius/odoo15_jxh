# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_name(self):
        name = super(ResPartner, self)._get_name()
        if self.phone:
            name = self.phone+" " + name
        return name

    @api.depends('is_company', 'name', 'parent_id.display_name', 'type', 'company_name', 'phone')
    def _compute_display_name(self):
        diff = dict(show_address=None, show_address_only=None, show_email=None, html_format=None, show_vat=None)
        names = dict(self.with_context(**diff).name_get())
        for partner in self:
            partner.display_name = names.get(partner.id)
            if self.phone:
                partner.display_name = self.phone+" "+ partner.display_name



