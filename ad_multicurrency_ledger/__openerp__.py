# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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


{
    'name': 'Multicurrency General Ledger',
    'version': '1.1',
    'category': 'Accounting',
    'sequence': 24,
    'summary': 'View and Print General Ledger with multicurrency',
    'description': """
        View and Print General Ledger with multicurrency
    """,
    'author': 'Jumeldi',
    'website': 'https://www.odoo.com/page/purchase',
    'images': [],
    'depends': ['account'],
    'data': [
        'general_ledger_view.xml',
        'general_ledger_print.xml'
        
#        'stock_view.xml'
    ],
    'test': [
#        'test/ui/purchase_users.yml',
#        'test/process/run_scheduler.yml',
#        'test/fifo_price.yml',
#        'test/fifo_returns.yml',
        #'test/costmethodchange.yml',
#        'test/process/cancel_order.yml',
#        'test/process/rfq2order2done.yml',
#        'test/process/generate_invoice_from_reception.yml',
#        'test/process/merge_order.yml',
#        'test/process/edi_purchase_order.yml',
#        'test/process/invoice_on_poline.yml',
#        'test/ui/duplicate_order.yml',
#        'test/ui/delete_order.yml',
#        'test/average_price.yml',
    ],
    'demo': [
#        'purchase_order_demo.yml',
#        'purchase_demo.xml',
#        'purchase_stock_demo.yml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
