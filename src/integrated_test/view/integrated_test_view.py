class IntegratedTestView():
    def __init__(self, name, elements, image=None, preparation=None) -> None:
        self.name = name
        self.elements = elements
        self.image = image
        self.preparation = preparation

    def getImage(self) -> str:
        return self.image

    def getName(self) -> str:
        return self.name
    
    def getElements(self) -> list:
        return self.elements

    def getPreparation(self):
        return self.preparation

    def hasImage(self) -> bool:
        return self.image != None
