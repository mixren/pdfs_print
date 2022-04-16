def remove_last_zeros(s: str)-> str:
    return s.rsplit(".", 1)[0]