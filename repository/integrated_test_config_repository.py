import yaml
from src.integrated_test.case.test_case import TestCase
from src.integrated_test.config.test_config import TestConfig
from src.integrated_test.view.block.integrated_test_view_block import IntegratedTestViewBlock
from src.integrated_test.perspective.integrated_test_perspective import IntegratedTestPerspective

class IntegratedTestConfigRepository():
    def findTestConfig(self) -> TestConfig:
        data = {}
        with open("./storage/integrated_test/view_config/共通.yml", 'r') as file:
            data = yaml.safe_load(file)

        blockPerspectives = []
        for perspectiveName in data:
            cases = []
            for case in data[perspectiveName]:
                cases.append(TestCase(
                    case['パターン'],
                    case['手順'],
                    case['想定結果'],
                    case['エビデンス'] if 'エビデンス' in case and case['エビデンス'] == '要' else False
                ))
            blockPerspectives.append(IntegratedTestPerspective(perspectiveName, cases))
        blocks = IntegratedTestViewBlock("共通", blockPerspectives)

        # テスト観点
        perspectives = None
        with open("./storage/integrated_test/view_config/テスト観点.yml", 'r') as file:
            perspectives = yaml.safe_load(file)

        return TestConfig(blocks, perspectives)
