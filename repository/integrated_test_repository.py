import glob
import os
import re
import yaml
from jinja2 import Template
from PIL import Image
from src.integrated_test.batch.integrated_test_batch import IntegratedTestBatch
from src.integrated_test.batch.process.integrated_test_batch_process import IntegratedTestBatchProcess
from src.integrated_test.batch.preparation.integrated_test_batch_preparation import IntegratedTestBatchPreparation
from src.integrated_test.case.integrated_test_case import IntegratedTestCase
from src.integrated_test.view.integrated_test_view import IntegratedTestView
from src.integrated_test.view.image.integrated_test_view_image import IntegratedTestViewImage
from src.integrated_test.view.block.integrated_test_view_block import IntegratedTestViewBlock
from src.integrated_test.view.preparation.integrated_test_view_preparation import IntegratedTestViewPreparation
from src.integrated_test.perspective.integrated_test_perspective import IntegratedTestPerspective
from src.integrated_test.integrated_test import IntegratedTest

class IntegratedTestRepository():
    def findBatch(self, name):
        # ビューのテストケース
        batchProcesses = self.getBatchProcess(f"./storage/integrated_test/batch/{name}/テストケース.yml")

        # ビューの事前準備
        preparationPath = f"./storage/integrated_test/batch/{name}/事前準備・注意点.yml"
        preparation = None
        if os.path.isfile(preparationPath):
            with open(preparationPath, 'r') as file:
                data = yaml.safe_load(file)
                preparation = IntegratedTestBatchPreparation([] if data == None else data)

        return IntegratedTestBatch(name, batchProcesses, preparation)

    def findView(self, name):
        # ビューのテストケース
        viewBlocks = self.getViewBlocks(f"./storage/integrated_test/view/{name}/テストケース.yml")

        # ビューの画面イメージ
        imagePath = f"./storage/integrated_test/view/{name}/画面イメージ.png"
        image = None
        if os.path.isfile(imagePath):
            img = Image.open(imagePath)
            w, h = img.size
            image = IntegratedTestViewImage(imagePath, w, h)

        # ビューの事前準備
        preparationPath = f"./storage/integrated_test/view/{name}/事前準備・注意点.yml"
        preparation = None
        if os.path.isfile(preparationPath):
            with open(preparationPath, 'r') as file:
                data = yaml.safe_load(file)
                preparation = IntegratedTestViewPreparation([] if data == None else data)

        return IntegratedTestView(name, viewBlocks, image, preparation)

    def get(self) -> list:
        batchPaths = glob.glob("./storage/integrated_test/batch/*/")
        batches = []
        for path in batchPaths:
            result = re.match(r"./storage/integrated_test/batch/(.+)/", path)
            name = result.group(1)
            batches.append(self.findBatch(name))

        files = []

        viewPaths = glob.glob("./storage/integrated_test/view/*/")
        views = []
        for path in viewPaths:
            result = re.match(r"./storage/integrated_test/view/(.+)/", path)
            name = result.group(1)
            views.append(self.findView(name))

        return IntegratedTest(batches, files, views)

    def getBatchProcess(self, path) -> list:
        output = ''
        with open(path, 'r') as file:
            template = Template(file.read())
            output = template.render()

        data = yaml.safe_load(output)

        batchProcess = []
        for _, processName in enumerate(data):
            perspectives = []
            for _, perspectiveName in enumerate(data[processName]):
                cases = []
                for _, case in enumerate(data[processName][perspectiveName]):
                    cases.append(IntegratedTestCase(
                        case['パターン'] if 'パターン' in case else '',
                        case["手順"] if "手順" in case else [],
                        case['想定結果'],
                        case['エビデンス'] if 'エビデンス' in case and case['エビデンス'] == '要' else False
                    ))
                perspectives.append(IntegratedTestPerspective(perspectiveName, cases))
            batchProcess.append(IntegratedTestBatchProcess(processName, perspectives))
        return batchProcess

    def getViewBlocks(self, path) -> list:
        output = ''
        with open(path, 'r') as file:
            template = Template(file.read())
            output = template.render()

        data = yaml.safe_load(output)

        viewBlocks = []
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
            viewBlocks.append(IntegratedTestViewBlock(blockName, perspectives))
        return viewBlocks
