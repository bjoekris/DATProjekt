## Unit tests skrevet af Magnus

# Used for unit testing
import unittest
from copy import deepcopy
from local import InsertDynamicData, RemoveTempFiles
import os
import json
import shutil


pdfName = 'Invoice'
testOrigTemplatePath = 'Api/HC Andersen Flyttefirma Template.docx'
testTemplatePath = 'uploadedTemplate.docx'
with open('Api/contextHC.json') as jsonString:
    contextDict: dict = json.load(jsonString)


class TestInsertDynamicData(unittest.TestCase):
    ## ------------------------------- Error Cases -------------------------------- ##
    
    def test_contextTooSmall(self):
        print('contextTooSmall')
        shutil.copyfile(testOrigTemplatePath, testTemplatePath)

        testContext = deepcopy(contextDict)
        expectedErrMsg = 'Name was not found in context. '

        testContext.pop('Name')
        imageCount = len(contextDict['Images'])

        with self.assertRaises(ValueError) as cm:
            InsertDynamicData(testTemplatePath, testContext, pdfName)
        
        RemoveTempFiles(testTemplatePath, pdfName)
        
        errMsg = cm.exception.args[0]
        self.assertEqual(errMsg, expectedErrMsg)
        self.assertTrue(GeneralTests.isImagesRemoved(imageCount))
    
    def test_contextTooLarge(self):
        print('contextTooLarge')
        shutil.copyfile(testOrigTemplatePath, testTemplatePath)
        
        testContext = deepcopy(contextDict)
        expectedErrMsg = 'test1 was not found in template. '

        testContext['test1'] = 1
        imageCount = len(contextDict['Images'])

        with self.assertRaises(ValueError) as cm:
            InsertDynamicData(testTemplatePath, testContext, pdfName)
            
        RemoveTempFiles(testTemplatePath, pdfName)
        
        errMsg = cm.exception.args[0]
        self.assertEqual(errMsg, expectedErrMsg)
        self.assertTrue(GeneralTests.isImagesRemoved(imageCount))
    
    def test_imageTooWide(self):
        print('imageTooWide')
        shutil.copyfile(testOrigTemplatePath, testTemplatePath)
        
        testContext = deepcopy(contextDict)
        expectedErrMsg = f'{testContext["Images"][0]["URL"]} Width has exceeded the maximum width og 170.'
        
        testContext['Images'][0]['Width'] = 171
        imageCount = len(contextDict['Images'])

        with self.assertRaises(ValueError) as cm:
            InsertDynamicData(testTemplatePath, testContext, pdfName)
            
        RemoveTempFiles(testTemplatePath, pdfName)
        
        errMsg = cm.exception.args[0]
        self.assertEqual(errMsg, expectedErrMsg)
        self.assertTrue(GeneralTests.isImagesRemoved(imageCount))
    
    def test_imageTooTall(self):
        print('imageTooTall')
        shutil.copyfile(testOrigTemplatePath, testTemplatePath)
        
        testContext = deepcopy(contextDict)
        expectedErrMsg = f'{testContext["Images"][0]["URL"]} Height has exceeded the maximum height og 125.'
        
        testContext['Images'][0]['Size'] = 0
        testContext['Images'][0]['Width'] = 0
        testContext['Images'][0]['Height'] = 126
        
        imageCount = len(contextDict['Images'])

        with self.assertRaises(ValueError) as cm:
            InsertDynamicData(testTemplatePath, testContext, pdfName)
            
        RemoveTempFiles(testTemplatePath, pdfName)
        
        errMsg = cm.exception.args[0]
        self.assertEqual(errMsg, expectedErrMsg)
        self.assertTrue(GeneralTests.isImagesRemoved(imageCount))
    
    def test_imageSizesAllZero(self):
        print('imageSizesAllZero')
        shutil.copyfile(testOrigTemplatePath, testTemplatePath)
        
        testContext = deepcopy(contextDict)
        expectedErrMsg = f'{testContext["Images"][0]["URL"]} Size, Width, and Height were 0, at least one must be larger than 0.'

        testContext['Images'][0]['Size'] = 0
        testContext['Images'][0]['Width'] = 0
        testContext['Images'][0]['Height'] = 0
        
        imageCount = len(contextDict['Images'])

        with self.assertRaises(ValueError) as cm:
            InsertDynamicData(testTemplatePath, testContext, pdfName)
            
        RemoveTempFiles(testTemplatePath, pdfName)
        
        errMsg = cm.exception.args[0]
        self.assertEqual(errMsg, expectedErrMsg)
        self.assertTrue(GeneralTests.isImagesRemoved(imageCount))

    ## ------------------------------ Success Cases ------------------------------- ##
    
    def test_success(self):
        print('success')
        shutil.copyfile(testOrigTemplatePath, testTemplatePath)
        
        imageCount = len(contextDict['Images'])

        self.assertTrue(InsertDynamicData(testTemplatePath, contextDict, pdfName))
        self.assertTrue(GeneralTests.isImagesRemoved(imageCount))
        self.assertTrue(GeneralTests.isTempDocxRemoved())

class GeneralTests:
    def isImagesRemoved(imageCount: int):
        print('isImageRemoved')
        
        for i in range(imageCount):
            if os.path.isfile(f'image{i}.png') == True:
                return False

        return True
    
    def isTempDocxRemoved():
        print('isTempDocxRemoved')

        return not os.path.isfile(f'{pdfName}.docx')
            

if __name__ == '__main__':
    unittest.main()