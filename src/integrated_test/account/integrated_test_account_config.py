class IntegratedTestAccountConfig():
    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value

    def getKey(self) -> list:
        return self.key

    def getValue(self) -> list:
        return self.value
