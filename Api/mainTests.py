# Used for unit testing
import unittest
from copy import deepcopy
from main import *

contextDict = {
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

testImageURL = [
    "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.photographylife.com%2Fwp-content%2Fuploads%2F2014%2F09%2FNikon-D750-Image-Samples-2.jpg&f=1&nofb=1&ipt=a2eaec1c0ec1a1d4e001ca18ea6b952c9961567ffab5dea6ad90da52901064ca&ipo=images/",
    "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.pixelstalk.net%2Fwp-content%2Fuploads%2F2016%2F07%2F3840x2160-Images-Free-Download.jpg&f=1&nofb=1&ipt=a03ad8f692ef649662d67e3dc842a81bddcd57e2779920b188eddbc435114c4e&ipo=images",
    "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Funiversemagazine.com%2Fwp-content%2Fuploads%2F2022%2F08%2Fzm4nfgq29yi91-1536x1536-1.jpg&f=1&nofb=1&ipt=3442c84f5326c536eb005071ed537fdbdb6fbb81e0926a9e1567a2e81cf54f9c&ipo=images"
]

testTemplatePath = 'Api/HC Andersen Flyttefirma Template.docx'
testTemplatePathWithImg = 'Api/HC Andersen Flyttefirma Template (With Images).docx'

def test_InsertDynamicData(
        templateFile: str,
        contextFile: dict,
        imageURLFile: list = None,
        imagesSize: int = 5,
        pdfName: str = "Invoice",
    ):
    # Extracts the context-dictionary from .json file
    context: dict = contextFile
    imageURLs: list = imageURLFile

    # Save a copy pf the uploaded template file
    tpl = DocxTemplate(templateFile)
    
    if imageURLs != None:
        index = 0
        images = []
        for url in imageURLs:
            image = FindImage(url, f'image{index}')
            
            foundImage = InlineImage(tpl, image, width = Inches(imagesSize))
            
            images.append(image)
            context[f'image{index}'] = foundImage
            
            index += 1
    
    context = InsertPageNumbers(context, templateFile)
    
    errMsg, valid = ValidateVariables(templateFile, context)
    if valid == False:
        if imageURLs != None: RemoveRenderedImages(images)
        return errMsg

    # Inserts data from the context-dictionary to the template
    tpl.render(context)
    
    tpl.save(f'{pdfName}.docx')

    if imageURLs != None: RemoveRenderedImages(images)
    return ConvertDocxToPDF(pdfName, templateFile)

class TestInsertDynamicData(unittest.TestCase):
    def test_contextTooLargeWithImg(self):
        testContext = deepcopy(contextDict)
        expectedErrMsg = 'test1 was not found in template. '

        testContext['test1'] = 1
        self.assertEqual(test_InsertDynamicData(testTemplatePathWithImg, testContext, testImageURL), expectedErrMsg)
    
    def test_contextTooLarge(self):
        testContext = deepcopy(contextDict)
        expectedErrMsg = 'test1 was not found in template. '

        testContext['test1'] = 1
        self.assertEqual(test_InsertDynamicData(testTemplatePath, testContext), expectedErrMsg)
    
    def test_contextTooSmallWithImg(self):
        testContext = deepcopy(contextDict)
        expectedErrMsg = 'Name was not found in context. '

        testContext.pop('Name')
        self.assertEqual(test_InsertDynamicData(testTemplatePathWithImg, testContext, testImageURL), expectedErrMsg)

    def test_contextTooSmall(self):
        testContext = deepcopy(contextDict)
        expectedErrMsg = 'Name was not found in context. '

        testContext.pop('Name')
        self.assertEqual(test_InsertDynamicData(testTemplatePath, testContext), expectedErrMsg)
    
    def test_successWithImg(self):
        self.assertTrue(test_InsertDynamicData(testTemplatePathWithImg, contextDict, testImageURL))
    
    def test_success(self):
        self.assertTrue(test_InsertDynamicData(testTemplatePath, contextDict))
    
if __name__ == '__main__':
    unittest.main()