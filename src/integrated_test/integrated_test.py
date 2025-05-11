class IntegratedTest():
    def __init__(self, batches=[], components=[], files=[], views=[]) -> None:
        self.batches = batches
        self.components = components
        self.files = files
        self.views = views

    def getBatches(self) -> list:
        return self.batches

    def getComponents(self) -> list:
        return self.components

    def getFiles(self) -> list:
        return self.files
    
    def getViews(self) -> list:
        return self.views
