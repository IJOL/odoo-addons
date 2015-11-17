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

{
    "name" : "Real State",
    "version" : "1.0",
    "author" : "Acysos S.L.",
    "website" : "www.acysos.com",
    "description": """Add real state management""",
    "license" : "AGPL-3",
    "category" : "Specific Industry Applications",
    "depends" : [
        "base",
        "crm",
        "document",
	"city",
        "document_ftp",
        ],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" :[
        'security/real_state_security.xml',
        'security/ir.model.access.csv',
        'report/generic_list.xml',
        'top_view.xml',
        'partner_view.xml',
        'top_sequence.xml',
        'document_data.xml',
        'company_view.xml',
        'res_user.xml',
        'rental_agreement_sequence.xml',
        'rental_agreement_view.xml',
        'crm_meeting_view.xml',
        ],
    "active": False,
    "installable": True
}