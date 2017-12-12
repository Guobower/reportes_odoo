# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Reporte de Balanza de Comprobacion',
    'version': '0.1',
    'summary': 'Reporte de Balanza de Comprobacion',
    'author': 'Ecosoft',
    'description': """
Reporte de Balanza de Comprobacion
    """,
    'website': 'www.ecosoft.mx.com',
    'depends': ['account','account_period_and_fiscalyear','l10n_mx_account_tree'],
    'category': 'Hidden',
    'sequence': 20,
    'data': [
        
        'wizard/wizard_trial_balance_views.xml',
        'wizard/wizard_general_balance_views.xml',
        'wizard/wizard_report_results_views.xml',
        'report/account_report.xml',
        'views/report_trialbalance.xml',
        'views/report_generalbalance.xml',
        'views/report_results.xml',
        
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': True,
}
