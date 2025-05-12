class IntegratedTestAccount():
    def __init__(self, name, configs) -> None:
        self.name = name
        self.configs = configs

    def getConfigs(self) -> list:
        return self.configs

    def getName(self) -> list:
        return self.name
