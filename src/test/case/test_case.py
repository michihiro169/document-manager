class TestCase():
    def __init__(self, pattern, procedures, forecast) -> None:
        self.forecast = forecast
        self.pattern = pattern
        self.procedures = procedures

    def getForecasts(self) -> str:
        return self.forecast

    def getPattern(self) -> str:
        return self.pattern

    def getProcedures(self) -> list:
        return self.procedures
