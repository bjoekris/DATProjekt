# pip install "fastapi[standard]"

from SaveToPDF import DocxToPDF

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import docx
from docx import Document
from docx.shared import Inches
from docx.shared import Pt, RGBColor

import winreg




"""
@app.post("/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""

def MakeTemplate(name, product, unit, price):
    doc = Document()
    doc.add_heading('Invoice', 0)
    doc.add_paragraph(f'Dear {name} ,')
    p2 = doc.add_paragraph('Please find attached invoice for your recent purchase of ')
    p2.add_run(str(unit)).bold = True
    p2.add_run(' units of ')
    p2.add_run(product).bold = True
    p2.add_run('.')

    [doc.add_paragraph('') for _ in range(2)]

    table = doc.add_table(rows=1, cols=4)
    hdrCells = table.rows[0].cells
    hdrCells[0].text = 'Product Name'
    hdrCells[1].text = 'Units'
    hdrCells[2].text = 'Unit Price'
    hdrCells[3].text = 'Total Price'
    for i in range(4):
        hdrCells[i].paragraphs[0].runs[0].font.bold = True
    
    rowCells = table.add_row().cells
    rowCells[0].text = product
    rowCells[1].text = f'{unit:,.2f}'
    rowCells[2].text = f'{price:,.2f}'
    rowCells[3].text = f'{unit * price:,.2f}'

    [doc.add_paragraph('') for _ in range(20)]

    doc.add_paragraph('We apprecieate your business and please come again!')
    doc.add_paragraph('Sincerely')
    doc.add_paragraph('InvoEZ')

    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")

    folderPath = winreg.QueryValueEx(reg_key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]

    winreg.CloseKey(reg_key)

    path = f'{folderPath}/{name}'

    doc.save(f'{path}.docx')
    DocxToPDF(path)

MakeTemplate('Cadana', 'some product', 100, 1000)