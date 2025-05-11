import yaml
from src.integrated_test.case.integrated_test_case import IntegratedTestCase
from src.integrated_test.config.integrated_test_config import IntegratedTestConfig
from src.integrated_test.config.integrated_test_config_batch import IntegratedTestConfigBatch
from src.integrated_test.config.integrated_test_config_component import IntegratedTestConfigComponent
from src.integrated_test.config.integrated_test_config_file import IntegratedTestConfigFile
from src.integrated_test.config.integrated_test_config_view import IntegratedTestConfigView
from src.integrated_test.block.integrated_test_block import IntegratedTestBlock
from src.integrated_test.perspective.integrated_test_perspective import IntegratedTestPerspective

class IntegratedTestConfigRepository():
    def find(self) -> IntegratedTestConfig:
        configBatch = None
        configComponent = None
        configFile = None
        configView = None
        types = ['component', 'batch', 'file', 'view']
        for type in types:
            data = {}
            with open(f"./storage/integrated_test/{type}_config/共通.yml", 'r') as file:
                data = yaml.safe_load(file)

            blockPerspectives = []
            for perspectiveName in data:
                cases = []
                for case in data[perspectiveName]:
                    cases.append(IntegratedTestCase(
                        case['パターン'],
                        case['手順'],
                        case['想定結果'],
                        case['エビデンス'] if 'エビデンス' in case and case['エビデンス'] == '要' else False
                    ))
                blockPerspectives.append(IntegratedTestPerspective(perspectiveName, cases))

            block = IntegratedTestBlock("共通", blockPerspectives)

            perspectives = None
            with open(f"./storage/integrated_test/{type}_config/テスト観点.yml", 'r') as file:
                perspectives = yaml.safe_load(file)

            if type == 'component':
                configComponent = IntegratedTestConfigComponent(block, perspectives)
            elif type == 'batch':
                configBatch = IntegratedTestConfigBatch(block, perspectives)
            elif type == 'file':
                configFile = IntegratedTestConfigFile(block, perspectives)
            elif type == 'view':
                configView = IntegratedTestConfigView(block, perspectives)

        return IntegratedTestConfig(
            configBatch,
            configComponent,
            configFile,
            configView
        )
