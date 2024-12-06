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
    "Total_Price" : 0,
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
            "units" : 1,
            "priceUnit" : 9999.95,
            "priceTotal" : 0
        },
        {
            "type" : "Fast pris for nedpakning",
            "units" : 1,
            "priceUnit" : 249.95,
            "priceTotal" : 0
        },
        {
            "type" : "Fast pris for opbevaring",
            "units" : 1,
            "priceUnit" : 349.95,
            "priceTotal" : 0
        },
        {
            "type" : "Pris for udlejning af udstyr",
            "units" : 8,
            "priceUnit" : 199.95,
            "priceTotal" : 0
        },
        {
            "type" : "Tungløft",
            "units" : 7,
            "priceUnit" : 99.95,
            "priceTotal" : 0
        }
    ]
}

testTemplatePath = 'Api/HC Andersen Flyttefirma Template.docx'
testPDFName = 'HC Andersen Flyttefirma Invoice'

def test_InsertDynamicData(
        templateFile: str,
        pdfName: str,
        contextFile: dict,
    ):
    context = contextFile

    templatePath = 'uploadedTemplate.docx'
    tpl = DocxTemplate(templateFile)
    
    context = InitializeContext(context)
    
    errMsg, valid = ValidateVariables(templatePath, context)
    if valid == False:
        return ValueError, errMsg

    # Inserts data from the context-dictionary to the template
    tpl.render(context)
    
    tpl.save(f'{pdfName}.docx')
    InsertPageNumbers(f'{pdfName}.docx')
    return ConvertDocxToPDF(pdfName)

class TestInsertDynamicData(unittest.TestCase):
    def test_contextTooLarge(self):
        testContext = deepcopy(contextDict)
        expectedErrMsg = ValueError, 'test1 was not found in template. '

        testContext['test1'] = 1
        self.assertEqual(test_InsertDynamicData(testTemplatePath, testPDFName, testContext), expectedErrMsg)
    
    def test_contextTooSmall(self):
        testContext = deepcopy(contextDict)
        expectedErrMsg = ValueError, 'Name was not found in context. '

        testContext.pop('Name')
        self.assertEqual(test_InsertDynamicData(testTemplatePath, testPDFName, testContext), expectedErrMsg)
    
    def test_success(self):
        self.assertTrue(test_InsertDynamicData(testTemplatePath, testPDFName, contextDict))
    
if __name__ == '__main__':
    unittest.main()