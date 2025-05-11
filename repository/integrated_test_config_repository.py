import yaml
from src.integrated_test.case.integrated_test_case import IntegratedTestCase
from src.integrated_test.integrated_test_config import IntegratedTestConfig
from src.integrated_test.batch.config.integrated_test_batch_config import IntegratedTestBatchConfig
from src.integrated_test.batch.process.integrated_test_batch_process import IntegratedTestBatchProcess
from src.integrated_test.file.config.integrated_test_file_config import IntegratedTestFileConfig
from src.integrated_test.file.block.integrated_test_file_block import IntegratedTestFileBlock
from src.integrated_test.view.config.integrated_test_view_config import IntegratedTestViewConfig
from src.integrated_test.view.block.integrated_test_view_block import IntegratedTestViewBlock
from src.integrated_test.perspective.integrated_test_perspective import IntegratedTestPerspective

class IntegratedTestConfigRepository():
    def findConfig(self) -> IntegratedTestConfig:
        # バッチデータ
        batchData = {}
        with open("./storage/integrated_test/batch_config/共通.yml", 'r') as f:
            batchData = yaml.safe_load(f)

        # 対象のバッチ処理のテスト観点
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
        batch = IntegratedTestBatchProcess("共通", processPerspectives)

        # バッチ処理の全体のテスト観点
        batchPerspectives = None
        with open("./storage/integrated_test/batch_config/テスト観点.yml", 'r') as f:
            batchPerspectives = yaml.safe_load(f)

        # ファイルデータ
        fileData = {}
        with open("./storage/integrated_test/file_config/共通.yml", 'r') as f:
            fileData = yaml.safe_load(f)

        # 対象のファイルのテスト観点
        blockPerspectives = []
        for perspectiveName in fileData:
            cases = []
            for case in fileData[perspectiveName]:
                cases.append(IntegratedTestCase(
                    case['パターン'],
                    case['手順'],
                    case['想定結果'],
                    case['エビデンス'] if 'エビデンス' in case and case['エビデンス'] == '要' else False
                ))
            blockPerspectives.append(IntegratedTestPerspective(perspectiveName, cases))
        file = IntegratedTestFileBlock("共通", blockPerspectives)

        # ファイルの全体のテスト観点
        filePerspectives = None
        with open("./storage/integrated_test/file_config/テスト観点.yml", 'r') as f:
            filePerspectives = yaml.safe_load(f)

        # ビューデータ
        viewData = {}
        with open("./storage/integrated_test/view_config/共通.yml", 'r') as f:
            viewData = yaml.safe_load(f)

        # 対象のビューのテスト観点
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

        # ビューの全体のテスト観点
        viewPerspectives = None
        with open("./storage/integrated_test/view_config/テスト観点.yml", 'r') as f:
            viewPerspectives = yaml.safe_load(f)

        return IntegratedTestConfig(
            IntegratedTestBatchConfig(batch, batchPerspectives),
            IntegratedTestFileConfig(file, filePerspectives),
            IntegratedTestViewConfig(block, viewPerspectives)
        )
