## Unit tests skrevet af Magnus

# Used for unit testing
import unittest
from copy import deepcopy
from local import *
import pathlib as pl
import json


pdfName = 'Invoice'
testTemplatePath = 'Api/HC Andersen Flyttefirma Template.docx'
with open('Api/contextHC.json') as jsonString:
    contextDict: dict = json.load(jsonString)

unrecognizedURL = {
    "URL" : "",
    "Size" : 4,
    "Positioned" : "False"
}


class TestInsertDynamicData(unittest.TestCase):
    ## ------------------------------- Errors -------------------------------- ##
    def test_contextTooSmall(self):
        testContext = deepcopy(contextDict)

        testContext.pop('Name')

        with self.assertRaises(Exception):
            InsertDynamicData(testTemplatePath, testContext, pdfName, True)
    
    def test_URLError(self):
        testContext = deepcopy(contextDict)

        testContext['Images'].append(unrecognizedURL)

        with self.assertRaises(Exception):
            InsertDynamicData(testTemplatePath, testContext, pdfName, True)
    
    def test_ImageTooWide(self):
        testContext = deepcopy(contextDict)
        
        testContext['Images'][0]['Width'] = 171

        with self.assertRaises(Exception):
            InsertDynamicData(testTemplatePath, testContext, pdfName, True)
    
    def test_ImageTooTall(self):
        testContext = deepcopy(contextDict)
        
        testContext['Images'][0]['Height'] = 126

        with self.assertRaises(Exception):
            InsertDynamicData(testTemplatePath, testContext, pdfName, True)
    
    def test_isImagesRemoved(self):
        testContext = deepcopy(contextDict)
        imageCount = len(testContext['Images'])

        InsertDynamicData(testTemplatePath, testContext, pdfName, True)

        for i in range(imageCount):
            path = pl.Path(f'image{i}.png')
            self.assertEqual((str(path), path.is_file()), (str(path), False))

    def test_contextTooLarge(self):
        testContext = deepcopy(contextDict)

        testContext['test1'] = 1

        with self.assertRaises(Exception):
            InsertDynamicData(testTemplatePath, testContext, pdfName, True)
    
    ## ------------------------------ Successes ------------------------------ ##
    def test_success(self):
        self.assertTrue(InsertDynamicData(testTemplatePath, contextDict, pdfName, True))

if __name__ == '__main__':
    unittest.main()