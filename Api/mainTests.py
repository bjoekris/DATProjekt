## Unit tests skrevet af Magnus

# Used for unit testing
import unittest
from copy import deepcopy
from local import *
import pathlib as pl
import json


pdfName = 'Invoice'
testTemplatePath = 'Api/HC Andersen Flyttefirma Template.docx'
with open('Api/context.json') as jsonString:
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
    
    def test_ImageTooBig(self):
        testContext = deepcopy(contextDict)
        
        testContext['Images'][0]['Size'] = 8

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
        pass
        testContext = deepcopy(contextDict)

        self.assertTrue(InsertDynamicData(testTemplatePath, testContext, pdfName, True))

#if __name__ == '__main__':
 #   unittest.main()