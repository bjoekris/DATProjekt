# Used for inserting dynamic data to word template
from docxtpl import DocxTemplate, InlineImage
from docx import Document
from docx.shared import Inches
from fastapi.responses import FileResponse

# Used for converting from docx to pdf
import os
from docx2pdf import convert

# Used for retrieving image files from URL
import requests

def InsertDynamicData(
        templatePath: str,
        context: dict,
        pdfName: str,
        isTest: bool = False,
    ):
    # Finds and open the copied template as a DocxTemplate object
    tpl = DocxTemplate(templatePath)
    
    # Finds images from URL and puts them into the context-dictionary
    index = 0
    imagesToRemove = []
    if context.__contains__('Images'):
        context["InlineImages"] = []
        for image in context['Images']:
            if image['Size'] > 7.5: return f'{image["URL"]} has size {image["Size"]}. It cannot exceed 8.'
            foundImage = FindImage(image['URL'], f'image{index}')
            if image['Positioned'] == 'True':
                context[f'Image{index}'] = InlineImage(tpl, foundImage, width = Inches(image["Size"]))
            else:
                context['InlineImages'].append(InlineImage(tpl, foundImage, width = Inches(image["Size"])))

            imagesToRemove.append(f'image{index}.png')
            index += 1
        context.pop('Images')

    # Validates the context- and template-variables
    errMsg, valid = ValidateVariables(templatePath, context)
    if valid == False:
        if isTest == False: os.remove(templatePath)
        if len(imagesToRemove) > 0:
            for image in imagesToRemove: os.remove(image)
        if isTest == True: print(errMsg)
        return errMsg

    # Inserts data from the context-dictionary to the template
    try:
        tpl.render(context)
    except Exception:
        errMsg = 'One, or more, URLs are causing errors.'
        if isTest == False: os.remove(templatePath)
        if len(imagesToRemove) > 0:
            for image in imagesToRemove: os.remove(image)
        if isTest == True: print(errMsg)
        return errMsg
    
    # Saves and converts to PDF
    tpl.save(f'{pdfName}.docx')
    if len(imagesToRemove) > 0:
        for image in imagesToRemove: os.remove(image)
    # Returns final PDF
    return ConvertDocxToPDF(pdfName, templatePath, isTest)
    
def ConvertDocxToPDF(path: str, templatePath: str, isTest: bool):
    convert(f'{path}.docx', f'{path}.pdf')
    os.remove(f'{path}.docx')
    if isTest == False: os.remove(templatePath)

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
        # All variables in the template must start with "{{"
        # We can therefore identify the variables, by searching the document for these
        if p.text.__contains__('{{') and not (p.text.__contains__('{% for') or p.text.__contains__('{% endfor')):
            tempValues = p.text.rsplit('{{')

            for temp in tempValues:
                if not temp.__contains__('}}'):
                    tempValues.remove(temp)

            # Isolates the template-variables, so only the text part is stored
            foundValues = []
            for i in range(len(tempValues)):
                tempValue = tempValues[i].split('}}')[0]
                foundValues.append(tempValue)

            for value in foundValues:
                if not values.__contains__(value):
                    values.append(value)

    # Ignores lists, since the are allowed to be empty
    for key in context:
        if not isinstance(context[key], list) and not isinstance(context[key], dict): keysNotContained.append(key)
    
    for value in values:
        valuesNotInputted.append(value)
    
    for value in values:
        for key in context:
            if value == key:
                keysContained.append(key)
                keysNotContained.remove(key)

                valuesInputted.append(value)
                valuesNotInputted.remove(value)
    
    # Builds the exception string, so it can be returned to the user
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
    path = open(f'{fileName}.png','wb')
    path.write(data)
    path.close()

    return f'{fileName}.png'