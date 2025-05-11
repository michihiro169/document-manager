import yaml
from src.integrated_test.case.integrated_test_case import IntegratedTestCase
from src.integrated_test.integrated_test_config import IntegratedTestConfig
from src.integrated_test.batch.config.integrated_test_batch_config import IntegratedTestBatchConfig
from src.integrated_test.batch.process.integrated_test_batch_process import IntegratedTestBatchProcess
from src.integrated_test.view.config.integrated_test_view_config import IntegratedTestViewConfig
from src.integrated_test.view.block.integrated_test_view_block import IntegratedTestViewBlock
from src.integrated_test.perspective.integrated_test_perspective import IntegratedTestPerspective

class IntegratedTestConfigRepository():
    def findConfig(self) -> IntegratedTestConfig:
        batchData = {}
        with open("./storage/integrated_test/batch_config/共通.yml", 'r') as file:
            batchData = yaml.safe_load(file)

        processPerspectives = []
        for perspectiveName in batchData:
            cases = []
            for case in batchData[perspectiveName]:
                cases.append(IntegratedTestCase(
                    case['パターン'],
                    case['手順'],
                    case['想定結果'],
                    case['エビデンス'] if 'エビデンス' in case and case['エビデンス'] == '要' else False
                ))
            processPerspectives.append(IntegratedTestPerspective(perspectiveName, cases))
        process = IntegratedTestBatchProcess("共通", processPerspectives)

        # テスト観点
        batchPerspectives = None
        with open("./storage/integrated_test/batch_config/テスト観点.yml", 'r') as file:
            batchPerspectives = yaml.safe_load(file)

        file = None

        viewData = {}
        with open("./storage/integrated_test/batch_config/共通.yml", 'r') as file:
            viewData = yaml.safe_load(file)

        blockPerspectives = []
        for perspectiveName in viewData:
            cases = []
            for case in viewData[perspectiveName]:
                cases.append(IntegratedTestCase(
                    case['パターン'],
                    case['手順'],
                    case['想定結果'],
                    case['エビデンス'] if 'エビデンス' in case and case['エビデンス'] == '要' else False
                ))
            blockPerspectives.append(IntegratedTestPerspective(perspectiveName, cases))
        block = IntegratedTestViewBlock("共通", blockPerspectives)

        # テスト観点
        viewPerspectives = None
        with open("./storage/integrated_test/view_config/テスト観点.yml", 'r') as file:
            viewPerspectives = yaml.safe_load(file)

        return IntegratedTestConfig(
            IntegratedTestBatchConfig(process, processPerspectives),
            file,
            IntegratedTestViewConfig(block, viewPerspectives)
        )
