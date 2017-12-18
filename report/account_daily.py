# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError


class ReportDailyEcosoft(models.AbstractModel):
    _name = 'report.account.report_daily_ecosoft'

  
    def get_lines(self, lista):
        results=[]
        #print 'lines ' + str(lista)
        for l in lista:
            #account = self.env['account.account'].browse([l.account_id])
            l_map={
                'code': l.account_id.code, #account.code,
                'depto': l.ref,
                'desc': l.account_id.name, #account.name, 
                'concept': l.name,  
                'credit': l.credit,
                'debit': l.debit
            }
            results.append(l_map)
        return results



    def calc_data (self, lista, period_data, context):
        results=[]
        if period_data:
            for a in lista:
                result={
                    'type' : a.state,
                    'num' : a.id,
                    'date' : a.with_context(context).period_id,
                    'concept' : a.name,
                    'moves': self.get_lines(line_ids)                
                }
                #s = reduce(lambda

                result['total_credit'] = reduce(lambda x, y : x + y , [ c ['credit'] for c in result['moves'] ])
                result['total_debit'] = reduce(lambda x, y : x + y , [ c ['debit'] for c in result['moves'] ])
                results.append(result)
        else:
            for a in lista:
                result={
                    'type' : a.ref,
                    'num' : a.id,
                    'date' : a.period_id.name,
                    'concept' : a.name,
                    'moves': self.get_lines(a.line_ids)                
                }
                
                result['total_credit']=reduce(lambda x, y : x + y , [ c ['credit'] for c in result['moves'] ])
                result['total_debit']=reduce(lambda x, y : x + y , [ c ['debit'] for c in result['moves'] ])
                results.append(result)
        return results 


    @api.model
    def render_html(self, wizard, data=None):
        context = self._context.copy()
        
        period_data = data['form'].get('period_id', False)
        choose_period = data['form'].get('choose_period', False)
        with_period = period_data and choose_period
        
        if with_period :
            context.update({'periods': [period_data[0]]})
        
        moves = self.env['account.move'].search([])
        if len(moves) != 1 and False:
            raise UserError(_("No hay una moves ."))
        
        account_res = self.calc_data(moves , period_data, context)
        
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': account_res,            
            'periodo': with_period and period_data[1]
        }
        return self.env['report'].render('account_reports_ecosoft.report_daily_ecosoft', docargs)
