# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError
import datetime
import calendar
import re
from utils_xlsx import UtilsXlsx

AUX_LEVEL=5



class ReportTrialBalanceEcosoft(models.AbstractModel):
    _name = 'report.account.report_trialbalance_ecosoft'

    
    
    def _get_accounts(self, account, account_list=[], depth=0, level=5):
        """ compute the balance, debit and credit for the provided accounts
            :Arguments:
                `accounts`: list of accounts record,
                `display_account`: it's used to display either all accounts or those accounts which balance is > 0
            :Returns a list of dictionary of Accounts with following key and value
                `name`: Account name,
                `code`: Account code,
                `credit`: total amount of credit,
                `debit`: total amount of debit,
                `balance`: total amount of balance,
        """
        #print depth
        if depth > 10:
            raise UserError(_("Depth 10 reach."))
        
        #print account.name +  str (account.id)
        childs = self.env['account.account'].search([('parent_id','=',account.id)], order="code asc")
        if  depth  < level:
            if childs:
                depth = depth + 1
                for acc in childs:
                    account_list.append(acc.id)
                    self._get_accounts(acc, account_list, depth, level)
            
        return account_list


    def get_data (self, data):
        context = self._context.copy()
        
        level = data['form'].get('level')
        if level == AUX_LEVEL:
            level = 10
        #print 'level:  ' + str (level) + ' -- ' + str(type(level))
        only_balance = data['form'].get('only_balance')
        #print 'only_balance:  ' + str (only_balance) + ' -- ' + str(type(only_balance))
        period_data = data['form'].get('period_id', False)
        choose_period = data['form'].get('choose_period', False)
        with_period = period_data and choose_period
        
        periodo=""
        if choose_period :
            context.update({'periods': [period_data[0]]})
            #print type (period_data[1])
            fecha = period_data[1].split('/')
            days = calendar.monthrange(int (fecha[1]), int (fecha[0]))
            last_day = days[1]  
            periodo="01/" + period_data[1] + " - "+ str(last_day) + "/" +  period_data[1]
        else: 
            periodo = "01/" + datetime.date.today().strftime("%m/%Y") + " - "+ datetime.date.today().strftime("%d/%m/%Y")
        
        account = self.env['account.account'].search([('parent_id','=',False)])
        if len(account) != 1 and False:
            raise UserError(_("No hay una cuenta padre unica."))
        
        
        account_list = []
        self._get_accounts(account[0], account_list, 0, level)
        accounts = self.env['account.account'].browse(account_list)
        

        if period_data:
            totales = {
            'argil_initial_balance': account[0].with_context(context).argil_initial_balance,
            'debit': account[0].with_context(context).debit,
            'credit': account[0].with_context(context).credit,
            }
        else:
            totales = {
            'argil_initial_balance': account[0].argil_initial_balance,
            'debit': account[0].debit,
            'credit': account[0].credit,
            }
        totales['balance'] = totales['argil_initial_balance'] + totales['debit'] - totales['credit']
        account_res = []
        for account in accounts:
            res = dict((fn, 0.0) for fn in ['argil_initial_balance','credit', 'debit', 'balance'])
            currency = account.currency_id and account.currency_id or account.company_id.currency_id
            res['level'] = account.level
            res['code'] = account.code
            res['name'] = account.name
            
            if with_period:
                res['argil_initial_balance'] = account.with_context(context).argil_initial_balance
                res['debit'] = account.with_context(context).debit
                res['credit'] = account.with_context(context).credit
            else:
                res['argil_initial_balance'] = account.argil_initial_balance
                res['debit'] = account.debit
                res['credit'] = account.credit

            if re.match('[2|3|4].', account.code):  # pasa a negativos las cuentas de pasivo
                #print  'code ' + account.code   
                res['balance'] = -(res['argil_initial_balance'] + res['debit'] - res['credit'])
                res['argil_initial_balance'] = -(res['argil_initial_balance'])
            else:
                res['balance'] = res['argil_initial_balance'] + res['debit'] - res['credit']

            account_res.append(res)
        
        if only_balance: 
            account_res =filter ( lambda x : ( x['argil_initial_balance'] != 0 or  x['debit'] != 0 or x['credit'] != 0 or x['balance'] != 0 )  , account_res)   
            
        #print 'account_res' + str (len (account_res)  )
        #self.model = self.env.context.get('active_model')
        #docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        
        docargs = {
            #'doc_ids': self.ids,
            #'doc_model': self.model,
            #'data': data['form'],
            #'docs': docs,
            'time': time,
            'Accounts': account_res,
            'totales': totales,
            'periodo': periodo
        }

        return docargs



    @api.model
    def render_html(self, wizard, data=None):       
        docargs =  self.get_data (data)
        return self.env['report'].render('account_reports_ecosoft.report_trialbalance_ecosoft', docargs)

    @api.model
    def _get_csv(self, data=None):
        print 'en trial balance'
        print data         
        docargs =  self.get_data (data)
        headers = ['Cuenta contable','Nombre', 'Nivel', 'Saldo Ant.', 'Cargos', 'Abonos', 'Saldo Actual']
        csv = '|'.join(headers)
        csv += "\n"
        accounts = docargs['Accounts']
        
        if len(accounts) > 0:
            for account in accounts:                        
                csv_row =  account['code'] + '|'+ account['name'] + '|' \
                           + str(account['level']) +'|'+ str (account['argil_initial_balance']) \
                           + '|'+ str(account['debit']) +'|'+ str(account['credit']) +'|'+ str(account['balance'])                
                csv += csv_row  + "\n"                
        csv +=  ' Totales |............ | |' + str (round (docargs['totales']['argil_initial_balance'],2)) + '|' \
                + str (round (docargs['totales']['debit'],2)) + '|' + str(round(docargs['totales']['credit'],2)) + '|' + str(round(docargs['totales']['balance'],2)) + "\n"        
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
        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': 1, })        
        matrix =map(lambda x: x.split('|'), self._get_csv(data).split('\n'))
        headers=[0,(len(matrix)-2)]                
        UtilsXlsx.add_matrix(matrix, worksheet, headers, bold)  
        
                
        
        
