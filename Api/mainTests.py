## Unit tests skrevet af Magnus

# Used for unit testing
import unittest
from local import InsertDynamicData, RemoveTempFiles
import os
import json
import shutil


pdfName = 'Invoice'
testOrigTemplatePath = 'Api/HC Andersen Flyttefirma Template.docx'
testTemplatePath = 'uploadedTemplate.docx'
with open('Api/contextHC.json') as jsonString:
    context: dict = json.load(jsonString)

wideImg = {
    'URL' : 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimages.pexels.com%2Fphotos%2F459225%2Fpexels-photo-459225.jpeg%3Fcs%3Dsrgb%26dl%3Ddaylight-environment-forest-459225.jpg%26fm%3Djpg&f=1&nofb=1&ipt=d2e4c67f2b922b62ea81f2eb0111d11879c10e53e46d82997368b3fcc1226861&ipo=images',
    'Size' : 0,
    'Width' : 0,
    'Height' : 0,
    'Positioned' : 'False',
    'List' : 10
}

tallImg = {
    'URL' : 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimages.unsplash.com%2Fphoto-1590523278191-995cbcda646b%3Fixlib%3Drb-1.2.1%26q%3D80%26fm%3Djpg%26crop%3Dentropy%26cs%3Dtinysrgb%26w%3D1080%26fit%3Dmax%26ixid%3DeyJhcHBfaWQiOjEyMDd9&f=1&nofb=1&ipt=01e583a14a5979f9009874d56d276aa56e15ee63b2cb84b9e18a610455048f99&ipo=images',
    'Size' : 0,
    'Width' : 0,
    'Height' : 0,
    'Positioned' : 'False',
    'List' : 10
}


class TestInsertDynamicData(unittest.TestCase):
    ## ------------------------------- Error Cases -------------------------------- ##
    
    def test_contextTooSmall(self):
        print('contextTooSmall')
        shutil.copyfile(testOrigTemplatePath, testTemplatePath)
        testContext = json.loads(json.dumps(context))

        imageCount = len(testContext['Images'])
        expectedErrMsg = 'Name was not found in context. '

        testContext.pop('Name')

        with self.assertRaises(ValueError) as cm:
            InsertDynamicData(testTemplatePath, testContext, pdfName)
        
        RemoveTempFiles(testTemplatePath, pdfName)
        
        errMsg = cm.exception.args[0]
        self.assertEqual(errMsg, expectedErrMsg)
        self.assertTrue(GeneralTests.isTempFilesRemoved(imageCount))
    
    def test_contextTooLarge(self):
        print('contextTooLarge')
        shutil.copyfile(testOrigTemplatePath, testTemplatePath)
        testContext = json.loads(json.dumps(context))

        imageCount = len(testContext['Images'])
        expectedErrMsg = 'test1 was not found in template. '

        testContext['test1'] = 1

        with self.assertRaises(ValueError) as cm:
            InsertDynamicData(testTemplatePath, testContext, pdfName)
            
        RemoveTempFiles(testTemplatePath, pdfName)
        
        errMsg = cm.exception.args[0]
        self.assertEqual(errMsg, expectedErrMsg)
        self.assertTrue(GeneralTests.isTempFilesRemoved(imageCount))
    
    def test_widthImageTooWide(self):
        print('widthImageTooWide')
        shutil.copyfile(testOrigTemplatePath, testTemplatePath)
        testContext = json.loads(json.dumps(context))

        testContext['Images'].append(wideImg)

        imageCount = len(testContext['Images'])
        expectedErrMsg = f'{testContext["Images"][-1]["URL"]} with Width: 171, at position: {imageCount} has exceeded the maximum width og 170.'
        
        testContext['Images'][-1]['Size'] = 0
        testContext['Images'][-1]['Width'] = 171
        testContext['Images'][-1]['Height'] = 0

        with self.assertRaises(ValueError) as cm:
            InsertDynamicData(testTemplatePath, testContext, pdfName)
            
        RemoveTempFiles(testTemplatePath, pdfName)
        
        errMsg = cm.exception.args[0]
        self.assertEqual(errMsg, expectedErrMsg)
        self.assertTrue(GeneralTests.isTempFilesRemoved(imageCount))
    
    def test_heightImageTooWide(self):
        print('heightImageTooWide')
        shutil.copyfile(testOrigTemplatePath, testTemplatePath)
        testContext = json.loads(json.dumps(context))

        testContext['Images'].append(wideImg)

        imageCount = len(testContext['Images'])
        width = 263.3426966292135
        expectedErrMsg = f'{testContext["Images"][-1]["URL"]} with Width: {width}, at position: {imageCount} has exceeded the maximum width og 170.'
        
        testContext['Images'][-1]['Size'] = 0
        testContext['Images'][-1]['Width'] = 0
        testContext['Images'][-1]['Height'] = 125

        with self.assertRaises(ValueError) as cm:
            InsertDynamicData(testTemplatePath, testContext, pdfName)
            
        RemoveTempFiles(testTemplatePath, pdfName)
        
        errMsg = cm.exception.args[0]
        self.assertEqual(errMsg, expectedErrMsg)
        self.assertTrue(GeneralTests.isTempFilesRemoved(imageCount))
    
    def test_widthImageTooTall(self):
        print('widthImageTooTall')
        shutil.copyfile(testOrigTemplatePath, testTemplatePath)
        testContext = json.loads(json.dumps(context))

        testContext['Images'].append(tallImg)

        imageCount = len(testContext['Images'])
        height = 226.66666666666666
        expectedErrMsg = f'{testContext["Images"][-1]["URL"]} with Height: {height}, at position: {imageCount} has exceeded the maximum height og 125.'
        
        testContext['Images'][-1]['Size'] = 0
        testContext['Images'][-1]['Width'] = 170
        testContext['Images'][-1]['Height'] = 0

        with self.assertRaises(ValueError) as cm:
            InsertDynamicData(testTemplatePath, testContext, pdfName)
            
        RemoveTempFiles(testTemplatePath, pdfName)
        
        errMsg = cm.exception.args[0]
        self.assertEqual(errMsg, expectedErrMsg)
        self.assertTrue(GeneralTests.isTempFilesRemoved(imageCount))
    
    def test_heightImageTooTall(self):
        print('heightImageTooTall')
        shutil.copyfile(testOrigTemplatePath, testTemplatePath)
        testContext = json.loads(json.dumps(context))

        testContext['Images'].append(tallImg)
        
        imageCount = len(testContext['Images'])
        expectedErrMsg = f'{testContext["Images"][-1]["URL"]} with Height: 126, at position: {imageCount} has exceeded the maximum height og 125.'
        
        testContext['Images'][-1]['Size'] = 0
        testContext['Images'][-1]['Width'] = 0
        testContext['Images'][-1]['Height'] = 126

        with self.assertRaises(ValueError) as cm:
            InsertDynamicData(testTemplatePath, testContext, pdfName)
            
        RemoveTempFiles(testTemplatePath, pdfName)
        
        errMsg = cm.exception.args[0]
        self.assertEqual(errMsg, expectedErrMsg)
        self.assertTrue(GeneralTests.isTempFilesRemoved(imageCount))
    
    def test_imageSizesAllZero(self):
        print('imageSizesAllZero')
        shutil.copyfile(testOrigTemplatePath, testTemplatePath)
        testContext = json.loads(json.dumps(context))
        
        imageCount = len(testContext['Images'])
        expectedErrMsg = f'{testContext["Images"][0]["URL"]} caused an error, at position: 1. At least one between "Size", "Width", and "Height" must be larger than 0.'

        testContext['Images'][0]['Size'] = 0
        testContext['Images'][0]['Width'] = 0
        testContext['Images'][0]['Height'] = 0

        with self.assertRaises(ValueError) as cm:
            InsertDynamicData(testTemplatePath, testContext, pdfName)
            
        RemoveTempFiles(testTemplatePath, pdfName)
        
        errMsg = cm.exception.args[0]
        self.assertEqual(errMsg, expectedErrMsg)
        self.assertTrue(GeneralTests.isTempFilesRemoved(imageCount))

    ## ------------------------------ Success Cases ------------------------------- ##
    
    def test_success(self):
        print('success')
        shutil.copyfile(testOrigTemplatePath, testTemplatePath)
        testContext = json.loads(json.dumps(context))
        
        imageCount = len(testContext['Images'])

        self.assertTrue(InsertDynamicData(testTemplatePath, testContext, pdfName))
        self.assertTrue(GeneralTests.isTempFilesRemoved(imageCount))


class GeneralTests:
    def isTempFilesRemoved(imageCount: int):
        for i in range(imageCount):
            if os.path.isfile(f'image{i}.png') == True:
                return False

        return not (os.path.isfile(f'{pdfName}.docx') or os.path.isfile(testTemplatePath))
            

if __name__ == '__main__':
    unittest.main()