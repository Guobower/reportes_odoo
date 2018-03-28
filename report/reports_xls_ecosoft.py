from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx


class ReportTrialBalance(ReportXlsx):	
	def generate_xlsx_report(self,workbook, data,lines):
		self.env['report.account.report_trialbalance_ecosoft']._get_xls(data, workbook) 
	
ReportTrialBalance('report.account.report_trialbalance_ecosoft.xlsx', 'wizard.trial.balance.ecosoft')


class ReportGeneralBalance(ReportXlsx):	
	def generate_xlsx_report(self,workbook, data,lines):
		self.env['report.account.report_generalbalance_ecosoft']._get_xls(data, workbook) 
	
ReportGeneralBalance('report.account.report_generalbalance_ecosoft.xlsx', 'wizard.general.balance.ecosoft')


class ReportResults(ReportXlsx):	
	def generate_xlsx_report(self,workbook, data,lines):
		self.env['report.account.report_results_ecosoft']._get_xls(data, workbook) 
	
ReportResults('report.account.report_results_ecosoft.xlsx', 'wizard.results.ecosoft')


class ReportDaily(ReportXlsx):	
	def generate_xlsx_report(self,workbook, data,lines):
		self.env['report.account.report_daily_ecosoft']._get_xls(data, workbook) 
	
ReportDaily('report.account.report_daily_ecosoft.xlsx', 'wizard.daily.ecosoft')


class ReportLedger(ReportXlsx):	
	def generate_xlsx_report(self,workbook, data,lines):
		self.env['report.account.report_ledger_ecosoft']._get_xls(data, workbook) 
	
ReportLedger('report.account.report_ledger_ecosoft.xlsx', 'wizard.ledger.ecosoft')
