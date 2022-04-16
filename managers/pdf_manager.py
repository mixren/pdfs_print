from pikepdf import Pdf

TARGET_PDF = 'MergedPdf.pdf'

def merge_first_page_pdfs(paths: list, name_suffix: str=None):
    target = f"{TARGET_PDF.split('.')[0]}_{name_suffix}.pdf" if name_suffix is not None else TARGET_PDF
    pdf = Pdf.new()
    for path in paths:
        src = Pdf.open(path)
        pdf.pages.append(src.pages[0])
        src.close()
    pdf.save(target)
    pdf.close()