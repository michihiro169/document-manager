class IntegratedTestConfig():
    def __init__(self, testBlockElement, perspectives) -> None:
        self.testBlockElement = testBlockElement
        self.perspectives = perspectives

    def getTestBlockElement(self):
        return self.testBlockElement

    def getPerspectives(self) -> list:
        return self.perspectives
