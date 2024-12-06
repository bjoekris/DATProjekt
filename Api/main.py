# pip install 'fastapi[standard]'
# pip install docxtpl
# pip install docx2pdf
# pip install python-docx

# Used for API calls
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# Used in conversion of required data, when converting from UploadFile to other type
import json
import shutil

# Used for inserting data in template
from docxtpl import DocxTemplate
from docx import Document

# Used for converting docx-format to pdf-format
import os
from docx2pdf import convert

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post('/insert-dynamic-data/')
async def insert_dynamic_data(
        templateFile: UploadFile = File(...),
        pdfName: str = Form(...),
        contextFile: UploadFile = File(...),
        images: list[UploadFile] = File(None),
    ):
    # Extracts the context-dictionary from .json file
    context = json.loads(contextFile.file.read())
    
    # Save a copy pf the uploaded template file
    templatePath = 'uploadedTemplate.docx'
    with open(templatePath, "wb") as buffer:
        shutil.copyfileobj(templateFile.file, buffer)
    
    tpl = DocxTemplate(templatePath)

    context = InitializeContext(context)
    
    errMsg, valid = ValidateVariables(templatePath, context)
    if valid == False:
        return ValueError, errMsg

    # Inserts data from the context-dictionary to the template
    tpl.render(context)
    
    tpl.save(f'{pdfName}.docx')
    InsertPageNumbers(f'{pdfName}.docx')
    return ConvertDocxToPDF(pdfName, templatePath)

def ConvertDocxToPDF(path: str, templatePath):
    convert(f'{path}.docx', f'{path}.pdf')
    os.remove(f'{path}.docx')
    os.remove(templatePath)

    return FileResponse(f'{path}.pdf', media_type = 'application/pdf', filename = path)

def ValidateVariables(path: str, context: dict):
    doc = Document(path)
    valid = True

    keysContained = []
    keysNotContained = []
    values = []
    valuesNotInputted = []
    valuesInputted = []

    for p in doc.paragraphs:
        # All variables must begin with "{{", therefore we can find them simply by looking for this
        if p.text.__contains__('{{') and not (p.text.__contains__('{% for') or p.text.__contains__('{% endfor')):
            tempValues = p.text.rsplit('{{')

            for temp in tempValues:
                if not temp.__contains__('}}'):
                    tempValues.remove(temp)

            # I don't know why, but it only seems to be able to do one of the variables per for-loop...
            # It doesn't work correctly with a single for-loop, there must be one for each variable in the tempValues list
            for _ in range(len(tempValues)):
                for tempValue in tempValues:
                    tempValues.remove(tempValue)
                    tempValue = tempValue.split('}}')[0]
                    tempValues.append(tempValue)

            for temp in tempValues:
                if not values.__contains__(temp):
                    values.append(temp)

    # Ignores lists, because these are not acounted for as variables in the template
    # It is also not seen as an error, if these are empty
    for key in context:
        if not isinstance(context[key], list): keysNotContained.append(key)
    for value in values:
        valuesNotInputted.append(value)
    
    for value in values:
        for key in context:
            if value == key:
                keysContained.append(key)
                keysNotContained.remove(key)

                valuesInputted.append(value)
                valuesNotInputted.remove(value)
    
    # Builds the exception string, so it can be returned
    errorMsg = ''
    if not len(keysNotContained) == 0:
        for key in keysNotContained:
            errorMsg += f'{key} was not found in template. '
        valid = False
    
    if not len(valuesNotInputted) == 0:
        for value in valuesNotInputted:
            errorMsg += f'{value} was not found in context. '
        valid = False
    
    return errorMsg, valid

# Inserts the total price to the context dictionary, this is done to automate the proccess
# I would suggest moving this out of the python file and place it in the WebApp
def InsertTotalPrices(context: dict):
    index = 0
    totalPrice = 0
    for i in context['itemsTable']:
        context['itemsTable'][index]['priceTotal'] = i['units'] * i['priceUnit']
        totalPrice += context['itemsTable'][index]['priceTotal']

        index += 1

    context['itemsTable'].append(
            {
                'type' : 'Pris eks. moms',
                'units' : '',
                'priceUnit' : '',
                'priceTotal' : "%.2f" % totalPrice,
            }
    )
    context['itemsTable'].append(
            {
                'type' : 'Pris inkl. moms',
                'units' : '',
                'priceUnit' : '',
                'priceTotal' : "%.2f" % (totalPrice * 1.25),
            }
    )
    context['Total_Price'] = "%.2f" % (totalPrice * 1.25)
    return context

def InsertPageNumbers(path: str):
    doc = Document(path)

    pageNumber = 1
    for p in doc.paragraphs:
        if p.text.__contains__('{{'):
            subStr = p.text
            subStr = subStr.split('{{Current_Page}}')
            subStr = subStr[0]+str(pageNumber)+subStr[1]
            p.text = subStr
            pageNumber += 1
    
    doc.save(path)
    tpl = DocxTemplate(path)

    context = {'Total_Pages' : str(pageNumber - 1)}
    tpl.render(context)

    tpl.save(path)

# Completes the context dictionary, by adding the last required variables
# I would suggest moving this out of the python file and place it in the WebApp
def InitializeContext(context):
    context = InsertTotalPrices(context)
    context['Current_Page'] = '{{Current_Page}}'
    context['Total_Pages'] = '{{Total_Pages}}'
    return context


# ------------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host = '127.0.0.1', port = 8000)