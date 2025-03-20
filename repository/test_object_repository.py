import glob
import os
import re
import yaml
from PIL import Image
from src.test.case.test_case import TestCase
from src.test.object.test_object import TestObject
from src.test.object.image.test_object_image import TestObjectImage
from src.test.object.part.test_object_part import TestObjectPart
from src.test.object.preparation.test_object_preparation import TestObjectPreparation
from src.test.perspective.test_perspective import TestPerspective

class TestObjectRepository():
    def getTestCases(self, path) -> list:
        data = {}
        with open(path, 'r') as file:
            data = yaml.safe_load(file)

        cases = []
        for case in data:
            cases.append(TestCase(
                case['パターン'] if 'パターン' in case else '',
                case["手順"] if "手順" in case else [],
                case['想定結果']
            ))

        return cases

    def find(self, testObjectName):
        parts = self.getTestObjectParts(f"./storage/test_object/{testObjectName}")

        # 画面イメージ
        imagePath = f"./storage/test_object/{testObjectName}/画面イメージ.png"
        image = None
        if os.path.isfile(imagePath):
            img = Image.open(imagePath)
            w, h = img.size
            image = TestObjectImage(imagePath, w, h)

        # 事前準備
        preparationPath = f"./storage/test_object/{testObjectName}/事前準備・注意点.yml"
        preparation = None
        if os.path.isfile(preparationPath):
            with open(preparationPath, 'r') as file:
                preparation = TestObjectPreparation(yaml.safe_load(file))

        return TestObject(testObjectName, parts, image, preparation)

    def get(self) -> list:
        testObjectPaths = glob.glob("./storage/test_object/*/")
        testObjects = []
        for path in testObjectPaths:
            result = re.match(r"./storage/test_object/(.+)/", path)
            name = result.group(1)
            testObjects.append(self.find(name))
        return testObjects

    def getTestObjectParts(self, path) -> list:
        testObjectPartPaths = glob.glob(f"{path}/*[0-9]*/*/")
        testObjectParts = []
        for path in testObjectPartPaths:
            result = re.match("./storage/test_object/.+?/([0-9]+?)/(.+?)/", path)
            name = result.group(2)

            perspectives = self.getTestPerspectives(path)

            testObjectParts.append(TestObjectPart(name, perspectives))
        return testObjectParts

    def getTestPerspectives(self, testObjectPartPath) -> list:
        testPerspectivePaths = glob.glob(f"{testObjectPartPath}/*.yml")
        perspectives = []
        for path in testPerspectivePaths:
            result = re.match("./storage/test_object/.+/.+/.+/(.+).yml", path)
            name = result.group(1)

            cases = self.getTestCases(path)

            perspectives.append(TestPerspective(name, cases))
        return perspectives
