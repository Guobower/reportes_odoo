# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError
import datetime
import calendar
from datetime import datetime as dtime
from .utils_xlsx import UtilsXlsx
import functools 
from .account_ecosoft import ReportAccountsEcosoft

class ReportLedgerEcosoft(ReportAccountsEcosoft):
    _name = 'report.account_reports_ecosoft.report_ledger_ecosoft'

  
    def calc_data ( self, lista, choose_period, context, month):
        results=[]
        if choose_period:
            for a in lista:
                result={
                    'balance' : a.with_context(context).balance,
                    'name' : a.name,
                    'code' : a.code,
                    'period': month.title(), #a.with_context(context).write_date,
                    'acum' : a.with_context(context).argil_balance_all,
                    'init_balance': a.with_context(context).argil_initial_balance,
                    'credit' : a.with_context(context).credit,
                    'debit' : a.with_context(context).debit
                }
                
                results.append(result)
        else:
            for a in lista:
                result={
                    'balance' : a.balance,
                    'name' : a.name,
                    'code' : a.code,
                    'period': month.title(), #a.write_date,
                    'acum': a.argil_balance_all,
                    'init_balance': a.argil_initial_balance,
                    'credit' : a.credit,
                    'debit' : a.debit                
                }
                results.append(result)
        return results 

    def get_data(self, data):
        context = self._context.copy()        
        level = data['form'].get('level')
        if level == AUX_LEVEL:
                level = 10        
        only_balance = data['form'].get('only_balance')                
        periodo=""
        if choose_period :                
                periodo= data['form'].get('date_from') + ' - ' + data['form'].get('date_to')
        else: 
                periodo = "01/" + datetime.date.today().strftime("%m/%Y") + " - "+ datetime.date.today().strftime("%d/%m/%Y")
                
        account_res = self.get_accounts(data['form'])              
        if only_balance: 
            account_res =filter ( lambda x : ( x['acum'] != 0 or x['init_balance'] != 0 or x['credit'] != 0 or x['debit'] != 0 )  , account_res)      
        docargs = {
           
            'time': time,
            'Accounts': account_res,            
            'periodo': periodo
        }
        return docargs


    @api.model
    def render_html(self, wizard, data=None):
        docargs = self.get_data(data)        
        return self.env['report'].render('account_reports_ecosoft.report_ledger_ecosoft', docargs)

    @api.model
    def get_report_values (self, docids, data): 
        print ('get values')       
        docargs =  self.get_data (data)        
        return docargs

    @api.model
    def _get_csv(self, data=None):        
        docargs =  self.get_data (data)
        headers = ['Cuenta' , 'Nombre', 'Saldo inicial', 'Acumulados', 'Periodo', 'Cargos', 'Abonos', 'Saldo', 'Cargos', 'Abonos']
        csv = '|'.join(headers)
        csv += "\n"
        accounts = docargs['Accounts']        
        if len(accounts) > 0:
            for account in accounts:                        
                csv_row =  account['code'] + '|'+ account['name'] + '|' + str(account['init_balance']) +'|'+ str (account['acum']) \
                            + '|' + str(account['period']) + '|'+ str(account['credit']) +'|'+ str(account['debit']) \
                            + '|' + str(account['balance']) + '|'+ str(account['credit']) +'|'+ str(account['debit']) \
                                        
                csv += csv_row  + "\n"                
        
        return csv

    @api.model
    def _get_xls(self, data=None, workbook=None):
        
        docargs =  self.get_data (data)
        worksheet = workbook.add_worksheet('Balance')
        
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 35)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 15)
        worksheet.set_column('G:G', 15)
        worksheet.set_column('H:H', 15)
        worksheet.set_column('I:I', 15)
        worksheet.set_column('J:J', 15)
        
        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': 1, })
        matrix =map(lambda x: x.split('|'), self._get_csv(data).split('\n'))
        headers=[0,]
        UtilsXlsx.add_matrix(matrix, worksheet, headers, bold)       
    

