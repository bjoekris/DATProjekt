# Brugt til at indsætte dynamiske data i word skabelon
from docxtpl import DocxTemplate, InlineImage
from docx import Document
from docx.shared import Inches
from fastapi.responses import FileResponse
from fastapi import HTTPException

# Brugt til at konvertere fra docx-format til pdf-format
import os
from docx2pdf import convert

# Brugt til at finde et givent billede, fra URL
import requests

def InsertDynamicData(
        templatePath: str,
        context: dict,
        pdfName: str,
        isTest: bool = False,
    ):
    ## -------------------------------------- Skrevet af Magnus -------------------------------------- ##
    # Finder og åbner den kopierede skabelon som DocxTemplate objekt
    tpl = DocxTemplate(templatePath)
    
    # Finder givene billeder fra URL, og ligger den i context-dictionary
    index = 0
    imagesToRemove = []
    if context.__contains__('Images'):
        context['InlineImages'] = []
        for image in context['Images']:
            if image['Size'] > 7.5:
                raise HTTPException(status_code = 400, details = f'{image["URL"]} has size {image["Size"]}. It cannot exceed 8.')
            
            foundImage = FindImage(image['URL'], f'image{index}')
            if image['Positioned'] == 'True':
                context[f'Image{index}'] = InlineImage(tpl, foundImage, width = Inches(image['Size']))
            
            else:
                context['InlineImages'].append(InlineImage(tpl, foundImage, width = Inches(image['Size'])))

            imagesToRemove.append(f'image{index}.png')
            index += 1
        
        context.pop('Images')

    # Validere context- og skabelon-variabler
    errMsg, valid = ValidateVariables(templatePath, context)
    if valid == False:
        if isTest == False:
            os.remove(templatePath)
        
        if len(imagesToRemove) > 0:
            for image in imagesToRemove: os.remove(image)
        
        if isTest == True: print(errMsg)
        
        raise HTTPException(status_code = 400, detail = errMsg)

    # Indsætter data fra context-dictionary til skabelon
    try:
        tpl.render(context)
    
    except Exception:
        errMsg = 'One, or more, URLs are causing errors.'
        if isTest == False:
            os.remove(templatePath)
        
        if len(imagesToRemove) > 0:
            for image in imagesToRemove: os.remove(image)
        
        if isTest == True: print(errMsg)
        
        raise HTTPException(status_code = 400, detail = errMsg)
    
    # Gemmer og konvertere til PDF
    tpl.save(f'{pdfName}.docx')
    if len(imagesToRemove) > 0:
        for image in imagesToRemove: os.remove(image)
    
    # Returnere færdig PDF
    return ConvertDocxToPDF(pdfName, templatePath, isTest)
    ## ---------------------------------------------------------------------------------------------- ##

## ---------------------------------------- Skrevet af Magnus --------------------------------------- ##
def ConvertDocxToPDF(path: str, templatePath: str, isTest: bool):
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
    f = open(f'{fileName}.png',"wb")
    f.write(data)
    f.close()

    return f'{fileName}.png'
## -------------------------------------------------------------------------------------------------- ##