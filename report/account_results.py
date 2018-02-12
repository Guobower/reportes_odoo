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
"""
INGRESOS= [50,52]
COSTOS=[53]
GASTOS_OPER=[57, 56, 68, 71, 70, 73, 80, 82, 85, 69, 72, 75, 64, 74, 78, 83, 86, 420]
GASTOS_PROD=[89, 92]
GASTOS_PROD_2=[87, 90]
"""


class ReportResultsEcosoft(models.AbstractModel):
    _name = 'report.account.report_results_ecosoft'

    def calc_total (self, lista):
        t=0
        if lista:
            total= {
                'month': reduce(lambda x, y : x + y , [ c ['month'] for c in lista ]), 
                'month_sales': reduce(lambda x, y : x + y , [ c ['month_sales'] for c in lista ]),  
                'acum_month': reduce(lambda x, y : x + y , [ c ['acum_month'] for c in lista ]), 
                'balance_sales': reduce(lambda x, y : x + y , [ c ['balance_sales'] for c in lista ]), 
                'average': reduce(lambda x, y : x + y , [ c ['average'] for c in lista ]), 
                #'acum': reduce(lambda x, y : x + y , [ c ['acum'] for c in lista ]) 
            }
            total['acum'] = total['balance_sales']
        else:
            total= {
                'month': 0.0, 
                'month_sales': 0.0,  
                'acum_month': 0.0, 
                'balance_sales': 0.0, 
                'average': 0.0, 
                'acum': 0.0 
            }
        return total
    
    def calc_porcent_base(self, resultados, totales):    
        for a in resultados:
            if totales['month'] != 0:
                a['month_sales']=round (a['month']/(totales['month']/100), 2)
            else: 
                a['month_sales']=0.0    
            if totales['acum_month'] !=0: 
                a['balance_sales']= round(a['acum_month']/(totales['acum_month']/100), 2)
            else:
                a['balance_sales']=0.0
            a['acum'] = a['balance_sales']


    def calc_porcent(self, resultados, base):    
        for a in resultados:
            if a['month'] != 0:
                a['month_sales']=round (a['month'] * base['month_sales'] /base['month'], 2)
            else: 
                a['month_sales']=0.0    
            if a['acum_month'] !=0: 
                a['balance_sales']= round(a['acum_month']*base['balance_sales']/base['acum_month'], 2)                
            else:
                a['balance_sales']=0.0
            a['acum'] = a['balance_sales']

    def calc_data(self, lista, context, choose_period, period_data):        
        resultados=[]
        #print period_data;
        if choose_period:
            month=int (period_data[1].split("/")[0])
            #print month
            for a in lista:
                result={}
                print ( "Con periodo" +  str (a.with_context(context).balance) + " ---" + str (a.with_context(context).argil_initial_balance)  + "---" + str (a.with_context(context).argil_balance_all) 
                    + "---" +  str  (a.with_context(context).debit) + "---" +  str( a.with_context(context).credit) )
                result['name'] = a.name
                result['acum_month'] = abs (a.with_context(context).argil_balance_all )
                result['month'] = abs(a.with_context(context).balance) #a.with_context(context).credit - a.with_context(context).debit
                result['month_sales'] = 0.0
                result['balance_sales'] = 0.0
                result['average'] = abs(a.with_context(context).argil_balance_all/month)
                #result['acum'] = a.with_context(context).balance
                resultados.append(result)
        else:
            month= datetime.date.today().month
            #print month
            for a in lista:
                result={}
                print ("Sin periodo" + str (a.balance) + "-------" +  str (a.argil_initial_balance) + "---" +  str (a.argil_balance_all) 
                    + "---" +  str  (a.debit) + "---" +  str(a.credit))
                result['name'] = a.name
                result['acum_month'] =abs (a.argil_balance_all) 
                result['month'] =  abs(a.balance) #a.credit - a.debit
                result['month_sales'] = 0.0
                result['balance_sales'] = 0.0
                result['average'] = abs(a.argil_balance_all/month)
                #result['acum'] = a.balance
                resultados.append(result)
        return resultados

    def total (self,resultados, base):
        if base=={}:            
            totales = self.calc_total(resultados)
            totales['month_sales'] = 100.0 if totales['month']!=0 else 0.0
            totales['balance_sales'] = 100.0 if totales['acum_month']!=0 else 0.0
            totales['acum'] = totales['balance_sales']
            self.calc_porcent_base(resultados, totales)
        else:            
            self.calc_porcent(resultados, base)        
            totales = self.calc_total(resultados)
        return totales    

    def negative (self, m):
        for key in m:
            if key != 'name':
                m[key] = -(m[key])
        str (m)    

    @api.model
    def render_html(self, wizard, data=None):

        context = self._context.copy()
        
        period_data = data['form'].get('period_id', False)
        choose_period = data['form'].get('choose_period', False)
       
        periodo=""
        if choose_period :
            context.update({'periods': [period_data[0]]})
            periodo=period_data[1]
        else: 
            periodo= datetime.date.today().strftime("%m/%Y")

        #ingresos_a = self.env['account.account'].browse(INGRESOS)
        ingresos_a = self.env['account.financial.report'].search([('name','=','INGRESOS')]).account_ids
        ingresos=self.calc_data(ingresos_a, context, choose_period, period_data)
        if len (ingresos) > 1:
            self.negative(ingresos[1])
        t_ingresos= self.total (ingresos, {}) # out['totales']
        base = {}
        if ingresos:
            base = ingresos [0]
        
        
        #costos_a = self.env['account.account'].browse(COSTOS)
        costos_a = self.env['account.financial.report'].search([('name','=','COSTOS')]).account_ids
        costos=self.calc_data(costos_a, context, choose_period, period_data)
        #costos=out['resultados']
        t_costos=self.total (costos, base)
        
        #gastos_oper_a = self.env['account.account'].browse(GASTOS_OPER)
        gastos_oper_a = self.env['account.financial.report'].search([('name','=','GASTOS DE OPERACIÓN')]).account_ids
        gastos_oper=self.calc_data(gastos_oper_a, context, choose_period, period_data)
        #gastos_oper=out['resultados']
        t_gastos_oper=self.total (gastos_oper, base)

        gastos_prod_fin_a= self.env['account.financial.report'].search([('name','=','GTOS Y PRODUCTOS FINANC.')]).account_ids
        gastos_prod_fin=self.calc_data(gastos_prod_fin_a, context, choose_period, period_data)
        #gastos_prod_fin=out['resultados']
        t_gastos_prod_fin=self.total (gastos_prod_fin, base)

        #gastos_prod_a = self.env['account.account'].browse(GASTOS_PROD)
        gastos_prod_a = self.env['account.financial.report'].search([('name','=','OT. GASTOS Y PRODUCTOS')]).account_ids
        gastos_prod=self.calc_data(gastos_prod_a, context, choose_period,  period_data)
        if len (gastos_prod) > 1:
            self.negative(gastos_prod[1])
        t_gastos_prod=self.total (gastos_prod, base)

        #gastos_prod_2_a = self.env['account.account'].browse(GASTOS_PROD_2)
        gastos_prod_2_a = self.env['account.financial.report'].search([('name','=','OT. VARIOS')]).account_ids
        gastos_prod_2=self.calc_data(gastos_prod_2_a, context, choose_period, period_data)
        if len (gastos_prod_2) > 1:
            self.negative(gastos_prod_2[1])
        t_gastos_prod_2=self.total (gastos_prod_2, base)

        imptos_a= self.env['account.financial.report'].search([('name','=','IMPTOS')]).account_ids
        imptos=self.calc_data(imptos_a, context, choose_period, period_data)
        #imptos=out['resultados']
        t_imptos=self.total (imptos, base)
        
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        

        
        def suma(map1, map2):
            m={}
            for key in map1.keys():                
                    m[key] = map1[key] + map2[key]
            return m

        def resta(map1, map2):
            m = {}
            for key in map1.keys():                
                    m[key] = map1[key] - map2[key]
            return m


        utilidad_bruta = resta (t_ingresos, t_costos)               
        utilidad_oper = resta (utilidad_bruta, t_gastos_oper) #dict (Counter( utilidad_bruta) - Counter(t_gastos_oper))
        total_util_oper = utilidad_oper #reduce(resta, [utilidad_bruta, t_costos], {}) #dict (Counter( utilidad_bruta) - Counter(t_gastos_oper))        
        aux = suma (total_util_oper, t_gastos_prod )
        utilidad_perd = suma (aux, t_gastos_prod_2) #dict (Counter( total_util_oper) + Counter(t_gastos_prod_2))
        
        util_neta = suma (utilidad_perd, t_imptos)
        
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
            'gastos_prod_fin': gastos_prod_fin,
            'gastos_prod': gastos_prod,
            'gastos_prod_2': gastos_prod_2, 
            'imptos': imptos,
            't_ingresos':t_ingresos,
            't_costos':t_costos,
            't_gastos_oper': t_gastos_oper, 
            't_gastos_prod_fin': t_gastos_prod_fin,
            't_gastos_prod': t_gastos_prod,
            't_gastos_prod_2': t_gastos_prod_2,
            't_imptos': t_imptos,
            'utilidad_bruta': utilidad_bruta,
            'utilidad_oper': utilidad_oper,
            'total_util_oper': total_util_oper,    
            'utilidad_perd': utilidad_perd,             
            'util_neta': util_neta 
        }
        return self.env['report'].render('account_reports_ecosoft.report_results_ecosoft', docargs)
