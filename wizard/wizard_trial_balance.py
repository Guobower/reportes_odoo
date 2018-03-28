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
    period_id = fields.Many2one('account.period', 'Periodo', required=False)
    level = fields.Selection([(1, '1.-Mayor'),(2, '2.- Cuenta'),(3, '3.- Sub-cta'),(4, '4.- Sub-cta-2'),(5, '5.- Auxiliar')], string='Nivel',
      required=True, copy=False, default=1,)
    display_account = fields.Selection([('all','All'), ('movement','With movements'), 
                                        ('not_zero','With balance is not equal to 0'),], 
                                        string='Display Accounts', required=True, default='movement')
    target_move = fields.Selection([('posted', 'All Posted Entries'),
                                    ('all', 'All Entries'),
                                    ], string='Target Moves', required=True, default='all')
    only_balance = fields.Boolean('Con saldos')
    
    
   
    @api.multi
    def print_csv(self):
        data = self.read(['choose_period','period_id','level','display_account','target_move', 'only_balance'])[0]
        print type (data)
        print data 
        data = str (data).replace('/', '---')
        print data

        return {
            'type' : 'ir.actions.act_url',
            'url': '/csv/trial/%s/'%(data),            
            'target': 'self',
        }

    
    def print_xls(self, data):        
        data.setdefault('form',{})
        data['form'].update(self.read(['choose_period','period_id','level','display_account','target_move', 'only_balance'])[0])
        return {'type': 'ir.actions.report.xml',
                'report_name': 'account.report_trialbalance_ecosoft.xlsx',
                'datas': data
                }        

    def print_report(self, data):
        data.setdefault('form',{})
        data['form'].update(self.read(['choose_period','period_id','level','display_account','target_move', 'only_balance'])[0])
        return self.env['report'].get_action(False, 'account.report_trialbalance_ecosoft', data=data)
