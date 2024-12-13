# Used for API calls
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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


async def insert_dynamic_data(
        templateFile: UploadFile = File(...),
        contextFile: UploadFile = File(...),
        pdfName: str = Form("Invoice"),
    ):
    # Extracts the context-dictionary from the .json file
    context: dict = json.loads(contextFile.file.read())

    # Saves a copy of the uploaded template file
    templatePath = 'uploadedTemplate.docx'
    with open(templatePath, "wb") as buffer:
        shutil.copyfileobj(templateFile.file, buffer)
    
    return InsertDynamicData(templatePath, context, pdfName)

if __name__ == '__main__':
    uvicorn.run(app, host = '127.0.0.1', port = 8000)