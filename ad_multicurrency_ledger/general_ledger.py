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

import time
from lxml import etree

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp.tools import float_compare
from openerp.report import report_sxw
import openerp
from operator import attrgetter


class general_ledger(osv.osv):
    _name = "general.ledger"
    
    _description = "General Ledger for Multicurrency"
    
    _domain_currency = []
    
    _columns = {
                    'name'                   : fields.char("Ref"),
                    'account_id'             : fields.many2one('account.account','Perkiraan',required=True),
                    'date_from'              : fields.date('Dari Tanggal',required=True),
                    'date_to'                : fields.date('Ke Tanggal',required=True),
                    'currency_id'            : fields.many2one('res.currency', 'Currency', domain=[('id', 'in', _domain_currency)]),
                    'line_ids'               : fields.one2many('general.ledger.line', 'ledger_id', 'Transaction List', ),
                    'company_id'             : fields.many2one('res.company', 'Company'),
                }
    
    def _get_saldoawal(self,cr, uid, account_id, date_created):
        debit = 0
        credit = 0
        account = self.pool.get('account.account').browse(cr, uid, account_id)
        
        move_ids = self.pool.get('account.move.line').search(cr,uid,[
                                                                                 ('account_id', '=', account_id),
                                                                                 ('date_created','<',date_created),
                                                                                 ('state', '=', 'valid')
                                                                        ]
                                                      )
        move_data = self.pool.get("account.move.line").browse(cr,uid,move_ids)
        saldo = 0
        if move_data:
            for mv in move_data:
                debit += mv.debit
                credit += mv.credit
        if account.user_type.report_type=='asset' or account.user_type.report_type=='expense':
            saldo = debit - credit
        elif account.user_type.report_type=='income' or account.user_type.report_type=='liability':
            saldo = credit - debit
            
            
        return saldo
    
    
    def _get_move(self, cr, uid, account_id, date_from, date_to):
        res =[]
#        print "USER ID NYA ADALAH : ", form['user_id'][0]
#        journal = self.pool.get('account.journal').browse(cr,uid,form['journal_id'][0])
#        account_id = journal.default_debit_account_id.id
        move_ids = self.pool.get('account.move.line').search(cr, uid,[
                                                                         ('account_id', '=', account_id),
                                                                         ('date_created','>=',date_from),
                                                                         ('date_created','<=',date_to),
                                                                         ('state', '=', 'valid')
                                                                        ]
                                                      )
        move_data = self.pool.get("account.move.line").browse(cr, uid,move_ids)
#        print "MOVE DATA NYA ADALAH....: ", move_data
        move_data2 = [x for x in move_data]
        move_data2.sort(key = attrgetter('date', 'id'), reverse = False)
        return move_data2
    
    
    
    
    def _get_saldoawal_currency(self, cr, uid, account_id, date_created, currency_id):
        account = self.pool.get('account.account').browse(cr, uid, account_id)
        
        move_ids = self.pool.get('account.move.line').search(cr,uid,[
                                                                                 ('account_id', '=', account_id),
                                                                                 ('date_created','<',date_created),
                                                                                 ('currency_id', '=', currency_id),
                                                                                 ('state', '=', 'valid')
                                                                        ]
                                                      )
        move_data = self.pool.get("account.move.line").browse(cr,uid,move_ids)
        saldo = 0
        if move_data:
            for mv in move_data:
                saldo += mv.amount_currency
        if account.user_type.report_type=='asset' or account.user_type.report_type=='expense':
            return saldo
        elif account.user_type.report_type=='income' or account.user_type.report_type=='liability':
            if saldo > 0:
                return -saldo
            elif saldo <0:
                return abs(saldo)
        return saldo
            
            
    
    
    def _get_move_currency(self, cr, uid, account_id, date_from, date_to, currency_id ):
        res =[]
#        print "USER ID NYA ADALAH : ", form['user_id'][0]
#        journal = self.pool.get('account.journal').browse(cr,uid,form['journal_id'][0])
#        account_id = journal.default_debit_account_id.id
        move_ids = self.pool.get('account.move.line').search(cr, uid,[
                                                                         ('account_id', '=', account_id),
                                                                         ('date_created','>=',date_from),
                                                                         ('date_created','<=',date_to),
                                                                         ('currency_id','=',currency_id),
                                                                         ('state', '=', 'valid'),
                                                                        ]
                                                      )
        move_data = self.pool.get("account.move.line").browse(cr, uid,move_ids)
#        print "MOVE DATA NYA ADALAH....: ", move_data
        move_data2 = [x for x in move_data]
        move_data2.sort(key = attrgetter('date', 'id'), reverse = False)
        
        return move_data2
    
    
    
    
    def on_change_account_id(self, cr, uid, ids, account_id, context=None):
        res = {}
        if context==None:
            context=context
        account_obj = self.pool.get('account.account')
        if account_id:
            account_data = account_obj.browse(cr, uid, account_id)
            _domain_currency = []
            if account_data.currency_id:
                print "COMPANY CURRENCY..., ", account_data.company_id.currency_id.name
                
#                 self._domain_currency.append(account_data.currency_id.id)
#                 self._domain_currency.append(account_data.company_id.currency_id.id)
                res = {
                       'value'  : {
                                   'name'           : 'General Ledger of ' + account_data.name,
                                   'currency_id'    : account_data.currency_id and account_data.currency_id.id or False,
                                   'company_id'     : account_data.company_id and account_data.company_id.id or False
                                   }
                       }
                
                _domain_currency = [account_data.currency_id.id, account_data.company_id.currency_id.id]
                
            else:
                _domain_currency.append(account_data.company_currency_id.id)
                res = {
                       'value'  : {
                                   'name'           : 'General Ledger of ' + account_data.name,
                                   'currency_id'    : account_data.company_currency_id,
                                   'company_id'     : account_data.company_id and account_data.company_id.id or False
                                   }
                       }
                _domain_currency.append(account_data.company_currency_id.id)
        return res
    
    
    
    def preview_general_ledger(self, cr, uid, ids, context=None):
        print "HIYAAAAAAAAAAAAAAAAAAAAAAAAA...."
        if context==None:
            context=context
        line_obj = self.pool.get('general.ledger.line')
        
        for gl in self.browse(cr, uid, ids, context=context):
            line_del_ids = line_obj.search(cr, uid, [('ledger_id', '=', gl.id)])
            if line_del_ids:
                line_obj.unlink(cr, uid, line_del_ids)
            if gl.currency_id.id==gl.company_id.currency_id.id:
                saldo_awal = self._get_saldoawal(cr, uid,gl.account_id.id, gl.date_from)
                saldo = 0
                val_awal = {
                            'name'      : "Begining Balance",
                            'date'      : gl.date_from,
                            'desc'      : "Begining Balance per" + str(gl.date_from),
                            'debit'     : 0,
                            'credit'    : 0,
                            'balance'   : saldo_awal,
                            'ledger_id' : gl.id,
                            'rate'      : 0
                            }
                line_obj.create(cr, uid, val_awal)
                move_data = self._get_move(cr, uid, gl.account_id.id, gl.date_from, gl.date_to)
                for mv in move_data:
                    if mv.account_id.user_type.report_type in ('asset', 'expense'):
                        saldo = saldo_awal + mv.debit - mv.credit
                    elif mv.account_id.user_type.report_type in ('income', 'liability'):
                        saldo = saldo_awal + mv.credit -mv.debit
                    
                    val = {
                            'name'      : mv.name,
                            'date'      : mv.date_created,
                            'desc'      : mv.ref,
                            'debit'     : mv.debit,
                            'credit'    : mv.credit,
                            'balance'   : saldo,
                            'ledger_id' : gl.id,
                            'rate'      : 0
                            }
                    line_obj.create(cr, uid, val)
                    saldo_awal = saldo
            elif gl.currency_id.id  != gl.company_id.currency_id.id:
                saldo_awal = self._get_saldoawal_currency(cr, uid, gl.account_id.id, gl.date_from, gl.currency_id.id)
                saldo = 0
                val_awal = {
                            'name'      : "Begining Balance",
                            'date'      : gl.date_from,
                            'desc'      : "Begining Balance per" + str(gl.date_from),
                            'debit'     : 0,
                            'credit'    : 0,
                            'balance'   : saldo_awal,
                            'ledger_id' : gl.id,
                            'rate'      : 0
                            }
                line_obj.create(cr, uid, val_awal)
                move_data = self._get_move_currency(cr, uid, gl.account_id.id, gl.date_from, gl.date_to, gl.currency_id.id)
                for mv in move_data:
                    ccy_debit = 0
                    ccy_credit = 0
                    rate = 0
                    if mv.amount_currency > 0 :
                        ccy_debit = mv.amount_currency
                        rate = mv.debit/mv.amount_currency
                    elif mv.amount_currency < 0 :
                        ccy_credit = abs(mv.amount_currency)
                        rate = mv.credit/abs(mv.amount_currency)
                         
                    if mv.account_id.user_type.report_type in ('asset', 'expense'):
                        saldo = saldo_awal + ccy_debit - ccy_credit
                    elif mv.account_id.user_type.report_type in ('income', 'liability'):
                        saldo = saldo_awal + ccy_credit-ccy_debit
                    
                    val = {
                            'name'      : mv.name,
                            'date'      : mv.date_created,
                            'desc'      : mv.ref,
                            'debit'     : ccy_debit,
                            'credit'    : ccy_credit,
                            'balance'   : saldo,
                            'ledger_id' : gl.id,
                            'rate'      : rate
                            }
                    line_obj.create(cr, uid, val)
                    saldo_awal = saldo
        
        return True
    
                
    
    
class general_ledger_line(osv.osv):
    _name = "general.ledger.line"
    _describtion = "Line General Ledger"
    
    _columns = {
                'name'      : fields.char("Ref"),
                'date'      : fields.date('Date'),
                'desc'      : fields.char("Description"),
                'debit'     : fields.float("Debit"),
                'credit'    : fields.float("Credit"),
                'balance'   : fields.float("Balance"),
                'ledger_id' : fields.many2one('general.ledger', 'Ledger', ondelete='cascade'),
                'rate'      : fields.float('Rate')
                
                }
    
    
    
    
    
    
