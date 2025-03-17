class ScheduleTicket():
    def __init__(self, name, phases = []) -> None:
        self.name = name
        self.phases = phases

    def getName(self) -> str:
        return self.name

    def getPhases(self) -> list:
        return self.phases
