class IntegratedTestFile():
    def __init__(self, name, blocks, image=None, preparation=None) -> None:
        self.name = name
        self.blocks = blocks
        self.image = image
        self.preparation = preparation

    def getImage(self) -> str:
        return self.image

    def getName(self) -> str:
        return self.name
    
    def getBlocks(self) -> list:
        return self.blocks

    def getPreparation(self):
        return self.preparation

    def hasImage(self) -> bool:
        return self.image != None
