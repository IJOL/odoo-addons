# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2013 Acysos S.L. (http://acysos.com) All Rights Reserved.
#                       Ignacio Ibeas <ignacio@acysos.com>
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv, fields
import tools
import os

class product_meter(osv.osv):
    _inherit = "product.meter"
    
    def _floor_get(self,cr,uid,ids,name,arg,context={}):
        res={}
        for meter in self.browse(cr,uid,ids,context):
            res[meter.id] = meter.partner_id.floor
        return res
    
    _columns = {
        'floor': fields.function(_floor_get, method=True, store=True, type='char', size=64, string='Floor', readonly=True),
    }
    
    _order = "floor asc"
    
product_meter()