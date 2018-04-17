# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import serialize_exception,content_disposition
import ast

class CsvController(http.Controller):
    
    @http.route('/csv/trial/<string:data>', auth='user')
    def csv_trial_balance(self, data, **kw):                
        data = str (data).replace('---', '/')
        form=dict()
        form['form'] = ast.literal_eval(data)        
        if data:            
            csv = http.request.env['report.account.report_trialbalance_ecosoft']._get_csv(form)                    
        filename = 'Balanza Comprobación Ecosoft.csv'        
        return request.make_response(csv,
                                        [('Content-Type', 'application/octet-stream'),
                                         ('Content-Disposition', 'attachment; filename="%s"'%(filename))])

  

    @http.route('/csv/general/<string:data>', auth='user')
    def csv_general_balance(self, data, **kw):                
        data = str (data).replace('---', '/')
        form=dict()
        form['form'] = ast.literal_eval(data)        
        if data:            
            csv = http.request.env['report.account.report_generalbalance_ecosoft']._get_csv(form)                    
        filename = 'Balance General Ecosoft.csv'        
        return request.make_response(csv,
                                        [('Content-Type', 'application/octet-stream'),
                                         ('Content-Disposition', 'attachment; filename="%s"'%(filename))])    

    @http.route('/csv/results/<string:data>', auth='user')
    def csv_report_results(self, data, **kw):                
        data = str (data).replace('---', '/')
        form=dict()
        form['form'] = ast.literal_eval(data)        
        if data:            
            csv = http.request.env['report.account.report_results_ecosoft']._get_csv(form)                    
        filename = 'Reporte Resultados Ecosoft.csv'
        print csv
        return request.make_response(csv,
                                        [('Content-Type', 'application/octet-stream'),
                                         ('Content-Disposition', 'attachment; filename="%s"'%(filename))])    

    @http.route('/csv/ledger/<string:data>', auth='user')
    def csv_ledger_book(self, data, **kw):                
        data = str (data).replace('---', '/')
        form=dict()
        form['form'] = ast.literal_eval(data)        
        if data:            
            csv = http.request.env['report.account.report_ledger_ecosoft']._get_csv(form)                    
        filename = 'Libro Mayor Ecosoft.csv'        
        return request.make_response(csv,
                                        [('Content-Type', 'application/octet-stream'),
                                         ('Content-Disposition', 'attachment; filename="%s"'%(filename))])    


    @http.route('/csv/daily/<string:data>', auth='user')
    def csv_daily_book(self, data, **kw):                
        data = str (data).replace('---', '/')
        form=dict()
        form['form'] = ast.literal_eval(data)        
        if data:            
            csv = http.request.env['report.account.report_daily_ecosoft']._get_csv(form)                    
        filename = 'Libro Diario Ecosoft.csv'        
        return request.make_response(csv,
                                        [('Content-Type', 'application/octet-stream'),
                                         ('Content-Disposition', 'attachment; filename="%s"'%(filename))])    