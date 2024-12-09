# pip install 'fastapi[standard]'
# pip install docxtpl
# pip install docx2pdf
# pip install python-docx
# pip install requests
# pip install pillow

# Used for API calls
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

# Used in conversion of required data, when converting from UploadFile to other type
import json
import shutil

# Used for inserting data in template
from docxtpl import DocxTemplate, InlineImage
from docx import Document
from docx.shared import Inches

# Used for converting docx-format to pdf-format
import os
from docx2pdf import convert

# Used for finding a given image from URL
import requests

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
        contextFile: UploadFile = File(...),
        imageURLFile: UploadFile = File(None),
        imagesSize: int = Form(5),
        pdfName: str = Form("Invoice"),
    ):
    # Extracts the context-dictionary from .json file
    context: dict = json.loads(contextFile.file.read())
    if imageURLFile != None: imageURLs: list = json.loads(imageURLFile.file.read())
    else: imageURLs = None

    # Save a copy pf the uploaded template file
    templatePath = 'uploadedTemplate.docx'
    with open(templatePath, "wb") as buffer:
        shutil.copyfileobj(templateFile.file, buffer)
    
    tpl = DocxTemplate(templatePath)
    
    if imageURLs != None:
        index = 0
        images = []
        for url in imageURLs:
            image = FindImage(url, f'image{index}')
            
            foundImage = InlineImage(tpl, image, width = Inches(imagesSize))
            
            images.append(image)
            context[f'image{index}'] = foundImage
            
            index += 1
    
    context = InsertPageNumbers(context, templatePath)
    
    errMsg, valid = ValidateVariables(templatePath, context)
    if valid == False:
        os.remove(templatePath)
        if imageURLs != None: RemoveRenderedImages(images)
        return errMsg

    # Inserts data from the context-dictionary to the template
    tpl.render(context)
    
    tpl.save(f'{pdfName}.docx')

    if imageURLs != None: RemoveRenderedImages(images)
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

def InsertPageNumbers(context: dict, path: str):
    doc = Document(path)

    pageNumber = 1
    for p in doc.paragraphs:
        if p.text.__contains__('{{Current_Page}}'):
            subStr = p.text
            subStr = subStr.split('{{Current_Page}}')
            subStr = subStr[0] + str(pageNumber) + subStr[1]
            p.text = subStr
            pageNumber += 1
    
    doc.save(path)

    context['Total_Pages'] = str(pageNumber - 1)
    return context

def FindImage(url: str, fileName: str):
    data = requests.get(url).content
    f = open(f'{fileName}.png','wb')
    f.write(data)
    f.close()

    return f'{fileName}.png'

def RemoveRenderedImages(images):
    for image in images:
        os.remove(image)


# ------------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    uvicorn.run(app, host = '127.0.0.1', port = 8000)