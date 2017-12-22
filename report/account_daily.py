# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError
import datetime


class ReportDailyEcosoft(models.AbstractModel):
    _name = 'report.account.report_daily_ecosoft'

  
    def get_lines(self, lista, choose_period, periodo, context):
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
        return results



    def calc_data (self, lista, choose_period, context, periodo):
        results=[]
        
        for a in lista:
            result={
                'type' : a.state,
                'num' : a.id,
                'date' : periodo, #a.with_context(context).period_id.name,
                'concept' : a.name,
                'moves': self.get_lines(a.line_ids, choose_period, periodo, context)                
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
        
        periodo=""
        if choose_period :
            context.update({'periods': [period_data[0]]})
            periodo=period_data[1]
        else: 
            periodo= datetime.date.today().strftime("%m/%Y")
        
        moves = self.env['account.move'].search([])
        if len(moves) != 1 and False:
            raise UserError(_("No hay una moves ."))
        
        account_res = self.calc_data(moves , choose_period, context, periodo)
        
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
