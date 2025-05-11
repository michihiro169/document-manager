class IntegratedTestBatch():
    def __init__(self, name, processes, preparation=None) -> None:
        self.name = name
        self.processes = processes
        self.preparation = preparation

    def getName(self) -> str:
        return self.name
    
    def getProcesses(self) -> list:
        return self.processes

    def getPreparation(self):
        return self.preparation
