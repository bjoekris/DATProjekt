# Brugt til API kald
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

# Brugt til i konversionen af nødvændig data, ved konvertering fra .json til given datatype
import json
import shutil

# Brugt til at indsætte dynamiske data i word skabelon
from docxtpl import DocxTemplate, InlineImage
from docx import Document
from docx.shared import Inches

# Brugt til at konvertere fra docx-format til pdf-format
import os
from docx2pdf import convert

# Brugt til at finde et givent billede, fra URL
import requests

## --------------------------------------- Skrevet af Bjørn ----------------------------------------- ##
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
## -------------------------------------------------------------------------------------------------- ##

## ----------------------------------- Skrevet af Magnus og Bjørn ----------------------------------- ##
@app.post('/insert-dynamic-data/')
async def insert_dynamic_data(
        templateFile: UploadFile = File(...),
        contextFile: UploadFile = File(...),
        imageURLFile: UploadFile = File(None),
        pdfName: str = Form("Invoice"),
    ):
    ## ----------------------------------- Skrevet af Magnus ---------------------------------------- ##
    # Ekstrahere context-dictionary og imageURLs-liste fra .json filer
    context: dict = json.loads(contextFile.file.read())
    if imageURLFile != None: imageURLs: dict = json.loads(imageURLFile.file.read())
    else: imageURLs = None
    ## ---------------------------------------------------------------------------------------------- ##

    ## ------------------------------------ Skrevet af Bjørn ---------------------------------------- ##
    # Gemmer kopi af uploadede skabelon fil
    templatePath = 'uploadedTemplate.docx'
    with open(templatePath, "wb") as buffer:
        shutil.copyfileobj(templateFile.file, buffer)
    ## ---------------------------------------------------------------------------------------------- ##
    
    ## ------------------------------------ Skrevet af Magnus --------------------------------------- ##
    # Finder og åbner den kopierede skabelon som DocxTemplate objekt
    tpl = DocxTemplate(templatePath)
    
    # Finder givene billeder fra URL, og ligger den i context-dictionary
    if imageURLs != None:
        index = 0
        images = []
        for url in imageURLs:
            image = FindImage(url, f'image{index}')
            
            context[f'image{index}'] = InlineImage(tpl, image, width = Inches(imageURLs[url]))
            
            images.append(image)
            index += 1
    
    # Validere context- og skabelon-variabler
    errMsg, valid = ValidateVariables(templatePath, context)
    if valid == False:
        os.remove(templatePath)
        if imageURLs != None: RemoveRenderedImages(images)
        return errMsg

    # Indsætter data fra context-dictionary til skabelon
    tpl.render(context)
    
    # Gemmer og konvertere til PDF
    tpl.save(f'{pdfName}.docx')
    if imageURLs != None: RemoveRenderedImages(images)
    return ConvertDocxToPDF(pdfName, templatePath)
    ## ---------------------------------------------------------------------------------------------- ##

## ----------------------------------- Skrevet af Magnus og Bjørn ----------------------------------- ##
def ConvertDocxToPDF(path: str, templatePath: str, isTest: bool = False):
    ## ------------------------------------ Skrevet af Magnus --------------------------------------- ##
    convert(f'{path}.docx', f'{path}.pdf')
    os.remove(f'{path}.docx')
    if isTest == False: os.remove(templatePath)
    ## ---------------------------------------------------------------------------------------------- ##

    ## ------------------------------------ Skrevet af Bjørn ---------------------------------------- ##
    return FileResponse(f'{path}.pdf', media_type = 'application/pdf', filename = path)
    ## ---------------------------------------------------------------------------------------------- ##

## ---------------------------------------- Skrevet af Magnus --------------------------------------- ##
def ValidateVariables(path: str, context: dict):
    doc = Document(path)
    valid = True

    keysContained = []
    keysNotContained = []
    values = []
    valuesNotInputted = []
    valuesInputted = []

    for p in doc.paragraphs:
        # Alle variabler i skabelonet starter med "{{"
        # Derfor kan man finde alle variabler ved at lede gennem alt tekst i dokumentet efter disse
        if p.text.__contains__('{{') and not (p.text.__contains__('{% for') or p.text.__contains__('{% endfor')):
            tempValues = p.text.rsplit('{{')

            for temp in tempValues:
                if not temp.__contains__('}}'):
                    tempValues.remove(temp)

            # Isolere skabelon-variablerne fra de sidste klammer, så de kan sammenlignes med context-variablerne
            foundValues = []
            for i in range(len(tempValues)):
                tempValue = tempValues[i].split('}}')[0]
                foundValues.append(tempValue)

            for value in foundValues:
                if not values.__contains__(value):
                    values.append(value)

    # Ignoere lister, da disse godt må være tomme
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
    
    # Bygger exception-string, så den kan returneres til brugeren
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

def FindImage(url: str, fileName: str):
    data = requests.get(url).content
    f = open(f'{fileName}.png','wb')
    f.write(data)
    f.close()

    return f'{fileName}.png'

def RemoveRenderedImages(images):
    for image in images:
        os.remove(image)
## -------------------------------------------------------------------------------------------------- ##

## --------------------------------------- Skrevet af Bjørn ----------------------------------------- ##
if __name__ == '__main__':
    uvicorn.run(app, host = '127.0.0.1', port = 8000)
## -------------------------------------------------------------------------------------------------- ##