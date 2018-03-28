# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Reportes de contabilidad Ecosoft',
    'version': '0.1',
    'summary': 'Reporte balanza de comprobación, Belanace general, Estado de resultados, Libro diario y Libro mayor',
    'author': 'Abraham Martínez y Antonio Silva ',
    'description': """
Reportes de Ecosoft
    """,
    'website': 'www.ecosoft.com.mx',
    'depends': ['account','account_period_and_fiscalyear','l10n_mx_account_tree', 'report_xlsx'],
    'category': 'Hidden',
    'sequence': 20,
    'data': [
        
        'wizard/wizard_trial_balance_views.xml',
        'wizard/wizard_general_balance_views.xml',
        'wizard/wizard_report_results_views.xml',
        'wizard/wizard_daily_views.xml',
        'wizard/wizard_ledger_views.xml',
        'report/account_report.xml',
        'views/report_trialbalance.xml',
        'views/report_generalbalance.xml',
        'views/report_results.xml',
        'views/report_daily.xml',
        'views/report_ledger.xml',
        
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': True,
}
