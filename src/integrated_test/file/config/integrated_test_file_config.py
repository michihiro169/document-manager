class IntegratedTestFileConfig():
    def __init__(self, block, perspectives) -> None:
        self.block = block
        self.perspectives = perspectives

    def getTestBlock(self):
        return self.block

    def getPerspectives(self) -> list:
        return self.perspectives
