# -*- coding: utf-8 -*-
    
class UtilsXlsx():

    @staticmethod
    def add_header(header, worksheet, bold, row):
        col=0                
        for h in header:                 
            worksheet.write_string (row, col, h, bold)
            col+=1
    
    @staticmethod
    def add_row(reg, worksheet, row):                
        col=0
        for r in reg:
            if type (r)==int:                
                    worksheet.write_number(row, col, r)
            else:
                worksheet.write_string(row, col, r)                             
            col+=1
    
    @staticmethod
    def add_matrix( rows, worksheet, row_headers, bold):                
        row = 0        
        for r in rows:             
            if row in row_headers:
                #print '0'
                UtilsXlsx.add_header(r, worksheet, bold, row)
            else:
                #print '1'
                UtilsXlsx.add_row(r, worksheet, row)                
            row+=1
    