class SchedulePhase():
    def __init__(self, name, tasks=[]) -> None:
        self.name = name
        self.tasks = tasks

    def getName(self) -> str:
        return self.name

    def getTasks(self) -> list:
        return self.tasks
