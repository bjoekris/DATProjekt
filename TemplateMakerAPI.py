# pip install 'fastapi[standard]'
# pip install python-docx
# pip install docx2pdf
# pip install python-dateutil

# Used in API calls
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Used in MakeTemplate() and/or InsertDynamicData()
from docx import Document
import winreg
from docx.shared import Inches
from datetime import date
from dateutil.parser import parse

# Used in ConvertDocxToPDF()
import os
from docx2pdf import convert

# @app.post('MakeTemplate/api')

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host='127.0.0.1', port=8000)


# TO DO:
# Attempt to recreate one of the templates from Kapil
# Set it up to work with Postman


def GenerateTemplate(fileName, image = None, imageWidth = None, fileNameOverride = None):
    folderPath = FindFolderPath()
    if fileNameOverride != True:
        templatePath = f'{folderPath}/{fileName} Invoice TemplateFile'
    else:
        templatePath = f'{folderPath}/{fileName}'

    doc = Document()

    doc.add_paragraph('{{Page Number}} of {{Total Pages}}').alignment = 2

    doc.add_heading('Invoice', 0)

    if image != None:
        if imageWidth != None:
            doc.add_picture(image, width = Inches(imageWidth))
        else:
            doc.add_picture(image, width = Inches(1.5))
    
    doc.add_paragraph('Dear {{Name}} ,')

    p = doc.add_paragraph('Please find attached invoice for your recent purchase of ')
    p.add_run('\n\n{{Product(s)}}')

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

    doc.add_paragraph('{{Page Number}} of {{Total Pages}}').alignment = 2

    doc.add_paragraph('Date of task execution: {{Date of Execution}}')
    doc.add_paragraph('Please ensure that all dues are paid in full before {{Date of Payment}}')
    
    doc.add_picture('InvoEZ logo.png', width = Inches(4)).keep_together = True

    doc.add_paragraph('{{Comments}}')

    doc.add_paragraph('We apprecieate your business and please come again!').keep_together = True
    doc.add_paragraph('Sincerely').keep_together = True
    doc.add_paragraph('InvoEZ').keep_together = True

    doc.save(f'{templatePath}.docx')




def InsertDynamicData(fileName, items, nameOverride, name, executionDate, paymentDate, comments = None):
    try:
        IsDate(paymentDate)
    except False:
        return("Make sure the date is formated correctly.")

    folderPath = FindFolderPath()

    if nameOverride != True:
        templatePath = f'{folderPath}/{fileName}'
    else:
        templatePath = f'{folderPath}/{fileName} Invoice TemplateFile'
    filePath = f'{folderPath}/{fileName} Invoice'
    tempPath = f'{folderPath}/{fileName} TempFile'

    doc = Document(f'{templatePath}.docx')

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
        if items[key][0] > 1:
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
        if items[key][0] > 1:
            if isinstance(items[key][0], float):
                rowCells[1].text = f'{items[key][0]:,.2f}'
            elif isinstance(items[key][0], int):
                rowCells[1].text = f'{items[key][0]}'
        rowCells[2].text = f'{items[key][1]:,.2f}'
        rowCells[3].text = f'{items[key][0] * items[key][1]:,.2f}'
    
    totalUnits = 0
    totalPrice = 0
    for key in items:
        totalUnits += items[key][0]
        totalPrice += items[key][0] * items[key][1]

    tableTotals = {'Total ex. moms' : totalUnits, 'Total ink. moms' : totalUnits}
    for key in tableTotals:
        rowCells = table.add_row().cells
        rowCells[0].text = key
        rowCells[1].text = f'{tableTotals[key]:,.2f}'
        rowCells[3].text = f'{totalPrice:,.2f}'
    
    doc.save(f'{tempPath}.docx')
    totalPages = CountPages(f'{tempPath}.docx')
    
    pageCount = 0
    for paragraph in doc.paragraphs:
        if paragraph.text.__contains__('{{Page Number}} of {{Total Pages}}'):
            pageCount += 1
            paragraph.text = f'Page {pageCount} of {totalPages}'

        if paragraph.text.__contains__('{{Date of Execution}}'):
            paragraph.text = f'Date of task execution: {executionDate}'
        if paragraph.text.__contains__('{{Date of Payment}}'):
            paragraph.text = f'Please ensure that all dues are paid in full before {paymentDate}'
        
        if paragraph.text.__contains__('{{Comments}}'):
            if comments != None:
                paragraph.text = '\n'
                for comment in comments:
                    paragraph.add_run(f'{comment}\n')
            else:
                DeleteParagraph(paragraph)

    doc.save(f'{tempPath}.docx')
    ConvertDocxToPDF(filePath, tempPath)




def CountPages(path):
    doc = Document(path)
    pages = 1    
    import re
    for p in doc.paragraphs:
        r = re.match('Chapter \d+', p.text)
        if r:
            print(r.group(), pages)
        for run in p.runs:
            if 'w:br' in run._element.xml and 'type="page"' in run._element.xml:
                pages += 1

    return pages

def ConvertDocxToPDF(path, tempPath):
    convert(f'{tempPath}.docx', f'{path}.pdf')
    os.remove(f'{tempPath}.docx')

def FindFolderPath():
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    folderPath = winreg.QueryValueEx(reg_key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
    winreg.CloseKey(reg_key)

    return folderPath

def DeleteParagraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)
    p._p = p._element = None

def DeleteTableRow(row):
    r = row._element
    r.getparent().remove(r)
    r._p = r._element = None

def IsDate(date, fuzzy = False):
    try: 
        parse(date, fuzzy=fuzzy)
        return True

    except ValueError:
        return False




if __name__ == '__main__':
    
    '--------------------------------------------------'

    items = {'Product 1' : [10, 99.95], 'Product 2' : [15, 199.95], 'Product 3' : [18, 324.95], 'Product 4' : [16, 499.95], 'Product 5' : [19, 649.95],
        'Product 6' : [4, 1499.95], 'Product 7' : [34, 124.95], 'Product 8' : [150, 1749.95], 'Product 9' : [6, 14999.95], 'Product 10' : [60, 19.95], 'Work Hours' : [22.5, 450]}
    fileName = 'Cadana Invoice TemplateFile'
    name = 'Cadana'

    image = 'CadanaLogo.png'
    imageWidth = 3

    '--------------------------------------------------'
    
    itemsHCFlyt = {'Fast pris for flytning' : [1, 9999.95], 'Fast pris for nedpakning' : [1, 249.95], 'Fast pris for udpakning' : [1, 499.95], 'Pris for opbevaring' : [1, 349.95],
        'Pris for leje af udstyr' : [8, 199.95], 'Tungløft' : [7, 99.95], 'Ekstra Arbejdstimer' : [7.5, 50]}
    fileNameHCFlyt =  'Ordrebekræftelse_opdateret'

    customerNameHCFlyt = f'H.C. Andersens Flyttefirma A/S'
    commentsHCFlyt = ['This is a comment', 'This is another comment']
    today = f'{date.today():%d-%m-%Y}'
    paymentDay = '01-01-2025'

    '--------------------------------------------------'

    generateTemplate = 0

    if generateTemplate == 1:
        GenerateTemplate(fileName, image, imageWidth, True)
    else:
        InsertDynamicData(name, itemsHCFlyt, True, customerNameHCFlyt, today, paymentDay)