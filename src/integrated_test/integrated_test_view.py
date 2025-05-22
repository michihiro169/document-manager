class IntegratedTestView():
    def __init__(self, name, blocks, images=[], preparation=None, accounts=[]) -> None:
        self.name = name
        self.blocks = blocks
        self.images = images
        self.preparation = preparation
        self.accounts = accounts

    def getAccounts(self) -> list:
        return self.accounts

    def getImages(self) -> list:
        return self.images

    def getName(self) -> str:
        return self.name
    
    def getBlocks(self) -> list:
        return self.blocks

    def getPreparation(self):
        return self.preparation

    def hasImages(self) -> bool:
        return len(self.images) > 0
