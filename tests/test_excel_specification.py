import unittest

from src.excel.excel_specification import ExcelSpecification

class TestExcelSpecification(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName)

    def test_getAlphabet(self):
        self.assertEqual(ExcelSpecification.getAlphabet(0), "A")
        self.assertEqual(ExcelSpecification.getAlphabet(25), "Z")
