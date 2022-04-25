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
    '''Return first directory path occurance that contains the input directory name. Also search for similar dir name.'''
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
        return [d for d in os.listdir(path) if dir_part.lower() in d.lower()][0]
    except:
        raise
    
def find_paths_from_list(path: str, drawing_names: list[DrawingFullName], destination_part: str):
    return_path=[]
    for drawing in drawing_names:
        path_fin = path
        lst_path = os.path.normpath(path_fin).split(os.sep)
        if len(lst_path) == 3:
            try:
                path_fin = get_existing_dir_path(path_fin, drawing.pipe_line)  # Throwable
            except:
                print(f"No directory named '{drawing.pipe_line}...'")
                continue
            
        try:
            path_fin = get_existing_dir_path(path_fin, drawing.dir_project_spool_name())  # Throwable
        except:
            print(f"No directory named '{drawing.dir_project_spool_name()}'")
            continue

        try:
            path_fin = get_existing_dir_path(path_fin, destination_part)  # Throwable
        except:
            print(f"No directory named similar to '{destination_part}' in {dir}")
            continue

        dr_mod_1= drawing.name_part_no_cwt_no_zeros()
        dr_mod_2= drawing.name_part_no_cwt_no_zeros_last_dash()

        files = [f for f in os.scandir(path_fin) if f.is_file()]
        found=False
        for file in files:
            if dr_mod_1 in file.name or dr_mod_2 in file.name:
                return_path.append(file.path)
                found=True
                break
        if not found:
            print(f"File '{dr_mod_1}'.pdf is not found.")

    return return_path


def find_paths_for_rasejumi_pdfs(path: str, drawing_names: list[DrawingFullName]):
    DIR_RASEJUMI = "Rasejumi ceham"
    return_path=[]
    for drawing in drawing_names:
        dir_path=""
        lst_path = os.path.normpath(path).split(os.sep)
        if len(lst_path) == 3:
            try:
                dir_path = get_existing_dir_path(path, drawing.pipe_line)  # Throwable
            except:
                print(f"No directory named '{drawing.pipe_line}...'")
                continue
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

        dr_mod_1= drawing.name_part_no_cwt_no_zeros()
        dr_mod_2= drawing.name_part_no_cwt_no_zeros_last_dash()

        files = [f for f in os.scandir(rasejumi_path) if f.is_file()]
        found=False
        for file in files:
            if dr_mod_1 in file.name or dr_mod_2 in file.name:
                return_path.append(file.path)
                found=True
                break
        if not found:
            print(f"File '{dr_mod_1}'.pdf is not found.")

    return return_path


def find_paths(root_dir_path: str, destination_dir: str, extension: str)-> list:
    '''Loop over all directories and subdirectories. Return all found paths matching input parameters.
    Directory names converted to lowercase, so - case insensitive.'''
    lst_res = []
    temp_prefix = "~$"
    
    for root, _, files in os.walk(root_dir_path):
        if str(os.path.basename(root)).lower() == destination_dir.lower():
            for file in files:
                if file.endswith(extension) and not file.startswith(temp_prefix):
                    file_path = os.path.join(root, file)
                    lst_res.append(file_path)

    return lst_res

def find_paths_similar_destination(root_dir_path: str, destination_dir: str, extension: str)-> list:
    '''Loop over all directories and subdirectories. Return all found paths matching input parameters, 
    where destination_dir can be part of the destination name.
    Directory names converted to lowercase, so - case insensitive.'''
    lst_res = []
    temp_prefix = "~$"
    
    for root, _, files in os.walk(root_dir_path):
        if destination_dir.lower() in str(os.path.basename(root)).lower():
            for file in files:
                if file.endswith(extension) and not file.startswith(temp_prefix):
                    file_path = os.path.join(root, file)
                    lst_res.append(file_path)

    return lst_res
