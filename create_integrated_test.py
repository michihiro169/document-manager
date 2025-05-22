from lib.excel_lib import ExcelLib
from repository.integrated_test_config_repository import IntegratedTestConfigRepository
from repository.integrated_test_repository import IntegratedTestRepository
from src.integrated_test.integrated_test_specification import IntegratedTestSpecification
import sys

# 結合テスト仕様書を生成する
# コントローラー兼アプリケーションルール

integratedTestConfigRepository = IntegratedTestConfigRepository()
integratedTestRepository = IntegratedTestRepository()

integratedTestConfig = integratedTestConfigRepository.find()
integratedTests = integratedTestRepository.get() if len(sys.argv) == 1 else [integratedTestRepository.find(sys.argv[1])]

for integratedTest in integratedTests.getBatches():
    prefix = 'バッチ処理'
    print(f"{prefix}{integratedTest.getName()} 作成中...")
    excel = IntegratedTestSpecification.toExcel(integratedTest, integratedTestConfig.getBatch(), prefix)
    ExcelLib.save(excel)

for integratedTest in integratedTests.getComponents():
    prefix = 'コンポーネント'
    print(f"{prefix}{integratedTest.getName()} 作成中...")
    excel = IntegratedTestSpecification.toExcel(integratedTest, integratedTestConfig.getComponent(), prefix)
    ExcelLib.save(excel)

for integratedTest in integratedTests.getFiles():
    prefix = 'ファイル'
    print(f"{prefix}{integratedTest.getName()} 作成中...")
    excel = IntegratedTestSpecification.toExcel(integratedTest, integratedTestConfig.getFile(), prefix)
    ExcelLib.save(excel)

for integratedTest in integratedTests.getViews():
    prefix = '画面'
    print(f"{prefix}{integratedTest.getName()} 作成中...")
    excel = IntegratedTestSpecification.toExcel(integratedTest, integratedTestConfig.getView(), prefix)
    ExcelLib.save(excel)
