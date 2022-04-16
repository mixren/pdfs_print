from openpyxl import load_workbook
from win32com import client
import os


def get_column_from_excel(file_excel: str, char_column: str) -> list:
    '''Return stripped values of selected Excel column as a list'''
    wb = load_workbook(filename=file_excel)
    sheet = wb.active
    col = sheet[char_column]
    return [entry.value.strip() for entry in col]


def merge_into_single_xlsx(paths_xmls: list):
    '''2 sec per worksheet'''
    infile = os.path.abspath('merged.xlsx')

    excel = client.Dispatch("Excel.Application")
    #wb_target = excel.Workbooks.Open(infile)
    wb_target = excel.Workbooks.Add()

    try:
        for path in paths_xmls:
            wb = excel.Workbooks.Open(path)
            ws = wb.Worksheets(1)
            ws.Copy(Before=wb_target.Worksheets(1))
            wb.Close()
    
        #wb_target.Close(SaveChanges=True)
        wb_target.SaveAs(infile)
    except Exception as e:
        print(f"{e}")
    finally:
        excel.Quit()
    

def convert_xlsx_to_pdf(xlsx_path: str, pdf_file_name: str, dest_dir_path: str= None)-> str:
    '''Convert .xlsx into .pdf. Excel needs to be installed. return destination path'''
    infile = os.path.abspath(xlsx_path)
    if dest_dir_path is None:
        dest_dir_path = os.path.dirname(infile)
    outfile = os.path.join(dest_dir_path, pdf_file_name)

    excel = client.Dispatch("Excel.Application")
    sheets = excel.Workbooks.Open(infile)
    work_sheets = sheets.Worksheets[0]
    
    try:
        work_sheets.ExportAsFixedFormat(0, outfile)
    except Exception as e:
        print("Failed to convert Excel to PDF. PDF might exist already and be opened. " + str(e))
    finally:
        excel.Quit()
    
    return outfile
        
    

