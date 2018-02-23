# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError
import datetime
import calendar
from datetime import datetime as dt


class ReportDailyEcosoft(models.AbstractModel):
    _name = 'report.account.report_daily_ecosoft'

  
    def get_lines(self, lista, choose_period,  context, only_balance):
        results=[]        
        for l in lista:            
            l_map={
                'code': l.account_id.code, #account.code,
                'depto': l.ref,
                'desc': l.account_id.name, #account.name, 
                'concept': l.name                
            }
            if choose_period:                
                l_map['credit']=l.with_context(context).credit
                l_map['debit']=l.with_context(context).debit

            else:                
                l_map['credit']=l.credit
                l_map['debit']=l.debit

            results.append(l_map)
        if only_balance: 
            results =filter ( lambda x : ( x['credit'] != 0 or x['debit'] != 0 )  , results)
        return results



    def calc_data (self, lista, choose_period, context, only_balance):
        results=[]
        
        for a in lista:
            result={
                'type' : a.state,
                'num' : a.id,
                'date' : dt.strptime(a.date,'%Y-%m-%d').strftime('%d/%m/%Y'), #a.date, #a.with_context(context).period_id.name,
                'concept' : a.name,
                'moves': self.get_lines(a.line_ids, choose_period,  context, only_balance)                
            }
           
            result['total_credit'] = reduce(lambda x, y : x + y , [ c ['credit'] for c in result['moves'] ])
            result['total_debit'] = reduce(lambda x, y : x + y , [ c ['debit'] for c in result['moves'] ])
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
        if choose_period :
            context.update({'periods': [period_data[0]]})
            #print type (period_data[1])
            fecha = period_data[1].split('/')
            days = calendar.monthrange(int (fecha[1]), int (fecha[0]))
            last_day = days[1]  
            periodo="01/" + period_data[1] + " - "+ str(last_day) + "/" +  period_data[1]
        else: 
            periodo = "01/" + datetime.date.today().strftime("%m/%Y") + " - "+ datetime.date.today().strftime("%d/%m/%Y")
        
        
        moves = self.env['account.move'].search([], order="id asc")
        if len(moves) != 1 and False:
            raise UserError(_("No hay una moves ."))
        
        account_res = self.calc_data(moves , choose_period, context,  only_balance)

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
        return self.env['report'].render('account_reports_ecosoft.report_daily_ecosoft', docargs)
