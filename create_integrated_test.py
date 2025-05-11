from lib.excel_lib import ExcelLib
from repository.test_config_repository import TestConfigRepository
from repository.test_block_repository import IntegratedTestRepository
from src.integrated_test.view.integrated_test_view_specification import IntegratedTestViewSpecification
import sys

# 結合テスト仕様書を生成する
# コントローラー兼アプリケーションルール

testConfigRepository = TestConfigRepository()
testBlockRepository = IntegratedTestRepository()

testConfig = testConfigRepository.getTestConfig()
testBlocks = testBlockRepository.get() if len(sys.argv) == 1 else [testBlockRepository.find(sys.argv[1])]

for testBlock in testBlocks:
    print(f"{testBlock.getName()} 作成中...")

    excel = IntegratedTestViewSpecification.toExcel(testBlock, testConfig)
    ExcelLib.save(excel)
