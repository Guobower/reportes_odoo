# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError
import datetime
from datetime import datetime as dt
import calendar
import re
from .utils_xlsx import UtilsXlsx
import functools
import json
import calendar
AUX_LEVEL=5



class ReportAccountsEcosoft(models.AbstractModel):
    _name = 'report.account_reports_ecosoft.report_accounts_ecosoft'
    
    # 'date_from': '2018-05-01 15:34:21', 'date_to': '2018-05-21 15:34:21',
    #get_date_range (options):
     #   last_day = calendar.monthrange(int (options['date_from'].split("-")[0]),int (options['date_from'].split("-")[1]))
      #  options['date_from_prev']=options['date_from'].
    
    """@api.model
    def get_accounts(self, options):
        #with_context(date_from_aml=options['date_from'], date_to=options['date_to'], date_from=options['date_from'] )
        print (options)
        accounts = self.env['account.account'].search([])
        lines  = self.env['account.move.line'].read_group([('date', '>=', options['date_from']), ('date', '<=', options['date_to'])],['credit', 'debit', 'balance', 'account_id','date'], groupby='account_id')
        lines_prev  = self.env['account.move.line'].read_group([ ('date', '>=', options['date_from']), ('date', '<=', options['date_to'])],[], groupby='account_id')
        lines_to  = self.env['account.move.line'].read_group([],['credit', 'debit', 'balance', 'account_id','date'], groupby='account_id')
        #print (lines.getkeys())
        print ('accounts: ' + str (accounts))
        print (len(lines_prev))
        print (lines_prev[0]['account_id'])
        print (json.dumps(lines_prev[0], indent=4, sort_keys=True))

        print (len(lines))
        print (lines[0]['account_id'])
        print (json.dumps(lines[0], indent=4, sort_keys=True))

        print (len(lines_to))
        print (lines_to[0]['account_id'])
        print (json.dumps(lines_to[0], indent=4, sort_keys=True))
        accounts_maps=[]
        for i in range (len(lines)) :
            account  = {
                        'code': lines[i]['account_id'][1][:20] ,
                        'name': lines[i]['account_id'][1][20:],
                        'balance': lines[i]['balance'],
                        'debit': lines[i]['debit'],
                        'credit': lines[i]['credit'],
                        'balance_init': lines_prev[i]['debit'] - lines_prev[i]['credit'],
                        }

            accounts_maps.append(account)           
        print (accounts_maps)
        return accounts_maps"""
    
    @api.model
    def get_accounts(self, options, account_ids=None):
        criterias_act = []
        criterias_prev = []
        if account_ids:
            criterias_act.append(('account_id', 'in', account_ids))
            criterias_prev.append(('account_id', 'in', account_ids))
        if data['form'].get('choose_period'):
            criterias_act.append(('date', '>=', options['date_from']), 
                                ('date', '<=', options['date_to'])) 
            criterias_prev.append(('date', '<', options['date_from'])) 

        lines  = self.env['account.move.line'].read_group(criterias_act,['credit', 'debit', 'balance', 'account_id','date'], groupby='account_id')
        lines_prev  = self.env['account.move.line'].read_group(criterias_prev,['credit', 'debit', 'balance', 'account_id','date'], groupby='account_id')
        accounts_maps=[]
        for i in range (len(lines)) :
            account  = {
                        'code': lines[i]['account_id'][1][:20] ,
                        'name': lines[i]['account_id'][1][20:],
                        'balance': lines[i]['balance'],
                        'debit': lines[i]['debit'],
                        'credit': lines[i]['credit'],
                        'balance_init': lines_prev[i]['debit'] - lines_prev[i]['credit'],
                        }

            accounts_maps.append(account)           
        print (accounts_maps)
        return accounts_maps