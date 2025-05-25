import csv
import glob
import os
import re
import yaml
from jinja2 import Template
from PIL import Image
from src.integrated_test.account.integrated_test_account import IntegratedTestAccount
from src.integrated_test.account.integrated_test_account_config import IntegratedTestAccountConfig
from src.integrated_test.integrated_test_batch import IntegratedTestBatch
from src.integrated_test.integrated_test_component import IntegratedTestComponent
from src.integrated_test.integrated_test_file import IntegratedTestFile
from src.integrated_test.case.integrated_test_case import IntegratedTestCase
from src.integrated_test.integrated_test_view import IntegratedTestView
from src.integrated_test.image.integrated_test_image import IntegratedTestImage
from src.integrated_test.matrix.integrated_test_matrix import IntegratedTestMatrix
from src.integrated_test.block.integrated_test_block import IntegratedTestBlock
from src.integrated_test.preparation.integrated_test_preparation import IntegratedTestPreparation
from src.integrated_test.perspective.integrated_test_perspective import IntegratedTestPerspective
from src.integrated_test.integrated_test import IntegratedTest

class IntegratedTestRepository():
    def find(self, type, name):
        blocks = self.getBlocks(f"./storage/integrated_test/{type}/{name}/テストケース.yml")

        matrices = []
        matrixPaths = sorted(glob.glob(f"./storage/integrated_test/{type}/{name}/マトリクス/*"))
        for matrixPath in matrixPaths:
            with open(matrixPath, 'r') as file:
                reader = csv.reader(file)
                data = [row for row in reader]
                matrices.append(IntegratedTestMatrix(os.path.splitext(os.path.basename(matrixPath))[0], data[0], data[1:]))

        images = []
        imagePaths = sorted(glob.glob(f"./storage/integrated_test/{type}/{name}/画面イメージ/*"))
        for imagePath in imagePaths:
            if os.path.isfile(imagePath):
                img = Image.open(imagePath)
                w, h = img.size
                images.append(IntegratedTestImage(imagePath, w, h))

        preparationPath = f"./storage/integrated_test/{type}/{name}/事前準備・注意点.yml"
        preparation = None
        if os.path.isfile(preparationPath):
            with open(preparationPath, 'r') as file:
                data = yaml.safe_load(file)
                preparation = IntegratedTestPreparation([] if data == None else data)

        testAccountPath = f"./storage/integrated_test/{type}/{name}/テストデータ.yml"
        testAccounts = []
        if os.path.isfile(testAccountPath):
            data = []
            with open(testAccountPath, 'r') as file:
                data = yaml.safe_load(file)
            for _, testAccountName in enumerate(data):
                testAccounts.append(IntegratedTestAccount(
                    testAccountName,
                    [IntegratedTestAccountConfig(value, data[testAccountName][value]) for key, value in enumerate(data[testAccountName])]
                ))

        if type == 'component':
            return IntegratedTestComponent(name, blocks, matrices, images, preparation, testAccounts)
        elif type == 'batch':
            return IntegratedTestBatch(name, blocks, matrices, images, preparation, testAccounts)
        elif type == 'file':
            return IntegratedTestFile(name, blocks, matrices, images, preparation, testAccounts)
        elif type == 'view':
            return IntegratedTestView(name, blocks, matrices, images, preparation, testAccounts)

    def get(self) -> list:
        testBatchs = []
        testComponents = []
        testFiles = []
        testViews = []
        types = ['batch', 'component', 'file', 'view']
        for type in types:
            paths = glob.glob(fr"./storage/integrated_test/{type}/*/")
            for path in paths:
                result = re.match(fr"./storage/integrated_test/{type}/(.+)/", path)
                name = result.group(1)
                if type == 'batch':
                    testBatchs.append(self.find(type, name))
                elif type == 'component':
                    testComponents.append(self.find(type, name))
                elif type == 'file':
                    testFiles.append(self.find(type, name))
                elif type == 'view':
                    testViews.append(self.find(type, name))

        return IntegratedTest(testBatchs, testComponents, testFiles, testViews)

    def getBlocks(self, path) -> list:
        output = ''
        with open(path, 'r') as file:
            template = Template(file.read())
            output = template.render()

        data = yaml.safe_load(output)

        blocks = []
        for _, blockName in enumerate(data):
            perspectives = []
            for _, perspectiveName in enumerate(data[blockName]):
                cases = []
                for _, case in enumerate(data[blockName][perspectiveName]):
                    cases.append(IntegratedTestCase(
                        case['パターン'] if 'パターン' in case else '',
                        case["手順"] if "手順" in case else [],
                        case['想定結果'],
                        case['エビデンス'] if 'エビデンス' in case and case['エビデンス'] == '要' else False
                    ))
                perspectives.append(IntegratedTestPerspective(perspectiveName, cases))
            blocks.append(IntegratedTestBlock(blockName, perspectives))
        return blocks
