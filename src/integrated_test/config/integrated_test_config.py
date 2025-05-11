class IntegratedTestConfig():
    def __init__(self, batch=None, component=None, file=None, view=None) -> None:
        self.batch = batch
        self.component = component
        self.file = file
        self.view = view

    def getBatch(self):
        return self.batch

    def getComponent(self):
        return self.component

    def getFile(self):
        return self.file

    def getView(self):
        return self.view
