# Brugt til API kald
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

# Brugt til i konversionen af nødvændig data, ved konvertering fra .json til given datatype
import json
import shutil
from local import *

## ------------------------------------------ Skrevet af Bjørn ---------------------------------------- ##
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
## --------------------------------------------------------------------------------------------------- ##

## --------------------------------------- Skrevet af Magnus og Bjørn -------------------------------- ##
@app.post('/insert-dynamic-data/')
async def insert_dynamic_data(
        templateFile: UploadFile = File(...),
        contextFile: UploadFile = File(...),
        pdfName: str = Form("Invoice"),
    ):
    ## -------------------------------------- Skrevet af Magnus -------------------------------------- ##
    # Ekstrahere context-dictionary og imageURLs-liste fra .json filer
    context: dict = json.loads(contextFile.file.read())
    ## ----------------------------------------------------------------------------------------------- ##

    ## --------------------------------------- Skrevet af Bjørn -------------------------------------- ##
    # Gemmer kopi af uploadede skabelon fil
    templatePath = 'uploadedTemplate.docx'
    with open(templatePath, "wb") as buffer:
        shutil.copyfileobj(templateFile.file, buffer)
    ## ----------------------------------------------------------------------------------------------- ##
    
    ## -------------------------------------- Skrevet af Magnus -------------------------------------- ##
    return InsertDynamicData(templatePath, context, pdfName)
## --------------------------------------------------------------------------------------------------- ##

## ----------------------------------------- Skrevet af Bjørn ---------------------------------------- ##
if __name__ == '__main__':
    uvicorn.run(app, host = '127.0.0.1', port = 8000)
## --------------------------------------------------------------------------------------------------- ##