class ExcelSheetCell():
    def __init__(self, value, style, dataValidation = None) -> None:
        self.value = value
        self.style = style
        self.dataValidation = dataValidation

    def getDataValidation(self) -> list:
        return self.dataValidation

    def getStyle(self):
        return self.style

    def getValue(self) -> str:
        return self.value

    def hasValidationList(self):
        return self.dataValidation != None
