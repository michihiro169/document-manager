from lib.excel_lib import ExcelLib
from repository.schedule_config_repository import ScheduleConfigRepository
from repository.schedule_repository import ScheduleRepository
from src.schedule.schedule_specification import ScheduleSpecification
import sys

# スケジュールを生成する
# コントローラー兼アプリケーションルール

startDate = sys.argv[1]
endDate = sys.argv[2]

scheduleConfigRepository = ScheduleConfigRepository()
scheduleRepository = ScheduleRepository()

scheduleConfig = scheduleConfigRepository.find()
schedule = scheduleRepository.get()

excel = ScheduleSpecification.toExcel(schedule, scheduleConfig, startDate, endDate)
ExcelLib.save(excel)
