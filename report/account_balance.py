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
from .account_ecosoft import ReportAccountsEcosoft
from  functools import reduce


AUX_LEVEL=5



class ReportTrialBalanceEcosoft(ReportAccountsEcosoft):
    _name = 'report.account_reports_ecosoft.report_trialbalance_ecosoft'
    

    def get_data (self, data):
        context = self._context.copy()        
        level = data['form'].get('level')
        if level == AUX_LEVEL:
                level = 10   
        choose_period = data['form'].get('choose_period')        
        only_balance = data['form'].get('only_balance')                
        periodo=""
        if choose_period :                
                periodo= data['form'].get('date_from') + ' - ' + data['form'].get('date_to')
        else: 
                periodo = "01/" + datetime.date.today().strftime("%m/%Y") + " - "+ datetime.date.today().strftime("%d/%m/%Y")
                
        account_res = self.get_accounts(data['form'])
        totales = {
                'balance': round (reduce(lambda x, y : x + y , [ c ['balance'] for c in account_res ]),2), 
                'debit': round ( reduce(lambda x, y : x + y , [ c ['debit'] for c in account_res ]), 2),  
                'credit': round (reduce(lambda x, y : x + y , [ c ['credit'] for c in account_res ]),2), 
                'balance_init': round (reduce(lambda x, y : x + y , [ c ['balance_init'] for c in account_res ]),2),                 
            }
        if account_res:   
            docargs = {                
                'time': time,
                'Accounts': account_res,
                'totales': totales,
                'periodo': periodo
            }



        return docargs



    @api.model
    def render_html(self, wizard, data=None):        
        docargs =self.get_data (data)
        return self.env['report'].render('account_reports_ecosoft.report_trialbalance_ecosoft', docargs)

    @api.model
    def get_report_values (self, docids, data): 
        print ('get values')        
        docargs =self.get_data (data)        
        return docargs

    @api.model
    def _get_csv(self, data=None):
        #print 'en trial balance'
        #print data            
        docargs =self.get_data (data)
        headers = ['Cuenta contable','Nombre', 'Nivel', 'Saldo Ant.', 'Cargos', 'Abonos', 'Saldo Actual']
        csv = '|'.join(headers)
        csv += "\n"
        if docargs:
                accounts = docargs['Accounts']
                
                if len(accounts) > 0:
                    for account in accounts:                                
                        csv_row =account['code'] + '|'+ account['name'] + '|' \
                                        + str(account['level']) +'|'+ str (account['balance']) \
                                        + '|'+ str(account['debit']) +'|'+ str(account['credit']) +'|'+ str(account['balance'])                    
                        csv += csv_row+ "\n"                    
                csv +=' Totales |............ | |' + str (round (docargs['totales']['balance'],2)) + '|' \
                        + str (round (docargs['totales']['debit'],2)) + '|' + str(round(docargs['totales']['credit'],2)) + '|' + str(round(docargs['totales']['balance'],2)) + "\n"        
        return csv


    @api.model
    def _get_xls(self, data=None, workbook=None):
            
        docargs =self.get_data (data)
        worksheet = workbook.add_worksheet('Balance')
        
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 35)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 15)
        worksheet.set_column('G:G', 15)        
        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': 1, })        
        matrix =map(lambda x: x.split('|'), self._get_csv(data).split('\n'))
        headers=[0,(len(matrix)-2)]                    
        UtilsXlsx.add_matrix(matrix, worksheet, headers, bold)
        
                    
        
        
