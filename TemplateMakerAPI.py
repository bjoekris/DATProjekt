# pip install "fastapi[standard]"

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# Used in MakeTemplate()
from docx import Document
import winreg
from docx.shared import Inches

# Used in ConvertDocxToPDF()
import os
from docx2pdf import convert

# @app.post("MakeTemplate/api")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)


# Adding a specified Page Break does not seem to function.
def MakeTemplate(name, items, image):
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
    folderPath = winreg.QueryValueEx(reg_key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
    winreg.CloseKey(reg_key)
    filePath = f'{folderPath}/{name}'
    tempPath = f"{folderPath}/temp{name}File"

    doc = Document()
    doc.add_heading('Invoice', 0)
    doc.add_paragraph(f'Dear {name} ,')

    p2 = doc.add_paragraph('Please find attached invoice for your recent purchase of ')
    for i in items:
        p2.add_run('\n')
        p2.add_run(str(items[i][0])).bold = True
        p2.add_run(' units of ')
        p2.add_run(i).bold = True
        p2.add_run('.')
    
    [doc.add_paragraph('') for _ in range(2)]

    table = doc.add_table(rows = 1, cols = 4)
    hdrCells = table.rows[0].cells
    hdrCells[0].text = 'Product Name'
    hdrCells[1].text = 'Units'
    hdrCells[2].text = 'Unit Price'
    hdrCells[3].text = 'Total Price'
    for i in range(4):
        hdrCells[i].paragraphs[0].runs[0].font.bold = True
    
    for i in items:
        rowCells = table.add_row().cells
        rowCells[0].text = i
        rowCells[1].text = f'{items[i][0]:,.2f}'
        rowCells[2].text = f'{items[i][1]:,.2f}'
        rowCells[3].text = f'{items[i][0] * items[i][1]:,.2f}'
    
    [doc.add_paragraph('') for _ in range(2)]

    doc.add_picture(image, width = Inches(1.5))
    
    doc.add_paragraph('We apprecieate your business and please come again!')
    doc.add_paragraph('Sincerely')
    doc.add_paragraph('InvoEZ')

    doc.save(f"{tempPath}.docx")
    convertDocxToPDF(filePath, tempPath)

def convertDocxToPDF(path, tempPath):
    convert(f"{tempPath}.docx", f"{path}.pdf")
    os.remove(f"{tempPath}.docx")



items = {"Product 1" : [10, 99.95], "Product 2" : [15, 199.95], "Product 3" : [18, 324.95], "Product 4" : [16, 499.95], "Work Hours" : [22.5, 450]}

MakeTemplate("Cadana", items, 'InvoEZ logo.png')