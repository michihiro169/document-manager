class IntegratedTestBatch():
    def __init__(self, name, blocks, matrices=[], images=[], preparation=None, accounts=None) -> None:
        self.name = name
        self.blocks = blocks
        self.matrices = matrices
        self.images = images
        self.preparation = preparation
        self.accounts = accounts

    def getAccounts(self) -> list:
        return self.accounts

    def getImages(self) -> list:
        return self.images

    def getMatrices(self) -> list:
        return self.matrices

    def getName(self) -> str:
        return self.name
    
    def getBlocks(self) -> list:
        return self.blocks

    def getPreparation(self):
        return self.preparation

    def hasImages(self) -> bool:
        return len(self.images) > 0

    def hasTestData(self) -> bool:
        return self.accounts != None
