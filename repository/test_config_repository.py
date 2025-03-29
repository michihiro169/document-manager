import yaml
from src.test.case.test_case import TestCase
from src.test.config.test_config import TestConfig
from src.test.block.element.test_block_element import TestBlockElement
from src.test.perspective.test_perspective import TestPerspective

class TestConfigRepository():
    def getTestConfig(self) -> TestConfig:
        data = {}
        with open("./storage/test_config/共通.yml", 'r') as file:
            data = yaml.safe_load(file)

        perspectives = []
        for perspectiveName in data:
            cases = []
            for case in data[perspectiveName]:
                cases.append(TestCase(
                    case['パターン'],
                    case['手順'],
                    case['想定結果']
                ))
            perspectives.append(TestPerspective(perspectiveName, cases))
        blockElements = TestBlockElement("共通", perspectives)

        # テスト観点
        perspectives = None
        with open("./storage/test_config/テスト観点.yml", 'r') as file:
            perspectives = yaml.safe_load(file)

        return TestConfig(blockElements, perspectives)
