# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError
import datetime

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

        total= {
            'month': reduce(lambda x, y : x + y , [ c ['month'] for c in lista ]), 
            #'month_sales': 100.0, 
            'acum_month': reduce(lambda x, y : x + y , [ c ['acum_month'] for c in lista ]), 
            #'balance_sales': 100.0, 
            'average': reduce(lambda x, y : x + y , [ c ['average'] for c in lista ]), 
            'acum': reduce(lambda x, y : x + y , [ c ['acum'] for c in lista ]) 
        }
        total['month_sales'] = 100.0 if total['month']!=0 else 0.0
        total['balance_sales'] = 100.0 if total['acum_month']!=0 else 0.0

        return total
    
    def calc_data(self, lista, context, choose_period, period_data):        
        resultados=[]
        print period_data;
        if choose_period:
            month=int (period_data[1].split("/")[0])
            print month
            for a in lista:
                result={}
                print (str (a.with_context(context).argil_initial_balance)  + "---" + str (a.with_context(context).argil_balance_all) 
                    + "---" +  str  (a.with_context(context).debit) + "---" +  str( a.with_context(context).credit) )
                result['name'] = a.name
                result['acum_month'] = a.with_context(context).argil_balance_all 
                result['month'] =  a.with_context(context).debit - a.with_context(context).credit
                result['month_sales'] = 0.0
                result['balance_sales'] = 0.0
                result['average'] = a.with_context(context).argil_balance_all/month
                result['acum'] = a.with_context(context).balance
                resultados.append(result)
        else:
            month= datetime.date.today().month
            print month
            for a in lista:
                result={}
                print ( str (a.argil_initial_balance) + "---" +  str (a.argil_balance_all) 
                    + "---" +  str  (a.debit) + "---" +  str(a.credit))
                result['name'] = a.name
                result['acum_month'] =a.argil_balance_all 
                result['month'] =  a.debit - a.credit
                result['month_sales'] = 0.0
                result['balance_sales'] = 0.0
                result['average'] = a.argil_balance_all/month
                result['acum'] = a.balance
                resultados.append(result)

        totales = self.calc_total(resultados)
        for a in resultados:
            if totales['month'] != 0:
                a['month_sales']=round (a['month']/(totales['month']/100), 2)
            else: 
                a['month_sales']=0.0    
            if totales['acum_month'] !=0: 
                a['balance_sales']= round(a['acum_month']/(totales['acum_month']/100), 2)
            else:
                a['balance_sales']=0.0

        out={
            'resultados':resultados,
            'totales':totales
        }

        return out


    

    @api.model
    def render_html(self, wizard, data=None):

        context = self._context.copy()
        
        period_data = data['form'].get('period_id', False)
        choose_period = data['form'].get('choose_period', False)
        #print str (period_data) + str(choose_period) + str(period_data[0]) + str(len (period_data))
        #with_period = period_data and choose_period
        periodo=""
        if choose_period :
            context.update({'periods': [period_data[0]]})
            periodo=period_data[1]
        else: 
            periodo= datetime.date.today().strftime("%m/%Y")

        ingresos_a = self.env['account.account'].browse(INGRESOS)
        out=self.calc_data(ingresos_a, context, choose_period, period_data)
        ingresos=out['resultados']
        t_ingresos=out['totales']
        
        costos_a = self.env['account.account'].browse(COSTOS)
        out=self.calc_data(costos_a, context, choose_period, period_data)
        costos=out['resultados']
        t_costos=out['totales']
        
        gastos_oper_a = self.env['account.account'].browse(GASTOS_OPER)
        out=self.calc_data(gastos_oper_a, context, choose_period, period_data)
        gastos_oper=out['resultados']
        t_gastos_oper=out['totales']

        gastos_prod_a = self.env['account.account'].browse(GASTOS_PROD)
        out=self.calc_data(gastos_prod_a, context, choose_period,  period_data)
        gastos_prod=out['resultados']
        t_gastos_prod=out['totales']

        gastos_prod_2_a = self.env['account.account'].browse(GASTOS_PROD_2)
        out=self.calc_data(gastos_prod_2_a, context, choose_period, period_data)
        gastos_prod_2=out['resultados']
        t_gastos_prod_2=out['totales']
        
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        

        
        def suma(accumulator, element):
            for key, value in element.items():
                if key == "month_sales" or key == "balance_sales":
                    if value!=0:
                        accumulator[key] = 100.0
                    else:                        
                        accumulator[key] = accumulator.get(key, 0) + value
                else:
                    accumulator[key] = accumulator.get(key, 0) + value
            return accumulator

        def resta(accumulator, element):
            for key, value in element.items():
                if key == "month_sales" or key == "balance_sales":
                    if value!=0:
                        accumulator[key] = 100.0
                    else:                        
                        accumulator[key] = accumulator.get(key, 0) + value                    
                else:
                    accumulator[key] = accumulator.get(key, 0) - value
            return accumulator


        utilidad_bruta = reduce(suma, [t_ingresos, t_costos], {})

        
        #print str (t_ingresos)  + " - " + str(utilidad_bruta) + " - " + str (t_costos)
        utilidad_oper = reduce(resta, [utilidad_bruta, t_costos], {}) #dict (Counter( utilidad_bruta) - Counter(t_gastos_oper))
        total_util_oper = reduce(resta, [utilidad_bruta, t_costos], {}) #dict (Counter( utilidad_bruta) - Counter(t_gastos_oper))
        gtos_prod_fin = reduce(resta, [utilidad_bruta, t_costos], {})
        utilidad_perd = reduce(suma, [total_util_oper, t_gastos_prod_2], {}) #dict (Counter( total_util_oper) + Counter(t_gastos_prod_2))
        total_isr_ptu = reduce(suma, [total_util_oper, t_gastos_prod_2], {})
        util_neta = reduce(suma, [total_util_oper, t_gastos_prod_2], {})
        print util_neta

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'periodo':periodo,
            'ingresos': ingresos,
            'costos': costos,
            'gastos_oper': gastos_oper,
            'gastos_prod': gastos_prod,
            'gastos_prod_2': gastos_prod_2, 
            't_ingresos':t_ingresos,
            't_costos':t_costos,
            't_gastos_oper': t_gastos_oper, 
            't_gastos_prod': t_gastos_prod,
            't_gastos_prod_2': t_gastos_prod_2,
            'utilidad_bruta': utilidad_bruta,
            'utilidad_oper': utilidad_oper,
            'total_util_oper': total_util_oper,
            'gtos_prod_fin': gtos_prod_fin,
            'utilidad_perd': utilidad_perd, 
            'total_isr_ptu': total_isr_ptu, 
            'util_neta': util_neta 
        }
        return self.env['report'].render('account_reports_ecosoft.report_results_ecosoft', docargs)
