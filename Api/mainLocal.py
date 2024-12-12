# Brugt til at indsætte dynamiske data i word skabelon
from docxtpl import DocxTemplate, InlineImage
from docx import Document
from docx.shared import Inches

# Brugt til at konvertere fra docx-format til pdf-format
import os
from docx2pdf import convert
from main import *

# Brugt til at finde et givent billede, fra URL
import requests

def InsertDynamicData(
        templateStr: str,
        context: dict,
        pdfName: str = "Invoice",
    ):
    # Gemmer kopi af uploadede skabelon fil
    templatePath = 'uploadedTemplate.docx'
    Document(templateStr).save(templatePath)
    
    # Finder og åbner den kopierede skabelon som DocxTemplate objekt
    tpl = DocxTemplate(templatePath)
    
    # Finder givene billeder fra URL, og ligger den i context-dictionary
    index = 0
    imagesToRemove = []
    if context['Images'] != None:
        context["InlineImages"] = []
        for url in context['Images']:
            image = FindImage(url, f'image{index}')
            context['InlineImages'].append(InlineImage(tpl, image, width = Inches(context['Images'][url])))

            imagesToRemove.append(f'image{index}.png')
            index += 1

    # Validere context- og skabelon-variabler
    errMsg, valid = ValidateVariables(templatePath, context)
    if valid == False:
        os.remove(templatePath)
        if context['Images'] != None:
            for image in imagesToRemove: os.remove(image)
        print(errMsg)
        return errMsg

    # Indsætter data fra context-dictionary til skabelon
    tpl.render(context)
    
    # Gemmer og konvertere til PDF
    tpl.save(f'{pdfName}.docx')
    if context['Images'] != None:
        for image in imagesToRemove: os.remove(image)
    return ConvertDocxToPDF(pdfName, templatePath)

## --------------------------------- Data --------------------------------- ##

templateStr = 'API/HC Andersen Flyttefirma Template.docx'
context = {
    "Name" : "Magnus Næhr",
    "Adress" : "Mølletoften 1",
    "City_postcode" : "Lyngby, 2800",
    "Customer_Number" : 123456,
    "Order_Number" : 123456,
    "Current_Date" : "05-12-2024",
    "Invoice_Type" : "Ordrebekræftelse",
    "Offer_Name" : "Dette er tilbudet",
    "Date_of_Execution" : "13-12-2024",
    "Floor_Elevator" : "2. etage, m. elevator.",
    "Square_Meters" : 28,
    "Parking" : "Perkeringsplads ude foran bolig.",
    "Time_Estimation" : "2 timer.",
    "Task_Description" : "Dette er opgave beskrivelsen.",
    "Second_Adresses" : [
        "Dette er en sekundær addresse.",
        "Dette er også en sekundær adresse."
    ],
    "Comments" : [
        "Dette er en kommentar",
        "Dette er også en kommentar"
    ],
    "Agreed_Date" : "13-12-2024",
    "Start_Time" : "10:30 - 11:30",
    "Agreed_Date_Equipment" : "14-12-2024",
    "Start_Time_Equipment" : "11:00 - 12:00",
    "Customer_Phone" : "12345678",
    "Total_Price" : 16123.9,
    "Reg_Number" : 123456,
    "Account_Number" : 123456,
    "Order_Id" : 123456,
    "Details" : [
        "Dette er en detalje.",
        "Dette er også en detalje"
    ],
    "Images" : {
        "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.photographylife.com%2Fwp-content%2Fuploads%2F2014%2F09%2FNikon-D750-Image-Samples-2.jpg&f=1&nofb=1&ipt=a2eaec1c0ec1a1d4e001ca18ea6b952c9961567ffab5dea6ad90da52901064ca&ipo=images/" : 6,
        "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.pixelstalk.net%2Fwp-content%2Fuploads%2F2016%2F07%2F3840x2160-Images-Free-Download.jpg&f=1&nofb=1&ipt=a03ad8f692ef649662d67e3dc842a81bddcd57e2779920b188eddbc435114c4e&ipo=images" : 6,
        "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Funiversemagazine.com%2Fwp-content%2Fuploads%2F2022%2F08%2Fzm4nfgq29yi91-1536x1536-1.jpg&f=1&nofb=1&ipt=3442c84f5326c536eb005071ed537fdbdb6fbb81e0926a9e1567a2e81cf54f9c&ipo=images" : 6
    },
    "itemsTable" : [
        {
            "type" : "Fast pris for flytning",
            "units" : "",
            "priceUnit" : 9999.95,
            "priceTotal" : 9999.95
        },
        {
            "type" : "Fast pris for nedpakning",
            "units" : "",
            "priceUnit" : 249.95,
            "priceTotal" : 249.95
        },
        {
            "type" : "Fast pris for opbevaring",
            "units" : "",
            "priceUnit" : 349.95,
            "priceTotal" : 349.95
        },
        {
            "type" : "Pris for udlejning af udstyr",
            "units" : 8,
            "priceUnit" : 199.95,
            "priceTotal" : 159960
        },
        {
            "type" : "Tungløft",
            "units" : 7,
            "priceUnit" : 99.95,
            "priceTotal" : 699.65
        },
        {
            "type" : "Pris i alt eks. moms",
            "units" : "",
            "priceUnit" : "",
            "priceTotal" : 12899.1
        },
        {
            "type" : "Pris i alt inkl. moms",
            "units" : "",
            "priceUnit" : "",
            "priceTotal" : 16123.9
        }
    ]
}

## ------------------------------------------------------------------------ ##

if __name__ == '__main__':
    InsertDynamicData(templateStr, context)