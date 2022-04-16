import os
from models.drawing_full_name import DrawingFullName


def into_nested_dir(path:str, dir:str)->str:
    '''Get into the folder and create if it doesn't exist'''
    nested_dir = os.path.join(path, dir)
    if not os.path.exists(nested_dir):
        os.makedirs(nested_dir)
    return nested_dir

def get_local_temp_dir_path()-> str:
    '''Get "/my_temp" directory's full path and create it if doesn't exist'''
    path = os.getcwd()
    temp_dir = "my_temp"
    return into_nested_dir(path, temp_dir)


def get_existing_dir_path(path: str, dir: str)-> str:
    '''Return first directory path occurance that contains the input directory name'''
    dir_path = os.path.join(path, dir)
    if not os.path.exists(dir_path):
        try:
            dir_path = os.path.join(path, find_similar_name_dir(path, dir))
        except:
            raise
    return dir_path

def find_similar_name_dir(path: str, dir_part: str)->str:
    '''Return first directory path occurance that contains the input directory name. Case insensitive.'''
    try:
        for _, dirs, _ in os.walk(path):
            return [d for d in dirs if dir_part.lower() in d.lower()][0]
    except:
        raise
    

def find_paths_for_rasejumi_pdfs(path: str, drawing_names: list[DrawingFullName]):
    DIR_RASEJUMI = "Rasejumi ceham"
    return_path=[]
    for drawing in drawing_names:
        dir_path=""
        try:
            dir_path = get_existing_dir_path(path, drawing.dir_project_spool_name())  # Throwable
        except:
            print(f"No directory named '{drawing.dir_project_spool_name()}'")
            continue

        rasejumi_path=""
        try:
            rasejumi_path = get_existing_dir_path(dir_path, DIR_RASEJUMI)  # Throwable
        except:
            print(f"No directory named '{DIR_RASEJUMI}' in {dir}")
            continue

        dr_mod_1=drawing.name_part_no_cwt_no_zeros()
        dr_mod_2=drawing.name_part_no_cwt_no_zeros_last_dash()
        for root, _, files in os.walk(rasejumi_path):
            found=False
            for file in files:
                if dr_mod_1 in file or dr_mod_2 in file:
                    return_path.append(os.path.join(root, file))
                    found=True
                    break
            if not found:
                print(f"File '{dr_mod_1}'.pdf is not found.")

    return return_path


def find_paths(root_dir_path, destination_dir, extension)-> list:
    '''Loop over all directories and subdirectories. Return all found paths'''
    lst_res = []
    temp_prefix = "~$"
    
    for root, _, files in os.walk(root_dir_path):
        if os.path.basename(root) == destination_dir:
            for file in files:
                if file.endswith(extension) and not file.startswith(temp_prefix):
                    file_path = os.path.join(root, file)
                    lst_res.append(file_path)

    return lst_res
