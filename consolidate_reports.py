import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import os
import sys

def combine_reports(report_files, output_report):
    wb = Workbook()
    wb.remove(wb.active)
    
    for report_file in report_files:
        sheet_name = os.path.splitext(os.path.basename(report_file))[0]
        
        try:
            df = pd.read_excel(report_file, sheet_name="Scan Report")  # Adjust if necessary
        except ValueError:
            print(f"Sheet 'Scan Report' not found in {report_file}. Skipping this file.")
            continue
        
        ws = wb.create_sheet(title=sheet_name[:31])
        
        for row in dataframe_to_rows(df, index=False, header=True):
            ws.append(row)
    
    wb.save(output_report)
    print(f"Combined report saved as {output_report}")

if len(sys.argv) < 3:
    print("Usage: python combine_reports.py <output_report.xlsx> <report1.xlsx> <report2.xlsx> ...")
    sys.exit(1)

output_report = sys.argv[1]
report_files = sys.argv[2:]

combine_reports(report_files, output_report)
