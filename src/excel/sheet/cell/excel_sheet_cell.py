class ExcelSheetCell():
    def __init__(self, value = "", style = None, dataValidation = None, hyperLink=None) -> None:
        self.value = value
        self.style = style
        self.dataValidation = dataValidation
        self.hyperLink = hyperLink

    def getDataValidation(self) -> list:
        return self.dataValidation

    def getHyperLink(self) -> str:
        return self.hyperLink

    def getStyle(self):
        return self.style

    def getValue(self) -> str:
        return self.value
    
    def hasHyperLink(self) -> bool:
        return self.hyperLink != None

    def hasStyle(self) -> bool:
        return self.style != None

    def hasValidationList(self):
        return self.dataValidation != None
