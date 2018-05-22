# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError
import datetime as dt
from .account_results import * 
import calendar
from datetime import datetime
import locale
from .utils_xlsx import UtilsXlsx
import functools

"""
ACTIVOS_CIRCULANTE_IDS
select id, name from account_account where name in ('BANCOS','FONDO DE CAJA CHICA','CLIENTES','IMPUESTOS ACREDITABLES PAGADOS'
,'IMPUESTOS ACREDITABLES POR','PAGAR','DEUDORES DIVERSOS','INVENTARIOS','IMPUESTOS A FAVOR','PAGOS PROVISIONALES DE ISR');

id  |              name              
-----+--------------------------------
 111 | INVENTARIOS
  33 | BANCOS
   3 | CLIENTES
   9 | IMPUESTOS ACREDITABLES PAGADOS
  10 | DEUDORES DIVERSOS
   6 | FONDO DE CAJA CHICA
  15 | PAGOS PROVISIONALES DE ISR
  12 | INVENTARIOS
  14 | IMPUESTOS A FAVOR

ACTIVOS_NO_CIRCULANTE_IDS
select id, name from account_account where name in ('EQUIPO DE INSTALACION', 'DEPN. ACUM. DE EQUIPO DE INSTALACION'
, 'MOBILIARIO Y EQUIPO DE OFICINA', 'DEPN. ACUM. DE MOB. Y EQUIPO DE OFICINA', 'EQUIPO DE TRANSPORTE', 'DEPN. ACUM. EQUIPO DE TRANSPORTE'
, 'EQUIPO DE COMPUTO', 'DEPN. ACUM. EQUIPO DE COMPUTO', 'GASTOS DE INSTALACION Y ADAPTACION', 'AMORT. DE GTOS. DE INST. Y ADAPTACION');
 id  |                  name                   
-----+-----------------------------------------
 196 | DEPN. ACUM. EQUIPO DE TRANSPORTE
 195 | EQUIPO DE TRANSPORTE
  20 | EQUIPO DE TRANSPORTE
  18 | MOBILIARIO Y EQUIPO DE OFICINA
 192 | DEPN. ACUM. DE EQUIPO DE INSTALACION
  22 | EQUIPO DE COMPUTO
  23 | DEPN. ACUM. EQUIPO DE COMPUTO
  19 | DEPN. ACUM. DE MOB. Y EQUIPO DE OFICINA
  21 | DEPN. ACUM. EQUIPO DE TRANSPORTE
 200 | GASTOS DE INSTALACION Y ADAPTACION
 194 | DEPN. ACUM. DE MOB. Y EQUIPO DE OFICINA
 193 | MOBILIARIO Y EQUIPO DE OFICINA
 191 | EQUIPO DE INSTALACION
 197 | EQUIPO DE COMPUTO
  26 | AMORT. DE GTOS. DE INST. Y ADAPTACION
  25 | GASTOS DE INSTALACION Y ADAPTACION
  16 | EQUIPO DE INSTALACION
  17 | DEPN. ACUM. DE EQUIPO DE INSTALACION
 467 | EQUIPO DE TRANSPORTE
 469 | EQUIPO DE COMPUTO
 470 | EQUIPO DE INSTALACION
 468 | EQUIPO DE COMPUTO

ACTIVOS_DIFERIDO
select id, name from account_account where name in ('DEPOSITOS EN GARANTIA', 'PAGOS ANTICIPADOS', 'ANTICIPO A PROVEEDORES');
 id  |          name          
-----+------------------------
 199 | DEPOSITOS EN GARANTIA
  24 | DEPOSITOS EN GARANTIA
  13 | PAGOS ANTICIPADOS
   7 | ANTICIPO A PROVEEDORES

PASIVO_CORTO_PLAZO
 select id, name from account_account where name in ('OTRAS CUENTAS POR PAGAR', 'ACREEDORES DIVERSOS', 'SUELDOS Y COMISIONES POR PAGAR', 
 'IMPUESTOS Y DERECHOS POR PAGAR', 'IVA POR PAGAR', 'IVA POR PAGAR DIFERIDO', 'OTROS PASIVOS POR PAGAR', 'IMPUESTO SOBRE LA RENTA', 
 'DOCUMENTOS POR PAGAR', 'PROVEEDORES', 'IMPUESTOS RETENIDOS', 'PROVISION CONTRIB DE S SOCIAL X PAGAR', 'PTU');
 id  |                 name                  
-----+---------------------------------------
 236 | OTRAS CUENTAS POR PAGAR
  31 | SUELDOS Y COMISIONES POR PAGAR
  35 | IVA POR PAGAR
  27 | PROVEEDORES
  28 | OTRAS CUENTAS POR PAGAR
  29 | ACREEDORES DIVERSOS
  39 | PROVISION CONTRIB DE S SOCIAL X PAGAR
  42 | IMPUESTO SOBRE LA RENTA
 123 | IVA POR PAGAR
  38 | IMPUESTOS RETENIDOS
  40 | OTROS PASIVOS POR PAGAR
  43 | DOCUMENTOS POR PAGAR
  41 | PTU
 307 | SUELDOS Y COMISIONES POR PAGAR
 309 | IVA POR PAGAR
 122 | IVA POR PAGAR

CAPITAL
select id, name from account_account where name in ('CAPITAL SUSCRITO', 'RESERVA LEGAL', 'RESULTADO DE EJERCICIOS ANTERIORES', 'RESULTADO DEL EJERCICIO');
id  |                name                
-----+------------------------------------
  45 | CAPITAL SUSCRITO
  46 | RESERVA LEGAL
  48 | RESULTADO DE EJERCICIOS ANTERIORES
 333 | RESERVA LEGAL

"""

"""
ACTIVOS_CIRCULANTE_IDS=[33, 3, 9, 8, 10, 6, 15, 12, 14]
ACTIVOS_NO_CIRCULANTE_IDS=[20, 18, 19, 22, 23, 21,26, 25, 16, 17]
ACTIVOS_DIFERIDO=[24, 13, 7]
PASIVO_CORTO_PLAZO=[31, 32, 35, 27, 37, 28, 29, 39, 42, 38, 40, 43, 41]
CAPITAL=[45, 46, 48, 49]
"""

class ReportGeneralBalanceEcosoft(ReportResultsEcosoft):
    _name = 'report.account_reports_ecosoft.report_generalbalance_ecosoft'

    def calc_total_balance (self, lista):
        t=0
        for a in lista:
            t= t+a['balance']
        return round (t,2)

    def calc_data_balance (self, lista, choose_period, context):
        results=[]
        if choose_period:
            for a in lista:
                #print a.with_context(context).balance
                result={
                    'balance' : a.with_context(context).balance,
                    'name' : a.with_context(context).name
                }
                results.append(result)
        else:
            for a in lista:
                result={
                    'balance' : a.balance,
                    'name' : a.name                
                }
                results.append(result)
        return results

    def negative (self, result, name):
        #print 'in negative'
        for reg in result:
            #print  name + '---' +reg['name']
            if name in reg['name']:
                reg['balance'] = -(abs (reg['balance']))
        #str (m)    
        
    def get_data(self, data):
        context = self._context.copy()
        period_data = data['form'].get('period_id', False)
        only_balance = data['form'].get('only_balance')
        choose_period = data['form'].get('choose_period', False)
        with_period = period_data and choose_period
        locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')
        
        periodo=''
        periodo_title=''
        if choose_period :
            context.update({'periods': [period_data[0]]})
            #print type (period_data[1])
            fecha = period_data[1].split('/')
            days = calendar.monthrange(int (fecha[1]), int (fecha[0]))
            last_day = days[1]  
            periodo="01/" + period_data[1] + " - "+ str(last_day) + "/" +  period_data[1]
            periodo_title = datetime.strptime(str(last_day) + "/" +  period_data[1],'%d/%m/%Y').strftime('%d de %B del %Y')

            #str (last_day) + ' de '+ calendar.month_name[int (period_data[0])].title() + 'del '+ calendar.year []
        else:
            periodo = "01/" + dt.date.today().strftime("%m/%Y") + " - "+ dt.date.today().strftime("%d/%m/%Y")
            periodo_title = datetime.strptime(dt.date.today().strftime("%d/%m/%Y"),'%d/%m/%Y').strftime('%d de %B del %Y')
        

        #activo_circulante = self.env['account.account'].browse(ACTIVOS_CIRCULANTE_IDS)
        activo_circulante = self.env['account.financial.report'].search([('name','=','ACTIVO CIRCULANTE')]).account_ids        
        activo_circulante=self.calc_data_balance(activo_circulante, choose_period, context)

        t_activo_circulante=self.calc_total_balance(activo_circulante) 
                               
        #activo_no_circulante = self.env['account.account'].browse(ACTIVOS_NO_CIRCULANTE_IDS)
        activo_no_circulante = self.env['account.financial.report'].search([('name','=','ACTIVO NO CIRCULANTE')]).account_ids
        activo_no_circulante=self.calc_data_balance(activo_no_circulante, choose_period, context)
        self.negative(activo_no_circulante, 'DEPN.')
        t_activo_no_circulante=self.calc_total_balance(activo_no_circulante)
        
        #activo_diferido = self.env['account.account'].browse(ACTIVOS_DIFERIDO)
        activo_diferido = self.env['account.financial.report'].search([('name','=','ACTIVO DIFERIDO')]).account_ids
        activo_diferido=self.calc_data_balance(activo_diferido, choose_period, context)
        t_activo_diferido=self.calc_total_balance(activo_diferido)

        #pasivo_corto_plazo = self.env['account.account'].browse(PASIVO_CORTO_PLAZO)
        pasivo_corto_plazo = self.env['account.financial.report'].search([('name','=','PASIVO CORTO PLAZO')]).account_ids
        pasivo_corto_plazo=self.calc_data_balance(pasivo_corto_plazo, choose_period, context)
        t_pasivo_corto_plazo=self.calc_total_balance(pasivo_corto_plazo)

        #capital = self.env['account.account'].browse(CAPITAL)
        capital = self.env['account.financial.report'].search([('name','=','CAPITAL')]).account_ids
        capital=self.calc_data_balance(capital, period_data, context)
        r = self.get_data_report(context, period_data, choose_period, data,periodo) 
        result_ejer={
                  'balance' : -(abs (r['util_neta']['month'])),
                  'name' : 'RESULTADO DEL EJERCICIO'
              }
        capital.append(result_ejer)               
        t_capital=self.calc_total_balance(capital)
       
        if only_balance: 
            activo_circulante =filter ( lambda x : ( x['balance'] != 0 )  , activo_circulante)
            activo_no_circulante =filter ( lambda x : ( x['balance'] != 0 )  , activo_no_circulante)
            activo_diferido =filter ( lambda x : ( x['balance'] != 0 )  , activo_diferido)
            pasivo_corto_plazo =filter ( lambda x : ( x['balance'] != 0 )  , pasivo_corto_plazo)
            capital =filter ( lambda x : ( x['balance'] != 0 )  , capital)   
               
        totales = {
            't_activo_circulante':t_activo_circulante, 
            't_activo_no_circulante':t_activo_no_circulante,
            't_activo_diferido': t_activo_diferido,
            't_pasivo_corto_plazo': t_pasivo_corto_plazo,
            't_capital': t_capital,
            't_activo': t_activo_circulante + t_activo_no_circulante + t_activo_diferido,
            't_pasivo_capital': t_pasivo_corto_plazo + t_capital
            }
        docargs = {
           
            'time': time,
            'activo_circulante': activo_circulante,
            'activo_no_circulante': activo_no_circulante,
            'activo_diferido': activo_diferido,
            'pasivo_corto_plazo': pasivo_corto_plazo,
            'capital': capital, 
            'totales': totales,
            'periodo': periodo,
            'periodo_title': periodo_title           
        }

        return docargs


    @api.model
    def render_html(self, wizard, data=None):
        docargs = self.get_data (data)
        return self.env['report'].render('account_reports_ecosoft.report_generalbalance_ecosoft', docargs)

    @api.model
    def get_report_values (self, docids, data): 
        print ('get values')       
        docargs =  self.get_data (data)        
        return docargs

    def get_map_account(self,docargs, name):
        accounts = docargs[name]
        csv = ''
        if len(accounts) > 0:
            for account in accounts:                        
                csv_row =  '|' + account['name'] + '|'+ str (account['balance']) 
                #print csv_row
                csv += csv_row  + "\n" 
        return csv               

       
    @api.model
    def _get_csv(self, data=None):
        #print 'en general balance'
        docargs =  self.get_data (data)
        headers = ['', 'Nombre', 'Saldo']
        csv = '|'.join(headers)
        csv += "\n"
        csv +='ACTIVO CIRCULANTE' + '|'  +  '|' + "\n" 
        csv += self.get_map_account(docargs, 'activo_circulante')
        csv += '|' + 'TOTAL DE ACTIVO CIRCULANTE' + '|'+ str (docargs['totales']['t_activo_circulante']) + "\n" 
        csv +='ACTIVO NO CIRCULANTE' + '|'  +  '|' + "\n" 
        csv += self.get_map_account(docargs, 'activo_no_circulante')
        csv += '|' + 'TOTAL DE ACTIVO NO CIRCULANTE' + '|'+ str (docargs['totales']['t_activo_no_circulante']) + "\n" 
        csv +='ACTIVO DIFERIDO' + '|'  +  '|' + "\n" 
        csv += self.get_map_account(docargs, 'activo_diferido')
        csv += '|' + 'TOTAL ACTIVO DIFERIDO' + '|'+ str (docargs['totales']['t_activo_diferido']) + "\n" 
        csv += 'TOTAL DE ACTIVO' + '|' + '|'+ str (docargs['totales']['t_activo']) + "\n" 
        csv +='PASIVO CORTO PLAZO' + '|'  +  '|' + "\n" 
        csv += self.get_map_account(docargs, 'pasivo_corto_plazo')
        csv += '|' + 'TOTAL DE PASIVO CORTO PLAZO' + '|'+ str (docargs['totales']['t_pasivo_corto_plazo']) + "\n" 
        csv +='CAPITAL' + '|'  +  '|' + "\n" 
        csv += self.get_map_account(docargs, 'capital')
        csv += '|' + 'TOTAL DE CAPITAL' + '|'+ str (docargs['totales']['t_capital']) + "\n" 
        csv += 'TOTALDE PASIVO Y CAPITAL' + '|' + '|'+ str (docargs['totales']['t_pasivo_capital']) + "\n"         
        return csv

                
    @api.model
    def _get_xls(self, data=None, workbook=None):
             
        docargs =  self.get_data (data)
        worksheet = workbook.add_worksheet('Balance')
        
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 35)
        worksheet.set_column('C:C', 15)
        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': 1, })
        matrix =map(lambda x: x.split('|'), self._get_csv(data).split('\n'))
        headers=[0,]
        i=0
        for r in matrix:
            if r[0]!='':
                headers.append(i)
            i+=1   
        UtilsXlsx.add_matrix(matrix, worksheet, headers, bold)  

        
