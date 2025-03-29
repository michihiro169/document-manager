class TestBlock():
    def __init__(self, name, parts, image=None, preparation=None) -> None:
        self.name = name
        self.parts = parts
        self.image = image
        self.preparation = preparation

    def getImage(self) -> str:
        return self.image

    def getName(self) -> str:
        return self.name
    
    def getParts(self) -> list:
        return self.parts

    def getPreparation(self):
        return self.preparation

    def hasImage(self) -> bool:
        return self.image != None
