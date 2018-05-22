# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _


class WizardResultsBalance(models.TransientModel):
    _name = 'wizard.results.ecosoft'

    choose_period = fields.Boolean('A un Periodo')
    date_from = fields.Datetime('Desde')
    date_to = fields.Datetime('Hasta')      
    only_balance = fields.Boolean('Con saldos')

    @api.multi
    def print_csv(self):
        data.setdefault('form',{})
        data['form'].update(self.read(['choose_period','date_from','date_to', 'only_balance'])[0])
        data = str (data).replace('/', '---')                

        return {
            'type' : 'ir.actions.act_url',
            'url': '/csv/results/%s/'%(data),            
            'target': 'blank',
        }

    def print_xls(self, data):        
        data.setdefault('form',{})
        data['form'].update(self.read(['choose_period','date_from','date_to', 'only_balance'])[0])
        return {'type': 'ir.actions.report.xml',
                'report_name': 'account.report_results_ecosoft.xlsx',
                'datas': data
                }

    def print_report(self, data):
        data.setdefault('form',{})
        data['form'].update(self.read(['choose_period','date_from','date_to', 'only_balance'])[0])
        return self.env.ref('account_reports_ecosoft.action_report_results_ecosoft').report_action(self, data=data)
        #return self.env['report'].get_action(False, 'account.report_results_ecosoft', data=data)
