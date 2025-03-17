import yaml
from src.schedule.config.schedule_config import ScheduleConfig

class ScheduleConfigRepository():
    def find(self) -> ScheduleConfig:
        members = []
        with open("./storage/schedule_config/メンバー.yml", 'r') as file:
            members = yaml.safe_load(file)

        initiatives = None
        with open("./storage/schedule_config/施策.yml", 'r') as file:
            initiatives = yaml.safe_load(file)

        holidays = None
        with open("./storage/schedule_config/休日.yml", 'r') as file:
            holidays = yaml.safe_load(file)

        return ScheduleConfig(members, initiatives, holidays)
