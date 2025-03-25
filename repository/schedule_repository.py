import glob
import re
import yaml
from src.schedule.schedule import Schedule
from src.schedule.task.schedule_task import ScheduleTask
from src.schedule.ticket.schedule_ticket import ScheduleTicket
from src.schedule.phase.schedule_phase import SchedulePhase

class ScheduleRepository():
    def get(self) -> list:
        path = glob.glob("./storage/schedule/*.yml")[0]
        with open(path, 'r') as file:
            data = yaml.safe_load(file)

        tickets = []
        for ticketName in data:
            ticket = data[ticketName]
            phases = []
            for phaseName in ticket:
                phase = ticket[phaseName]
                tasks = []

                # フェーズと作業が同じ場合
                if self.hasTask(phase):
                    phases.append(SchedulePhase(phaseName, [
                        ScheduleTask(
                            '',
                            phase['見積'] if phase != None and '見積' in phase else None,
                            phase['実績'] if phase != None and '実績' in phase else None,
                            phase['担当'] if phase != None and '担当' in phase else None
                        )
                    ]))
                    continue

                for taskName in phase:
                    task = phase[taskName]
                    tasks.append(ScheduleTask(
                        taskName,
                        task['見積'] if task != None and '見積' in task  else None,
                        task['実績'] if task != None and '実績' in task  else None,
                        task['担当'] if task != None and '担当' in task  else None
                    ))

                phases.append(SchedulePhase(phaseName, tasks))

            tickets.append(ScheduleTicket(ticketName, phases))

        result = re.match(r"./storage/schedule/(.+).yml", path)
        return Schedule(result[1], tickets)

    def hasTask(self, data):
        if data == None:
            return True
        return '見積' in data or '実績' in data or '担当' in data
