from odoo import models


class ReportTrialBalance(models.AbstractModel):
	_name = 'report.account_reports_ecosoft.report_trialbalance_ecosoft.xlsx'
	_inherit = 'report.report_xlsx.abstract'	
	def generate_xlsx_report(self,workbook, data,lines):
		self.env['report.account_reports_ecosoft.report_trialbalance_ecosoft']._get_xls(data, workbook) 
	
#ReportTrialBalance('report.account.report_trialbalance_ecosoft.xlsx', 'wizard.trial.balance.ecosoft')


class ReportGeneralBalance(models.AbstractModel):	
	_name = 'report.account_reports_ecosoft.report_general_ecosoft.xlsx'
	_inherit = 'report.report_xlsx.abstract'	
	def generate_xlsx_report(self,workbook, data,lines):
		self.env['report.account_reports_ecosoft.report_generalbalance_ecosoft']._get_xls(data, workbook) 
	
#ReportGeneralBalance('report.account.report_generalbalance_ecosoft.xlsx', 'wizard.general.balance.ecosoft')


class ReportResults(models.AbstractModel):	
	_name = 'report.account_reports_ecosoft.report_results_ecosoft.xlsx'
	_inherit = 'report.report_xlsx.abstract'	
	def generate_xlsx_report(self,workbook, data,lines):
		self.env['report.account_reports_ecosoft.report_results_ecosoft']._get_xls(data, workbook) 
	
#ReportResults('report.account.report_results_ecosoft.xlsx', 'wizard.results.ecosoft')


class ReportDaily(models.AbstractModel):	
	_name = 'report.account_reports_ecosoft.report_daily_ecosoft.xlsx'
	_inherit = 'report.report_xlsx.abstract'	
	def generate_xlsx_report(self,workbook, data,lines):
		self.env['report.account_reports_ecosoft.report_daily_ecosoft']._get_xls(data, workbook) 
	
#ReportDaily('report.account.report_daily_ecosoft.xlsx', 'wizard.daily.ecosoft')


class ReportLedger(models.AbstractModel):	
	_name = 'report.account_reports_ecosoft.report_ledger_ecosoft.xlsx'
	_inherit = 'report.report_xlsx.abstract'	
	def generate_xlsx_report(self,workbook, data,lines):
		self.env['report.account_reports_ecosoft.report_ledger_ecosoft']._get_xls(data, workbook) 
	
#ReportLedger('report.account.report_ledger_ecosoft.xlsx', 'wizard.ledger.ecosoft')
