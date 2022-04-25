#!/usr/bin/env python

import os
import time
import tkinter as tk
from tkinter import messagebox
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

    file = "print_80.xlsx"

    root_path=os.path.join(root_2021, dir_21_80)

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
        print(f"Text file successfully created")
    else:
        print(f"Text file failed to create.")
    
    print(f"Merging xmls...")
    exm.merge_into_single_xlsx(paths_xlsx)


def my_var_parts_observer(var, index, mode):
    toggle_list_search(v_parts.get())


def toggle_list_search(radio_var: str):
    if radio_var == '1':
        ent_list_select.configure(state=tk.DISABLED)
        btn_list_select.configure(state=tk.DISABLED)
    else:
        ent_list_select.configure(state=tk.NORMAL)
        btn_list_select.configure(state=tk.NORMAL)


def select_list_xlsx():
    import tkinter.filedialog as fd
    path = fd.askopenfilename(title="Select an Excel list of parts", filetypes=[("Excel files","*.xlsx")], initialdir=os.getcwd())
    if path:
        ent_list_select.delete(0, tk.END)
        ent_list_select.insert(0, path)
        ent_list_select.xview_moveto(1)

def select_root_folder():
    import tkinter.filedialog as fd
    path = fd.askdirectory(title="Select Root Folder")
    if path:
        ent_root_dir.delete(0, tk.END)
        ent_root_dir.insert(0, path)
        ent_root_dir.xview_moveto(1)


def generate_2():
    if not cm.is_connected_to_server():
        msg = "You are not connected to the CWT server"
        print(msg)
        lbl_result.config(text=msg, fg="red")

    root_path = ent_root_dir.get()

    # PDF or Excel
    if v_files.get() == '1':
        # PDF
        destination_dir = "mi ceham" # approximate name to "Rasejumi Ceham"
        file_extension = ".pdf"
        path_files = []
        msg_1 = f"Searching 'Rasejumi Ceham' directories and inner '{file_extension}' files. It may take some time..."
    else:
        # Excel
        destination_dir = "DWR"
        file_extension = ".xlsx"
        path_files = []
        msg_1 = f"Searching '{destination_dir}' directories and inner '{file_extension}' files. It may take some time..."
    
    # All or Selected
    if v_parts.get() == '1':
        # ALL
        print(msg_1)
        if v_files.get() == '1':
            path_files = fexm.find_paths_similar_destination(root_path, destination_dir, file_extension)
        else:
            path_files = fexm.find_paths(root_path, destination_dir, file_extension)
        s = "\n".join(list(map(os.path.basename,path_files)))
        print(f"Search is completed. {len(path_files)} {file_extension} files found. Namely: \n{s}")

        is_txt_created = tfm.create_txt_for_list(path_files, file_extension[1:])
        if is_txt_created:
            print(f"Text file successfully created")
        else:
            print(f"Text file failed to create.")
    else:
        # Select from list
        col_values=exm.get_column_from_excel(file_excel=ent_list_select.get(), char_column="A")
        drawings = list(map(DrawingFullName.from_full_name_string, col_values))
        path_files = fexm.find_paths_from_list(root_path, drawings, destination_dir)
        if len(drawings) == len(path_files):
            print("All files found.")

    print(f"Total {len(path_files)} files")
    response = messagebox.askokcancel("askokcancel", f"{len(path_files)} files found. It will take around {round(1.2*len(path_files))} seconds. Merge?")
    if response == 1:
        print("Merging...")
        if v_files.get() == '1':
            pdfm.merge_first_page_pdfs(path_files)
        else:
            exm.merge_into_single_xlsx(path_files)
        lbl_result.config(text=f"Successfully Merged", fg="green")
        print("Successfully Merged")
    else:
        print("Cancelled")
        lbl_result.config(text=f"Cancelled", fg="red")


'''def generate():
    root_path = ent_root_dir.get()

    if v_files.get() == '1':
        # PDF
        destination_dir = "mi ceham" # approximate name to "Rasejumi Ceham"
        file_extension = ".pdf"
        path_files = []
        if v_parts.get() == '1':
            print(f"Searching 'Rasejumi Ceham' directories and inner '{file_extension}' files. It may take some time...")
            path_files = fexm.find_paths_similar_destination(root_path, destination_dir, file_extension)
            s = "\n".join(list(map(os.path.basename,path_files)))
            print(f"Search is completed. {len(path_files)} {file_extension} files found. Namely: \n{s}")

            is_txt_created = tfm.create_txt_for_list(path_files, file_extension[1:])
            if is_txt_created:
                print(f"Text file '{tfm.TXT_FILE}' successfully created")
            else:
                print(f"Text file '{tfm.TXT_FILE}' failed to create.")
        
        else:
            col_values=exm.get_column_from_excel(file_excel=ent_list_select.get(), char_column="A")
            drawings = list(map(DrawingFullName.from_full_name_string, col_values))

            path_files = fexm.find_paths_from_list(root_path, drawings, destination_dir)
            if len(drawings) == len(path_files):
                print("All files found.")
            #dirs_from_excel = get_dirs_from_excel(file_excel=file, char_column="A")
            #paths_rasejumi = find_paths_for_rasejumi_pdfs_2(root_path, dirs_from_excel)

        print(f"Total {len(path_files)} files")
        response = messagebox.askokcancel("askokcancel", f"{len(path_files)} files found. Merge?")
        if response == 1:
            print("Merging pdfs...")
            pdfm.merge_first_page_pdfs(path_files)
        else:
            print("Cancelled")

    else:
        # Excel
        destination_dir = "DWR"
        file_extension = ".xlsx"
        path_files = []
        if v_parts.get() == '1':
            print(f"Searching '{destination_dir}' directories and inner '{file_extension}' files. It may take some time...")
            path_files = fexm.find_paths(root_path, destination_dir, file_extension)
            s = "\n".join(list(map(os.path.basename, path_files)))
            print(f"Search is completed. {len(path_files)} {file_extension} files found. Namely: \n{s}")

            is_txt_created = tfm.create_txt_for_list(path_files, file_extension[1:])
            if is_txt_created:
                print(f"Text file '{tfm.TXT_FILE}' successfully created")
            else:
                print(f"Text file '{tfm.TXT_FILE}' failed to create.")

        else:
            col_values=exm.get_column_from_excel(file_excel=ent_list_select.get(), char_column="A")
            drawings = list(map(DrawingFullName.from_full_name_string, col_values))

            path_files = fexm.find_paths_from_list(root_path, drawings, destination_dir)
            if len(drawings) == len(path_files):
                print("All files found.")

        print(f"Total {len(path_files)} files")
        response = messagebox.askokcancel("askokcancel", f"{len(path_files)} files found. Merge?")
        if response == 1:
            print(f"Merging xmls. It takes about 2 sec per worksheet...")
            exm.merge_into_single_xlsx(path_files)
        else:
            print("Cancelled")'''


if __name__ == '__main__':
    root = tk.Tk()
    root.title("CWT File Merger")

    # Frame Root dir
    frm_root_dir = tk.Frame(master=root)
    frm_root_dir.grid(row=0, column=0, sticky="w", pady=20, padx=50)

    lbl_root_dir = tk.Label(frm_root_dir, text= "Root Path: ")
    ent_root_dir = tk.Entry(frm_root_dir, width=40)
    btn_root_dir = tk.Button(frm_root_dir, text= "Select", command=select_root_folder)
    lbl_root_dir.grid(row=0, column=0, sticky="w", padx=10)
    ent_root_dir.grid(row=0, column=1, sticky="e", padx=10)
    btn_root_dir.grid(row=0, column=2, sticky='e', padx=10)
    ent_root_dir.insert(0, "Z:\CWT Documents\\2021")


    # Parts to Search
    lbl_root_dir = tk.Label(root, text= "Parts to search:")
    lbl_root_dir.grid(row=1, column=0, sticky="w", padx=16, pady=20)


    v_parts = tk.StringVar(root, "1")
    v_parts.trace_add('write', my_var_parts_observer)
    values = {"All parts" : "1",
              "Selected parts (provide list as .xlsx, part example: CWT.MP21-80-24.01.00)" : "2"}
    for i, (text, value) in enumerate(values.items()):
        tk.Radiobutton(root, text = text, variable = v_parts, value = value).grid(row=2+i, column=0, sticky='w', padx=26, pady=2) # pack(side = tk.TOP, ipady = 5)


    frm_list_select = tk.Frame(master=root)
    frm_list_select.grid(row=4, column=0, sticky="w", pady=4, padx=26)
    ent_list_select = tk.Entry(frm_list_select, width=40)
    btn_list_select = tk.Button(frm_list_select, text= "Select", command=select_list_xlsx)
    ent_list_select.grid(row=0, column=0, sticky="e", padx=20)
    btn_list_select.grid(row=0, column=1, sticky='e', padx=5)
    toggle_list_search('1')


    # Files to Merge
    lbl_root_dir = tk.Label(root, text= "Files to merge:")
    lbl_root_dir.grid(row=5, column=0, sticky="w", padx=16, pady=20)


    v_files = tk.StringVar(root, "1")
    values = {"PDFs. Первая страцица чертежа из \"Rasejumi Ceham\"" : "1",
              "Excels. Запись Контроля Качества Сварки из папки \"DWR\"" : "2"} # Dictionary to create multiple buttons
    for i, (text, value) in enumerate(values.items()):
        tk.Radiobutton(root, text = text, variable = v_files, value = value).grid(row=6+i, column=0, sticky='w', padx=26, pady=2) # pack(side = tk.TOP, ipady = 5)


    # Button
    btn_generate = tk.Button(master=root, width=30, height=2, text="Check before Merge", command=generate_2)
    btn_generate.grid(row=8, column=0, pady=30, padx=20)

    
    # Result Label
    lbl_result = tk.Label(master=root, fg="grey", font=('Arial', 10))
    lbl_result.grid(row=9, column=0, pady=14, padx=20)

    

    '''if not cm.is_connected_to_server():
        print("You are not connected to the CWT server")

    else:
        start = time.time()
        merge_pdf_first_pages()
        #merge_xlsx()
        end = time.time()
        print(f"Success \nTime elapsed: {round(end-start,4)} sec")'''

    root.mainloop()