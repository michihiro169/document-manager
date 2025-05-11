class IntegratedTestConfig():
    def __init__(self, batch=None, file=None, view=None) -> None:
        self.batch = batch
        self.file = file
        self.view = view

    def getBatch(self):
        return self.batch

    def getFile(self):
        return self.file

    def getView(self):
        return self.view
