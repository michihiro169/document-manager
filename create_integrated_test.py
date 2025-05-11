from lib.excel_lib import ExcelLib
from repository.integrated_test_config_repository import IntegratedTestConfigRepository
from repository.integrated_test_repository import IntegratedTestRepository
from src.integrated_test.view.integrated_test_view_specification import IntegratedTestViewSpecification
import sys

# 結合テスト仕様書を生成する
# コントローラー兼アプリケーションルール

integratedTestConfigRepository = IntegratedTestConfigRepository()
integratedTestRepository = IntegratedTestRepository()

integratedTestConfig = integratedTestConfigRepository.findConfig()
integratedTests = integratedTestRepository.get() if len(sys.argv) == 1 else [integratedTestRepository.find(sys.argv[1])]

for integratedTest in integratedTests.getViews():
    print(f"{integratedTest.getName()} 作成中...")

    excel = IntegratedTestViewSpecification.toExcel(integratedTest, integratedTestConfig.getView())
    ExcelLib.save(excel)
