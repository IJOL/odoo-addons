# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (c) 2014-2015 Acysos S.L. (http://acysos.com)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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

from openerp import models, fields, api
from openerp.addons.decimal_precision import decimal_precision as dp


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.one
    @api.depends('sale_id.amount_untaxed', 'sale_id.amount_tax',
                 'sale_id.amount_total')
    def _compute_amount(self):
        if self.sale_id:
            if self.pack_operation_ids:
                for operation in self.pack_operation_ids:
                    self.amount_untaxed += operation.sale_subtotal
                    self.amount_tax += operation.sale_taxes
                self.amount_total = self.amount_untaxed + self.amount_tax
            else:
                for move in self.move_lines:
                    self.amount_untaxed += move.sale_subtotal
                    self.amount_tax += move.sale_taxes
                self.amount_total = self.amount_untaxed + self.amount_tax

    amount_untaxed = fields.Float(compute='_compute_amount',
                                  digits_compute=dp.get_precision('Account'),
                                  string='Untaxed Amount')
    amount_tax = fields.Float(compute='_compute_amount',
                              digits_compute=dp.get_precision('Account'),
                              string='Taxes')
    amount_total = fields.Float(compute='_compute_amount',
                                digits_compute=dp.get_precision('Account'),
                                string='Total')
    stock_valued = fields.Boolean(string="Stock Valued")


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.one
    @api.depends('procurement_id.sale_line_id',
                 'procurement_id.sale_line_id.price_unit',
                 'procurement_id.sale_line_id.discount',
                 'procurement_id.sale_line_id.price_subtotal',
                 'procurement_id.sale_line_id.price_reduce',
                 'procurement_id.sale_line_id.order_id')
    def _sale_prices(self):
        if self.procurement_id.sale_line_id:
            sale_line = self.procurement_id.sale_line_id
            self.sale_taxes = round(
                (sale_line.order_id._amount_line_tax(sale_line) /
                 sale_line.product_uom_qty) * self.product_qty, 2) if sale_line.product_uom_qty else 0.00
            self.sale_price_untaxed = sale_line.price_reduce
            self.sale_price_unit = sale_line.price_unit
            self.sale_discount = sale_line.discount
            self.sale_subtotal = round(sale_line.price_reduce *
                                       self.product_qty, 2)
        else:
            self.sale_taxes = 0
            self.sale_price_untaxed = 0
            self.sale_subtotal = 0
            self.sale_price_unit = 0
            self.sale_discount = 0

    sale_subtotal = fields.Float(
        compute='_sale_prices', digits_compute=dp.get_precision('Account'),
        string='Subtotal')
    sale_price_unit = fields.Float(compute='_sale_prices',
                                   digits_compute=dp.get_precision('Account'),
                                   string='Price')
    sale_price_untaxed = fields.Float(
        compute='_sale_prices', digits_compute=dp.get_precision('Account'),
        string='Price Untaxed')
    sale_taxes = fields.Float(compute='_sale_prices',
                              digits_compute=dp.get_precision('Account'),
                              string='Total Taxes')
    sale_discount = fields.Float(compute='_sale_prices',
                                 digits_compute=dp.get_precision('Account'),
                                 string='Discount (%)')


class StockPackOperation(models.Model):
    _inherit = "stock.pack.operation"

    @api.one
    def _sale_prices(self):
        self.sale_taxes = 0
        self.sale_price_untaxed = 0
        self.sale_subtotal = 0
        self.sale_price_unit = 0
        self.sale_discount = 0
        if self.linked_move_operation_ids:
            move = self.linked_move_operation_ids[0].move_id
            if move.procurement_id.sale_line_id:
                self.sale_taxes = round((move.sale_taxes / move.product_qty) *
                                        self.product_qty, 2)
                self.sale_price_untaxed = move.sale_price_untaxed
                self.sale_price_unit = move.sale_price_unit
                self.sale_discount = move.sale_discount
                self.sale_subtotal = round(self.sale_price_untaxed *
                                           self.product_qty, 2)

    sale_subtotal = fields.Float(
        compute='_sale_prices', digits_compute=dp.get_precision('Account'),
        string='Subtotal')
    sale_price_unit = fields.Float(compute='_sale_prices',
                                   digits_compute=dp.get_precision('Account'),
                                   string='Price')
    sale_price_untaxed = fields.Float(
        compute='_sale_prices', digits_compute=dp.get_precision('Account'),
        string='Price Untaxed')
    sale_taxes = fields.Float(compute='_sale_prices',
                              digits_compute=dp.get_precision('Account'),
                              string='Total Taxes')
    sale_discount = fields.Float(compute='_sale_prices',
                                 digits_compute=dp.get_precision('Account'),
                                 string='Discount (%)')
