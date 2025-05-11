class IntegratedTestFileImage():
    def __init__(self, path, width, height) -> None:
        self.path = path
        self.width = width
        self.height = height

    def getHeight(self):
        return self.height

    def getPath(self) -> str:
        return self.path

    def getWidth(self):
        return self.width
