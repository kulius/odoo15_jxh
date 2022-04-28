# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    partnerline_ids = fields.One2many(comodel_name="sale.order.partnerline",
                                                 inverse_name="order_id", string="歷史銷售資料", required=False, )

    @api.onchange('partner_id')
    def onchange_partner_id_salehistory(self):
        if not self.partner_id:
            return
        product_record = self.env['sale.order.line'].search([('order_partner_id', '=', self.partner_id.id)])
        self.write({'partnerline_ids': [(5, 0, 0)]})
        if product_record:
            new_lines = []
            for line in product_record:
                vals = {
                    'order_id': self.id,
                    'sale_order_id': line.order_id.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'price_total': line.price_total,
                }
                new_lines.append((0, 0, vals))
            self.partnerline_ids = new_lines


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

#金屬加工-內製委外成本
class SaleOrderPartnerLine(models.Model):
    _name = 'sale.order.partnerline'
    _description = '客戶歷史訂單'

    order_id = fields.Many2one(comodel_name="sale.order", string="訂單", ondelete='cascade')
    sale_order_id = fields.Many2one(comodel_name="sale.order", string="銷售訂單", ondelete='cascade')
    product_id = fields.Many2one('product.product', string='產品')
    product_uom_qty = fields.Float(string='數量')
    price_unit = fields.Float(string='單價')
    price_total = fields.Float(string='總計')
