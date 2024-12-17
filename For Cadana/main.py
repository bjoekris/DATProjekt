# Used for API
from fastapi import FastAPI, Form, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

# Used for converting necessarry data from .json to given datatype
import json
import shutil
from local import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Loggin setup
logging.basicConfig(level=logging.INFO)


# API keys for validation
API_KEYS = {
    'user1': 'abc123456789',
    'user2': 'def987654321',
}

# Function to validate API key
def validate_api_key(api_key: str) -> bool:
    return api_key in API_KEYS.values()


@app.post('/insert-dynamic-data/')
async def insert_dynamic_data(
        templateFile: UploadFile = File(...),
        contextFile: UploadFile = File(...),
        pdfName: str = Form("Invoice"),
        x_api_key: str = Header(None),
    ):
    logging.info('Received request to /insert-dynamic-data/')

     # Validate API key
    if not x_api_key or not validate_api_key(x_api_key):
        raise HTTPException(status_code = 401, detail = 'Unauthorized: Invalid API Key')

    logging.info('API Key validated.')
    
    # Extracts the context-dictionary from the .json file
    context: dict = json.loads(contextFile.file.read())

    # Saves a copy of the uploaded template file
    templatePath = 'uploadedTemplate.docx'
    with open(templatePath, "wb") as buffer:
        shutil.copyfileobj(templateFile.file, buffer)
    
    try:
        return InsertDynamicData(templatePath, context, pdfName)
    except Exception as e:
        logging.info(f'InsertDynamicData returned {e}')
        return e

if __name__ == '__main__':
    uvicorn.run(app, host = '127.0.0.1', port = 8000)