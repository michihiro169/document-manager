from lib.excel_lib import ExcelLib
from repository.test_config_repository import TestConfigRepository
from repository.test_object_repository import TestBlockRepository
from src.test.object.test_object_specification import TestObjectSpecification
import sys

# 結合テスト仕様書を生成する
# コントローラー兼アプリケーションルール

testConfigRepository = TestConfigRepository()
testObjectRepository = TestBlockRepository()

testConfig = testConfigRepository.getTestConfig()
testObjects = testObjectRepository.get() if len(sys.argv) == 1 else [testObjectRepository.find(sys.argv[1])]

for testObject in testObjects:
    print(f"{testObject.getName()} 作成中...")

    excel = TestObjectSpecification.toExcel(testObject, testConfig)
    ExcelLib.save(excel)
