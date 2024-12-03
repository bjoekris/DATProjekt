# pip install 'fastapi[standard]'
# pip install docxtpl
# pip install docx2pdf

# Used for API calls
from fastapi import FastAPI, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# Used for inserting data in template
from docxtpl import DocxTemplate
from datetime import datetime

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

        contextKeys: list[str] = Form(...),
        contextValues: list[str] = Form(...),

        tables: list = Form(...)
    ):
    context = {}
    for key in contextKeys:
        for value in contextValues:
            context[key] = value
            print(f'Key: {key}, Value: {context[key]}')

    tpl = DocxTemplate(f'{inputPath}.docx')

    tpl.render(context)
    tpl.render({'{{Current Date}}' : datetime.today.strftime("%d-%m-%Y")})
    for table in tables: tpl.render(tables[table])

    tpl.save(f'{outputPath}.docx')
    ConvertDocxToPDF(outputPath)

def ConvertDocxToPDF(path):
    convert(f'{path}.docx', f'{path}.pdf')
    os.remove(f'{path}.docx')

    return FileResponse(f'{path}.pdf', media_type = 'application/pdf', filename = path)


# ------------------------------------------------------------------------------------------- #


def InserDynamicData(
        inputPath: str,
        outputPath: str,

        context: dict[str, str],
        tables: dict[dict[str, list[int, float]]]
    ):
    tpl = DocxTemplate(f'docxtpl/{inputPath}.docx')

    tpl.render(context)
    tpl.render({'{{Current Date}}' : datetime.today().strftime("%d-%m-%Y")})
    for table in tables: tpl.render(tables[table])

    tpl.save(f'{outputPath}.pdf')


# ------------------------------------------------------------------------------------------- #


# Example of how the context dictionary could look like:
context = {
    '{{Name}}' : 'Magnus Næhr',
    '{{Adress}}' : 'Mølletoften 1',
    '{{City_postcode}}' : 'Lyngby, 2800',
}

# Example for how a table could look like in the table dictionary:
priceTabel = {
    'listEntries' : [
        { 'Fast pris for flytning' : [1, 9999.95] },
        { 'Fast pris for nedpakning' : [1, 249.95] },
        { 'Fast pris for opbevaring' : [1, 349.95] },
        { 'Pris for udlejning af udstyr' : [8, 199.95] },
        { 'Tungløft' : [7, 99.95] }
    ]
}


# ------------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    usingPostman = 0

    if usingPostman == 1:
        import uvicorn
        uvicorn.run(app, host = '127.0.0.1', port = 8000)
    else:
        InserDynamicData('HC Andersen Flyttefirma Template', 'HC Andersen Flyttefirma Invoice', context, priceTabel)