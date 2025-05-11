class IntegratedTest():
    def __init__(self, batches=[], files=[], views=[]) -> None:
        self.batches = batches
        self.files = files
        self.views = views

    def getBatches(self) -> list:
        return self.batches

    def getFiles(self) -> list:
        return self.files
    
    def getViews(self) -> list:
        return self.views
