class DrawingFullName:

    def __init__(self, pipe_line, drawing_short) -> None:
        '''
        pipe_line: MP21-77
        drawing_short: 32.01
        '''
        self.pipe_line = pipe_line
        self.drawing_short = drawing_short


    @classmethod
    def from_valid_input(cls, pipe_line: str, drawing_short: str):
        return cls(pipe_line, drawing_short)

    @classmethod
    def from_full_name_string(cls, s: str):
        '''Example: CWT.MP21-77-32.01.00'''
        if len(s.strip().split(".")) != 4:
            raise ValueError(f"'{s}' should contain three '.'. Example: CWT.MP21-77-32.01.00")
        if len(s.strip().split("-")) != 3:
            raise ValueError(f"'{s}' should contain two '-'. Example: CWT.MP21-77-32.01.00")
        if 'CWT' not in s:
            raise ValueError(f"'{s}' should contain 'CWT'. Example: CWT.MP21-77-32.01.00")
        if len(s.strip()) < 11:
            raise ValueError(f"'{s}' should be longer than 11 symbols. Example: CWT.MP21-77-32.01.00")
        pl, ds = s.strip().split(".", 1)[1].rsplit(".", 1)[0].rsplit("-", 1)
        return cls(pl, ds)


    '''@staticmethod
    def is_valid_part_name_cwt_with_zeros(s: str)-> Result[str,str]:
        #Example: CWT.MP21-77-32.01.00
        if not s:
            return Failure(f"Should be not empty")
        elif len(s.split('.')) != 4:
            return Failure(f"Should be three dots '.' in '{s}'")
        elif len(s.split('-')) != 3:
            return Failure(f"Should be 2 dashes '-' in '{s}'")
        elif len(s) < 12:
            return Failure("Is too short")
        else:
            return Success(s)'''


    def name_with_zeros(self):
        '''Example: CWT.MP21-77-32.01.00'''
        return f"CWT.{self.pipe_line}-{self.drawing_short}.00"

    def dir_project_spool_name(self):
        '''Example: CWT.MP21-77-32'''
        return f"CWT.{self.pipe_line}-{self.drawing_short.split('.')[0]}"

    def name_part_no_cwt_no_zeros(self):
        '''Example: MP21-77-32.01'''
        return f"{self.pipe_line}-{self.drawing_short}"

    def name_part_no_cwt_no_zeros_last_dash(self):
        '''Example: MP21-77-32-01'''
        return f"{self.pipe_line}-{self.drawing_short.replace('.', '-')}"
