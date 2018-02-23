# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError
import datetime
import calendar
from datetime import datetime as dtime


class ReportLedgerEcosoft(models.AbstractModel):
    _name = 'report.account.report_ledger_ecosoft'

  
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

    @api.model
    def render_html(self, wizard, data=None):
        context = self._context.copy()
        
        period_data = data['form'].get('period_id', False)
        choose_period = data['form'].get('choose_period', False)
        with_period = period_data and choose_period
        only_balance = data['form'].get('only_balance')
        periodo=""
        month=""
        if choose_period :
            context.update({'periods': [period_data[0]]})
            #print type (period_data[1])
            fecha = period_data[1].split('/')
            days = calendar.monthrange(int (fecha[1]), int (fecha[0]))
            last_day = days[1]  
            periodo="01/" + period_data[1] + " - "+ str(last_day) + "/" +  period_data[1]
            month = dtime.strptime(str(last_day) + "/" +  period_data[1],'%d/%m/%Y').strftime('%B')
        else: 
            periodo = "01/" + datetime.date.today().strftime("%m/%Y") + " - "+ datetime.date.today().strftime("%d/%m/%Y")
            month = dtime.strptime(datetime.date.today().strftime("%d/%m/%Y"),'%d/%m/%Y').strftime('%B')
        
        account = self.env['account.account'].search([('level','=',1)], order="code asc")
        if len(account) != 1 and False:
            raise UserError(_("No hay una cuenta padre unica."))
        
        account_res = self.calc_data(account,choose_period, context, month)
      
        if only_balance: 
            account_res =filter ( lambda x : ( x['acum'] != 0 or x['init_balance'] != 0 or x['credit'] != 0 or x['debit'] != 0 )  , account_res)

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': account_res,            
            'periodo': periodo
        }
        return self.env['report'].render('account_reports_ecosoft.report_ledger_ecosoft', docargs)
