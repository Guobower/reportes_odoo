# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _
from odoo import http
from odoo.http import request as req
import csv
import urllib


class WizardTrialBalance(models.TransientModel):
    _name = 'wizard.trial.balance.ecosoft'

    choose_period = fields.Boolean('A un Periodo')
    date_from = fields.Datetime('Desde')
    date_to = fields.Datetime('Hasta')    
    level = fields.Selection([(1, '1.-Mayor'),(2, '2.- Cuenta'),(3, '3.- Sub-cta'),(4, '4.- Sub-cta-2'),(5, '5.- Auxiliar')], string='Nivel',
      required=True, copy=False, default=1,)    
    only_balance = fields.Boolean('Con saldos')

    
    
   
    @api.multi
    def print_csv(self):
        data.setdefault('form',{})
        data['form'].update(self.read(['choose_period','date_from','date_to', 'level', 'only_balance'])[0])        
        data = str (data).replace('/', '---')        
        return {
            'type' : 'ir.actions.act_url',
            'url': '/csv/trial/%s/'%(data),            
            'target': 'self',
        }

    
    def print_xls(self, data):        
        data.setdefault('form',{})
        data['form'].update(self.read(['choose_period','date_from','date_to', 'level', 'only_balance'])[0])
        return {'type': 'ir.actions.report.xml',
                'report_name': 'account.report_trialbalance_ecosoft.xlsx',
                'datas': data
                }        

    def print_report(self, data):
        data.setdefault('form',{})
        data['form'].update(self.read(['choose_period','date_from','date_to', 'level', 'only_balance'])[0])
        print (data['form'])
        return self.env.ref('account_reports_ecosoft.action_report_trial_balance_ecosoft').report_action(self, data=data)
        #return self.env['report'].get_action(False, 'account.report_trialbalance_ecosoft', data=data)
