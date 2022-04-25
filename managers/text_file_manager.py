
TXT_NAME="merged"
TXT_EXT = ".txt"

def create_txt_for_list(lst: list, suffx: str)-> bool:
    file = f"{TXT_NAME}_{suffx}{TXT_EXT}"
    try:
        f=open(file, "a+")
        for s in lst:
            f.write("\n"+s.rsplit(".",1)[0].rsplit("\\",1)[1])
        f.close()
    except Exception as e:
        return False
    return True

'''def get_list_drawing_names(file_path)-> Result[list[DrawingFullName], str]:
    try:
        with open(file_path, mode='r') as doc:
            s = doc.read()
            list = s.split()
            drawings = [DrawingFullName.from_full_name_string(l) for l in list]
            drawings = drawings[::-1] if is_reversed else drawings
            return Success(drawings)
    except Exception as e:  
        return Failure(f"Can't open the .txt file. {e}")'''