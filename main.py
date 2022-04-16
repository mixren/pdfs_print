#!/usr/bin/env python

import os
import time
import managers.connection_manager as cm
import managers.excel_manager as exm
import managers.pipe_drawing_manager as pdm
import managers.pdf_manager as pdfm
import managers.file_explorer_manager as fexm
import managers.text_file_manager as tfm
from models.drawing_full_name import DrawingFullName


def merge_pdf_first_pages():
    root_2021 = "Z:\CWT Documents\\2021"
    dir_21_77 = "MP21-77 BP101_POX_CS"
    dir_21_81 = "MP21-81 PP108_POX_CS"
    dir_21_80 = "MP21-80 BP101_SL_CS"

    file = "print_14_04.xlsx"

    root_path=os.path.join(root_2021, dir_21_77)

    col_values=exm.get_column_from_excel(file_excel=file, char_column="A")
    drawings = list(map(DrawingFullName.from_full_name_string, col_values))
    #drawings = list(map(pdm.remove_last_zeros, col_values))

    paths_ras = fexm.find_paths_for_rasejumi_pdfs(root_path, drawings)
    if len(drawings) == len(paths_ras):
        print("All files found.")
    #dirs_from_excel = get_dirs_from_excel(file_excel=file, char_column="A")
    #paths_rasejumi = find_paths_for_rasejumi_pdfs_2(root_path, dirs_from_excel)

    print("Merging pdfs...")
    pdfm.merge_first_page_pdfs(paths_ras)


def merge_xlsx():
    root_2021 = "Z:\CWT Documents\\2021"
    dir_21_81 = "MP21-81 PP108_POX_CS"
    destination_dir = "DWR"
    file_extension = ".xlsx"
    test_paths_xlsx = ['Z:\\CWT Documents\\2021\\MP21-81 PP108_POX_CS\\CWT.MP21-81-1\\DWR\\CWT.MP21-81-1.01.00.xlsx', 'Z:\\CWT Documents\\2021\\MP21-81 PP108_POX_CS\\CWT.MP21-81-1\\DWR\\CWT.MP21-81-1.02.00.xlsx', 'Z:\\CWT Documents\\2021\\MP21-81 PP108_POX_CS\\CWT.MP21-81-1\\DWR\\CWT.MP21-81-1.03.00.xlsx', 'Z:\\CWT Documents\\2021\\MP21-81 PP108_POX_CS\\CWT.MP21-81-1\\DWR\\CWT.MP21-81-1.04.00.xlsx']

    root_path=os.path.join(root_2021, dir_21_81)

    #paths_xlsx = fexm.find_paths(root_path, destination_dir, file_extension)
    paths_xlsx = test_paths_xlsx
    print(f"Found {len(paths_xlsx)} Excel documents.")

    is_txt_created = tfm.create_txt_for_list(paths_xlsx)
    if is_txt_created:
        print(f"Text file '{tfm.TXT_FILE}' successfully created")
    else:
        print(f"Text file '{tfm.TXT_FILE}' failed to create.")
    
    print(f"Merging xmls...")
    exm.merge_into_single_xlsx(paths_xlsx)



if __name__ == '__main__':
    if not cm.is_connected_to_server():
        print("You are not connected to the CWT server")

    else:
        start = time.time()
        merge_pdf_first_pages()
        #merge_xlsx()
        end = time.time()
        print(f"Success \nTime elapsed: {round(end-start,4)} sec")
