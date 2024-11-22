from spire.doc import *
from spire.doc.common import *

def DocxToPDF(path):
    document = Document()
    
    document.LoadFromFile(f'{path}.docx')
    
    document.SaveToFile(f"{path}.pdf", FileFormat.PDF)
    document.Close()