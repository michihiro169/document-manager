import yaml
from src.integrated_test.case.test_case import TestCase
from src.integrated_test.config.test_config import TestConfig
from src.integrated_test.view.block.integrated_test_view_block import IntegratedTestViewBlock
from src.integrated_test.perspective.test_perspective import TestPerspective

class IntegratedTestConfigRepository():
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
                    case['想定結果'],
                    case['エビデンス'] if 'エビデンス' in case and case['エビデンス'] == '要' else False
                ))
            perspectives.append(TestPerspective(perspectiveName, cases))
        blockElements = IntegratedTestViewBlock("共通", perspectives)

        # テスト観点
        perspectives = None
        with open("./storage/test_config/テスト観点.yml", 'r') as file:
            perspectives = yaml.safe_load(file)

        return TestConfig(blockElements, perspectives)
