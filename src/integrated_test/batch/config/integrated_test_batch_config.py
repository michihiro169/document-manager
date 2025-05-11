class IntegratedTestBatchConfig():
    def __init__(self, process, perspectives) -> None:
        self.process = process
        self.perspectives = perspectives

    def getProcess(self):
        return self.process

    def getPerspectives(self) -> list:
        return self.perspectives
