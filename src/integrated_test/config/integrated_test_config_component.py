class IntegratedTestConfigComponent():
    def __init__(self, block, perspectives) -> None:
        self.block = block
        self.perspectives = perspectives

    def getBlock(self):
        return self.block

    def getPerspectives(self) -> list:
        return self.perspectives
