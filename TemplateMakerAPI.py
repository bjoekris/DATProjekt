# pip install "fastapi[standard]"
# pip install python-docx
# pip install docx2pdf

# Used in API calls
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Used in MakeTemplate()
from docx import Document
import winreg
from docx.shared import Inches
from docx.enum.text import WD_BREAK

# Used in ConvertDocxToPDF()
import os
from docx2pdf import convert

# @app.post("MakeTemplate/api")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)


# TO DO:
# Attempt to recreate one of the templates from Kapil
# Set it up to work with Postman


def GenerateTemplate(fileName, image = None, imageWidth = None):
    # Used to find the download folder on a given computer.
    folderPath = FindFolderPath()
    templatePath = f"{folderPath}/{fileName} Invoice TemplateFile"

    doc = Document()

    doc.add_heading('Invoice', 0)

    if image != None:
        if imageWidth != None:
            doc.add_picture(image, width = Inches(imageWidth))
        else:
            doc.add_picture(image, width = Inches(1.5))
    
    doc.add_paragraph('Dear {{Name}} ,')

    p = doc.add_paragraph('Please find attached invoice for your recent purchase of ')
    p.add_run('\n\n{{Product(s)}}')
    
    [doc.add_paragraph('') for _ in range(1)]

    table = doc.add_table(rows = 1, cols = 4)
    hdrCells = table.rows[0].cells
    hdrCells[0].text = 'Product Name'
    hdrCells[1].text = 'Units'
    hdrCells[2].text = 'Unit Price'
    hdrCells[3].text = 'Total Price'
    for i in range(4):
        hdrCells[i].paragraphs[0].runs[0].font.bold = True
    
    rowCells = table.add_row().cells
    rowCells[0].text = '{{Product Name}}'
    rowCells[1].text = '{{Units}}'
    rowCells[2].text = '{{Unit Price}}'
    rowCells[3].text = '{{Total Price}}'

    doc.add_page_break()
    
    doc.add_picture('InvoEZ logo.png', width = Inches(4)).keep_together = True

    doc.add_paragraph("")

    doc.add_paragraph("Lorem ipsum odor amet, consectetuer adipiscing elit. Luctus ante faucibus habitasse dui hendrerit. Ad dis penatibus laoreet ultrices potenti ad massa. Eros ultricies dui est suscipit libero mi cursus amet. Nulla egestas lacinia molestie ipsum phasellus. Gravida porttitor dui aliquet egestas auctor morbi eu ultrices. Porta interdum sagittis nibh vitae lacinia commodo cursus. Fusce quam porta facilisi cursus cras fermentum eros pulvinar habitant. Class lectus nam pulvinar malesuada odio condimentum. Placerat pulvinar malesuada luctus dui velit massa consequat convallis.")
    doc.add_paragraph("Eleifend fames diam dui ante metus vestibulum. Ipsum proin sociosqu venenatis posuere elementum. Ac curae cras luctus volutpat imperdiet mattis nullam non ligula. Taciti metus feugiat maecenas nunc volutpat congue accumsan. Netus sed himenaeos ridiculus leo ultricies. Est habitant nec eget interdum mi conubia sodales netus. Praesent nisi urna fringilla cras aptent proin ex. Tincidunt fringilla gravida consectetur vitae a vitae, dolor velit. Dignissim nascetur himenaeos tincidunt ornare nisi lacus pellentesque ex.")
    
    doc.add_paragraph("")

    doc.add_paragraph('We apprecieate your business and please come again!').keep_together = True
    doc.add_paragraph('Sincerely').keep_together = True
    doc.add_paragraph('InvoEZ').keep_together = True

    doc.save(f"{templatePath}.docx")

def InsertDynamicData(fileName, items, name = None):
    folderPath = FindFolderPath()

    templatePath = f"{folderPath}/{fileName} Invoice TemplateFile"
    filePath = f"{folderPath}/{fileName} Invoice"
    tempPath = f"{folderPath}/{fileName} TempFile"

    doc = Document(f"{templatePath}.docx")

    for p in doc.paragraphs:
        if p.text.__contains__('{{Name}}'):
            paragraph1 = p
    
    paragraph1.text = f'Dear '
    paragraph1.add_run(f'{name}')

    for p in doc.paragraphs:
        if p.text.__contains__('{{Product(s)}}'):
            paragraph2 = p
    
    paragraph2.text = 'Please find attached invoice for your recent purchase of \n'
    for key in items:
        paragraph2.add_run('\n')
        paragraph2.add_run(str(items[key][0])).bold = True
        paragraph2.add_run(' units of ')
        paragraph2.add_run(key).bold = True
        paragraph2.add_run('.')
    
    for t in doc.tables:
        if t.cell(1, 0).text.__contains__('{{Product Name}}'):
            table = t
    
    DeleteTableRow(table.rows[1])
    for key in items:
        rowCells = table.add_row().cells
        rowCells[0].text = key
        rowCells[1].text = f'{items[key][0]:,.2f}'
        rowCells[2].text = f'{items[key][1]:,.2f}'
        rowCells[3].text = f'{items[key][0] * items[key][1]:,.2f}'
    
    doc.save(f"{tempPath}.docx")
    ConvertDocxToPDF(filePath, tempPath)

def ConvertDocxToPDF(path, tempPath):
    convert(f"{tempPath}.docx", f"{path}.pdf")
    os.remove(f"{tempPath}.docx")

def FindFolderPath():
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
    folderPath = winreg.QueryValueEx(reg_key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
    winreg.CloseKey(reg_key)

    return folderPath

def DeleteTableRow(row):
    r = row._element
    r.getparent().remove(r)
    r._p = r._element = None

if __name__ == "__main__":
    items = {"Product 1" : [10, 99.95], "Product 2" : [15, 199.95], "Product 3" : [18, 324.95], "Product 4" : [16, 499.95], "Product 5" : [19, 649.95],
        "Product 6" : [4, 1499.95], "Product 7" : [34, 124.95], "Product 8" : [150, 1749.95], "Product 9" : [6, 14999.95], "Product 10" : [60, 19.95], "Work Hours" : [22.5, 450]}
    name = "Cadana"

    image = "CadanaLogo.png"
    imageWidth = 3

    customerName = f'{name} Customer'

    generateTemplate = 0

    if generateTemplate == 1:
        GenerateTemplate(name, image, imageWidth)
    else:
        InsertDynamicData(name, items, customerName)