# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError

"""
GASTOS_OPER

select id, name from account_account where name in  ('CORTESÍAS A CLIENTES', 'SUELDOS PERSONAL OPER. TEC. ', 
'COMISIONES PERSONAL OPER. TEC. ', 'SUELDOS PERSONAL DE OFICINA ', 'COMISIONES PERSONAL DE OFICINA ', 
'COMBUSTIBLES ', 'OTRAS PRESTACIONES AL PERSONAL ', 'IMPUESTOS SOBRE REMUNERACIONES ', 'ARRENDAMIENTO DE OTROS EQUIPOS ', 
'AMORTIZACIONES DE GASTOS DIFERIDOS ', 'MANTTO. EDIFICIOS Y PROPIEDAD', 'CONSULTORÍA ', 'GASTOS DE OPERACIÓN:', 
'DEPRECIACION DE EQUIPO', 'PAPELERIA Y ARTICULOS DE OFICINA', 'ENTRENAMIENTO Y MATERIAL TECNICO', 
'MANTTO. DE EQUIPO DE TRANSPORTE', 'ELECTRICIDAD GAS Y AGUA', 'PRIMAS DE ANTIGUEDAD ', 'CUOTAS AL SEGURO SOCIAL ', 
'IMPUESTOS Y DERECHOS VARIOS', 'PRIMAS DE SEGUROS Y FIANZAS ', 'SERVICIO DE VIGILANCIA ', 'DIVERSOS GASTOS SEMIFIJOS ', 
'TELEFONOS Y TELECOMUNICACIONES ', 'HERRAMIENTAS Y MAT. DE CONSUMO ', 'SAR ', 'APORTACIONES AL INFONAVIT ', 'HONORARIOS',
 'RENTA DE INMUEBLES', 'CUOTAS Y SUSCRIPCIONES', 'MANTENIMIENTO DE EQUIPO', 'UNIFORMES', 'GASTOS DE VIAJE Y PRESENTACION');
 id  |               name               
-----+----------------------------------
 607 | PAPELERIA Y ARTICULOS DE OFICINA
 172 | UNIFORMES
 173 | UNIFORMES
  68 | ENTRENAMIENTO Y MATERIAL TECNICO
  71 | PAPELERIA Y ARTICULOS DE OFICINA
  82 | RENTA DE INMUEBLES
  85 | HONORARIOS
  69 | GASTOS DE VIAJE Y PRESENTACION
  72 | UNIFORMES
  75 | MANTENIMIENTO DE EQUIPO
  64 | MANTTO. DE EQUIPO DE TRANSPORTE
  74 | DEPRECIACION DE EQUIPO
  78 | CUOTAS Y SUSCRIPCIONES
  83 | ELECTRICIDAD GAS Y AGUA
  86 | IMPUESTOS Y DERECHOS VARIOS
 608 | UNIFORMES
 389 | UNIFORMES
 403 | UNIFORMES
 477 | CUOTAS Y SUSCRIPCIONES
 418 | UNIFORMES
 484 | RENTA DE INMUEBLES
(21 rows)
"""
INGRESOS=[51,52]
COSTOS=[53]
GASTOS_OPER=[68, 71, 82, 85, 69, 72, 75, 64, 74, 78, 83, 86]
GASTOS_PROD=[89, 92]
GASTOS_PROD_2=[87, 90]

class ReportResultsEcosoft(models.AbstractModel):
    _name = 'report.account.report_results_ecosoft'

    def calc_total (self, lista):
        t=0
        for a in lista:
            t= t+a.balance
        return t

    
    def calc_data(self, lista):        
        resultados=[]
        
        for a in lista:
            result={}
            result['name'] = a.name
            result['balance'] = a.balance
            result['month'] = 0.0
            result['month_sales'] = 0.0
            result['balance_sales'] = 0.0
            result['average'] = 0.0
            result['acum'] = result['balance_sales']
            resultados.append(result)
        return resultados

    @api.model
    def render_html(self, wizard, data=None):
        ingresos_a = self.env['account.account'].browse(INGRESOS)
        ingresos=self.calc_data(ingresos_a)
        t_ingresos=self.calc_total(ingresos_a)                
        
        costos_a = self.env['account.account'].browse(COSTOS)
        costos=self.calc_data(costos_a)
        t_costos=self.calc_total(costos_a)
        
        gastos_oper_a = self.env['account.account'].browse(GASTOS_OPER)
        gastos_oper=self.calc_data(gastos_oper_a)
        t_gastos_oper=self.calc_total(gastos_oper_a)

        gastos_prod_a = self.env['account.account'].browse(GASTOS_PROD)
        gastos_prod=self.calc_data(gastos_prod_a)
        t_gastos_prod=self.calc_total(gastos_prod_a)

        gastos_prod_2_a = self.env['account.account'].browse(GASTOS_PROD_2)
        gastos_prod_2=self.calc_data(gastos_prod_2_a)
        t_gastos_prod_2=self.calc_total(gastos_prod_2_a)
        
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        


        totales = {
            
            }
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'ingresos': ingresos,
            'costos': costos,
            'gastos_oper': gastos_oper,
            'gastos_prod': gastos_prod,
            'gastos_prod_2': gastos_prod_2, 
            't_ingresos':{'month': 0.0, 'month_sales':0.0, 'balance':t_ingresos, 'balance_sales':0.0, 'average':0.0, 'acum':0.0 } ,
            't_costos':{'month': 0.0, 'month_sales':0.0, 'balance':t_costos, 'balance_sales':0.0, 'average':0.0, 'acum':0.0 } ,
            't_gastos_oper': {'month': 0.0, 'month_sales':0.0, 'balance':t_gastos_oper, 'balance_sales':0.0, 'average':0.0, 'acum':0.0 },
            't_gastos_prod': {'month': 0.0, 'month_sales':0.0, 'balance':t_gastos_prod, 'balance_sales':0.0, 'average':0.0, 'acum':0.0 },
            't_gastos_prod_2': {'month': 0.0, 'month_sales':0.0, 'balance':t_gastos_prod_2, 'balance_sales':0.0, 'average':0.0, 'acum':0.0 },
            'utilidad_bruta': {'month': 0.0, 'month_sales':0.0, 'balance':t_ingresos - t_costos, 'balance_sales':0.0, 'average':0.0, 'acum':0.0 },
            'utilidad_oper': {'month': 0.0, 'month_sales':0.0, 'balance':(t_ingresos - t_costos) - t_gastos_oper, 'balance_sales':0.0, 'average':0.0, 'acum':0.0 },
            'total_util_oper': {'month': 0.0, 'month_sales':0.0, 'balance':(t_ingresos - t_costos) - t_gastos_oper, 'balance_sales':0.0, 'average':0.0, 'acum':0.0 },
            'gtos_prod_fin':  {'month': 0.0, 'month_sales':0.0, 'balance':0.0, 'balance_sales':0.0, 'average':0.0, 'acum':0.0 }, 
            'utilidad_perd': {'month': 0.0, 'month_sales':0.0, 'balance':(t_ingresos - t_costos) - t_gastos_oper + t_gastos_oper + t_gastos_prod_2, 'balance_sales':0.0, 'average':0.0, 'acum':0.0 },
            'total_isr_ptu': {'month': 0.0, 'month_sales':0.0, 'balance':0.0, 'balance_sales':0.0, 'average':0.0, 'acum':0.0 },
            'util_neta': {'month': 0.0, 'month_sales':0.0, 'balance':(t_ingresos - t_costos) - t_gastos_oper + t_gastos_oper + t_gastos_prod_2, 'balance_sales':0.0, 'average':0.0, 'acum':0.0 },         
        }
        return self.env['report'].render('account_reports_ecosoft.report_results_ecosoft', docargs)
