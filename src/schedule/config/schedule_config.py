class ScheduleConfig():
    def __init__(self, members, initiatives, holidays) -> None:
        self.members = members
        self.initiatives = initiatives
        self.holidays = holidays

    def getHolidays(self) -> list:
        return self.holidays

    def getInitiatives(self) -> list:
        return self.initiatives

    def getMembers(self) -> list:
        return self.members
