# pip install 'fastapi[standard]'
# pip install docxtpl
# pip install docx2pdf
# pip install python-docx

# Used for API calls
from fastapi import FastAPI, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# Used for inserting data in template
from docxtpl import DocxTemplate
from datetime import datetime
from docx import Document

# Used in ConvertDocxToPDF()
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
async def inser_dynamic_data(
        inputPath: str = Form(...),
        outputPath: str = Form(...),
        context: dict[str, str] = Form(...),
        useTotals: bool = Form(...),
    ):
    tpl = DocxTemplate(f'docxtpl/{inputPath}.docx')
    if useTotals == True: context = InsertTotalPrices(context)
    
    errMsg, variablesValid = CheckVariablesValid(inputPath, context)
    if variablesValid == False:
        return print(errMsg)

    tpl.render(context)
    
    tpl.save(f'{outputPath}.docx')
    return ConvertDocxToPDF(outputPath)

def ConvertDocxToPDF(path: str):
    convert(f'{path}.docx', f'{path}.pdf')
    os.remove(f'{path}.docx')

    return FileResponse(f'{path}.pdf', media_type = 'application/pdf', filename = path)

def CheckVariablesValid(path: str, context: dict):
    doc = Document(f'docxtpl/{path}.docx')
    valid = True

    keysContained = []
    keysNotContained = []
    values = []
    valuesNotInputted = []
    valuesInputted = []
    for p in doc.paragraphs:
        if p.text.__contains__('{{'):
            tempValues = []
            tempValues.append(p.text.rsplit('{{')[1])
            for value in tempValues:
                values.append(value.split('}}')[0])

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
    
    exception = 'ContextVariablesError:\n'
    if not len(keysNotContained) == 0:
        for key in keysNotContained:
            exception += f'{key} was not found in template\n'
        valid = False
    
    if not len(valuesNotInputted) == 0:
        for value in valuesNotInputted:
            exception += f'{value} was not found in context\n'
        valid = False
    
    return exception, valid

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

# ------------------------------------------------------------------------------------------- #


# Test method (Can't get Postman to accept dictionaries for some reason)
def InserDynamicData(
        inputPath: str,
        outputPath: str,
        context: dict[str, str],
        useTotals: bool,
    ):
    tpl = DocxTemplate(f'docxtpl/{inputPath}.docx')
    if useTotals == True: context = InsertTotalPrices(context)
    
    errMsg, variablesValid = CheckVariablesValid(inputPath, context)
    if variablesValid == False:
        return print(errMsg)

    tpl.render(context)
    
    tpl.save(f'{outputPath}.docx')
    ConvertDocxToPDF(outputPath)


# ------------------------------------------------------------------------------------------- #


# Example of how the context dictionary could look like:
context = {
    # Variables
    'Name' : 'Magnus Næhr',
    'Adress' : 'Mølletoften 1',
    'City_postcode' : 'Lyngby, 2800',
    'Customer_Number' : 123456,
    'Order_Number' : 123456,
    'Current_Date' : datetime.today().strftime("%d-%m-%Y"),
    'Offer_Name' : 'Dette er tilbudet',
    'Date_of_Execution' : '13-12-2024',
    'Floor_Elevator' : '2. etage, m. elevator.',
    'Square_Meters' : 28,
    'Parking' : 'Perkeringsplads ude foran bolig.',
    'Time_Estimation' : '2 timer.',
    'Task_Description' : 'Dette er opgave beskrivelsen.',
    'Second_Adresses' : 'Dette er en sekundær addresse.',
    'Comments' : 'Dette er en kommentar.',
    'Agreed_Date' : '13-12-2024',
    'Start_Time' : '10:30 - 11:30',
    'Agreed_Date_Equipment' : '14-12-2024',
    'Start_Time_Equipment' : '11:00 - 12:00',
    'Customer_Phone' : '12345678',
    'Total_Price' : 0,
    'Reg_Number' : 123456,
    'Account_Number' : 123456,
    'Order_Id' : 123456,
    'Details' : 'Dette er en detalje.',

    # Tables
    'itemsTable' : [
        {
            'type' : 'Fast pris for flytning',
            'units' : 1,
            'priceUnit' : 9999.95,
            'priceTotal' : 0
        },
        {
            'type' : 'Fast pris for nedpakning',
            'units' : 1,
            'priceUnit' : 249.95,
            'priceTotal' : 0
        },
        {
            'type' : 'Fast pris for opbevaring',
            'units' : 1,
            'priceUnit' : 349.95,
            'priceTotal' : 0
        },
        {
            'type' : 'Pris for udlejning af udstyr',
            'units' : 8,
            'priceUnit' : 199.95,
            'priceTotal' : 0
        },
        {
            'type' : 'Tungløft',
            'units' : 7,
            'priceUnit' : 99.95,
            'priceTotal' : 0
        },
    ]
}


# ------------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    usingPostman = 0

    if usingPostman == 1:
        import uvicorn
        uvicorn.run(app, host = '127.0.0.1', port = 8000)
    else:
        InserDynamicData('HC Andersen Flyttefirma Template', 'HC Andersen Flyttefirma Invoice', context, True)