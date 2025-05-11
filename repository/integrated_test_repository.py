import glob
import os
import re
import yaml
from jinja2 import Template
from PIL import Image
from src.integrated_test.case.integrated_test_case import IntegratedTestCase
from src.integrated_test.view.integrated_test_view import IntegratedTestView
from src.integrated_test.view.image.integrated_test_view_image import IntegratedTestViewImage
from src.integrated_test.view.block.integrated_test_view_block import IntegratedTestViewBlock
from src.integrated_test.view.preparation.integrated_test_view_preparation import IntegratedTestViewPreparation
from src.integrated_test.perspective.integrated_test_perspective import IntegratedTestPerspective

class IntegratedTestRepository():
    def find(self, viewName):
        # テストケース
        blocks = self.getViewBlocks(f"./storage/integrated_test/view/{viewName}/テストケース.yml")

        # 画面イメージ
        imagePath = f"./storage/integrated_test/view/{viewName}/画面イメージ.png"
        image = None
        if os.path.isfile(imagePath):
            img = Image.open(imagePath)
            w, h = img.size
            image = IntegratedTestViewImage(imagePath, w, h)

        # 事前準備
        preparationPath = f"./storage/integrated_test/view/{viewName}/事前準備・注意点.yml"
        preparation = None
        if os.path.isfile(preparationPath):
            with open(preparationPath, 'r') as file:
                data = yaml.safe_load(file)
                preparation = IntegratedTestViewPreparation([] if data == None else data)

        return IntegratedTestView(viewName, blocks, image, preparation)

    def get(self) -> list:
        viewPaths = glob.glob("./storage/integrated_test/view/*/")
        views = []
        for path in viewPaths:
            result = re.match(r"./storage/integrated_test/view/(.+)/", path)
            name = result.group(1)
            views.append(self.find(name))
        return views

    def getViewBlocks(self, path) -> list:
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
            blocks.append(IntegratedTestViewBlock(blockName, perspectives))
        return blocks
