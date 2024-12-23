# Brugt til API
from fastapi import FastAPI, Form, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

# Brugt til i konversionen af nødvændig data, ved konvertering fra .json til given datatype
import json
import shutil
from local import *

## ------------------------------------------ Skrevet af Bjørn --------------------------------------- ##
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

#Loggin setup
logging.basicConfig(level=logging.INFO)


# API nøgler til validering
API_KEYS = {
    'user1': 'abc123456789',
    'user2': 'def987654321',
}

# Funktion til at validere API nøgle
def validate_api_key(api_key: str) -> bool:
    return api_key in API_KEYS.values()
## --------------------------------------------------------------------------------------------------- ##

## --------------------------------------- Skrevet af Magnus og Bjørn -------------------------------- ##
@app.post('/insert-dynamic-data/')
async def insert_dynamic_data(
        templateFile: UploadFile = File(...),
        contextFile: UploadFile = File(...),
        pdfName: str = Form('Invoice'),
        x_api_key: str = Header(None),
    ):
    ## --------------------------------------- Skrevet af Bjørn -------------------------------------- ##
    logging.info('Received request to /insert-dynamic-data/')

     # Validate API key
    if not x_api_key or not validate_api_key(x_api_key):
        raise HTTPException(status_code = 401, detail = 'Unauthorized: Invalid API Key')

    logging.info('API Key validated.')
    ## ----------------------------------------------------------------------------------------------- ##

    ## -------------------------------------- Skrevet af Magnus -------------------------------------- ##
    # Ekstrahere context-dictionary fra .json filen
    context: dict = json.loads(contextFile.file.read())
    ## ----------------------------------------------------------------------------------------------- ##

    ## --------------------------------------- Skrevet af Bjørn -------------------------------------- ##
    # Gemmer kopi af uploadede skabelon fil
    templatePath = 'uploadedTemplate.docx'
    with open(templatePath, "wb") as buffer:
        shutil.copyfileobj(templateFile.file, buffer)
    ## ----------------------------------------------------------------------------------------------- ##
    
    ## -------------------------------------- Skrevet af Magnus -------------------------------------- ##
    try:
        return InsertDynamicData(templatePath, context, pdfName)
    except Exception as e:
        logging.info(f'InsertDynamicData returned: {e}')
        RemoveTempFiles(templatePath, pdfName)
        raise HTTPException(status_code = 500, detail = f'{e}')
## --------------------------------------------------------------------------------------------------- ##

## ----------------------------------------- Skrevet af Bjørn ---------------------------------------- ##
if __name__ == '__main__':
    uvicorn.run(app, host = '127.0.0.1', port = 8000)
## --------------------------------------------------------------------------------------------------- ##