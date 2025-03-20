class TestConfig():
    def __init__(self, testObjectPart, perspectives) -> None:
        self.testObjectPart = testObjectPart
        self.perspectives = perspectives

    def getTestObjectPart(self):
        return self.testObjectPart

    def getPerspectives(self) -> list:
        return self.perspectives
