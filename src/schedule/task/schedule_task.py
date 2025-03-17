class ScheduleTask():
    def __init__(self, name, estimate, achievement, member) -> None:
        self.name = name
        self.estimate = estimate
        self.achievement = achievement
        self.member = member

    def getAchievement(self) -> str:
        return self.achievement

    def getEstimate(self) -> str:
        return self.estimate

    def getMember(self) -> str:
        return self.member

    def getName(self) -> str:
        return self.name
