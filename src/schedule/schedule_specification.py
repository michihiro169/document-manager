from src.excel.excel import Excel
from src.excel.sheet.excel_sheet import ExcelSheet
from src.excel.sheet.auto_filter.excel_sheet_auto_filter import ExcelSheetAutoFilter
from src.excel.sheet.cell.excel_sheet_cell import ExcelSheetCell
from src.excel.sheet.cell.alignment.excel_sheet_cell_alignment import ExcelSheetCellAlignment
from src.excel.sheet.cell.border.excel_sheet_cell_border import ExcelSheetCellBorder
from src.excel.sheet.cell.fill.excel_sheet_cell_fill import ExcelSheetCellFill
from src.excel.sheet.cell.font.excel_sheet_cell_font import ExcelSheetCellFont
from src.excel.sheet.cell.line.excel_sheet_cell_line import ExcelSheetCellLine
from src.excel.sheet.cell.style.excel_sheet_cell_style import ExcelSheetCellStyle
import datetime
import re

# スケジュールに業界的な正解はないが最大公約数的な取り決めとして定義する
class ScheduleSpecification():
    # 分析シート作成
    @classmethod
    def createAnalysisSheet(cls, schedule, config):
        members = config.getMembers()

        # 分析用の値作成
        values = []

        # 作業者別の稼働率
        values.append(["作業者別の稼働率", '担当者が{名前}の行の実績の合計 / 稼働日 * 8'])
        for member in members:
            values.append([f"=SUMIF(作業リスト!H:H,\"{member}\",作業リスト!F:F) / (進捗!B3 * 8)"])
        values.append([''])

        # 全体の速度
        values.append(['全体の速度'])
        values.append(["=進捗!B7/(進捗!B4)", '実績工数合計 / 人員数'])
        values.append([''])

        # チケット別の超過率
        tickets = schedule.getTickets()
        values.append(['チケット別の超過率', 'チケットが{名前}の行の実績の合計 / チケットが{名前}の行の見積の合計'])
        for ticket in tickets:
            values.append([f"=SUMIF(作業リスト!B:B,\"{ticket.getName()}\",作業リスト!F:F) / SUMIF(作業リスト!B:B,\"{ticket.getName()}\",作業リスト!E:E)"])
        values.append([''])

        # 担当者別の超過率
        values.append(['担当者別の超過率', '担当者が{名前}の行の実績の合計 / チケットが{名前}の行の見積の合計'])
        for member in members:
            values.append([f"=SUMIF(作業リスト!H:H,\"{member}\",作業リスト!F:F) / SUMIF(作業リスト!H:H,\"{ticket.getName()}\",作業リスト!E:E)"])
        values.append([''])

        # 担当者 * 作業 別の超過率
        values.append(['担当者 * 作業 別の超過率'])
        values.append([''])

        # 作業者の一人称率
        values.append(['作業者の一人称率'])
        values.append([''])

        # 作業者サポート数
        values.append(['作業者サポート数'])
        values.append([''])

        # 行作成
        rows = []
        for _, row in enumerate(values):
            cells = []
            for _, cell in enumerate(row):
                cellStyle = ExcelSheetCellStyle()
                cell = ExcelSheetCell(cell, cellStyle)
                cells.append(cell)
            rows.append(cells)

        # 列幅
        widths = [25, 67]

        return ExcelSheet("分析", rows, widths)

    # 稼働日シート作成
    @classmethod
    def createBusinessDaysSheet(cls, config, startDate, endDate):
        # スケジュール開始日と終了日
        result = re.match("([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})", startDate)
        d1 = datetime.date(int(result.group(1)), int(result.group(2)), int(result.group(3)))
        result = re.match("([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})", endDate)
        d2 = datetime.date(int(result.group(1)), int(result.group(2)), int(result.group(3)))

        # 祝日
        holidays = []
        for holiday in config.getHolidays():
            result = re.match("([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})", holiday)
            holidays.append(datetime.date(int(result.group(1)), int(result.group(2)), int(result.group(3))))

        # 稼働日
        businessDays = []
        # +1は当日を開始日と終了日の差分に含めるため
        for i in range((d2 - d1).days + 1):
            # 土日と休日はスキップ
            if d1.weekday() >= 5 or any(d == d1 for d in holidays):
                d1 = d1 + datetime.timedelta(days=1)
                continue
            businessDays.append(d1)
            d1 = d1 + datetime.timedelta(days=1)

        # 稼働日から行作成
        rows = []
        for day in businessDays:
            cellStyle = ExcelSheetCellStyle()
            rows.append([ExcelSheetCell(day, cellStyle)])

        return ExcelSheet("稼働日", rows, [11])

    # 進捗シート作成
    @classmethod
    def createSheetProgress(cls, config, startDate, endDate):
        rowValues = [
            ["開始日", startDate],
            ["終了日", endDate, "当日の業務終了時点でリリース状態にあること"],
            ["稼働日", f"=COUNT(稼働日!A:A)"],
            ["人員数", len(config.getMembers())],
            ["予算工数", f"=B3 * B4 * 8", "稼働日 * 人員数 * 8h"],
            ["見積工数合計", f"=SUM(作業リスト!E:E)", 'リリースに必要な全ての作業について見積もった工数。予算工数との差分はバッファとして確保'],
            ["実績工数合計", f'=SUM(作業リスト!F:F)', '人員が実際に消費した工数'],
            ["完了予定工数", f'=MATCH(TODAY(), 稼働日!A:A) * 8 * B4', '作業n日目 * 8h * 人員数。完了工数と一致していればオンスケ'],
            ["完了工数", f'=SUMIF(作業リスト!G:G,"完了", 作業リスト!F:F) + SUMIF(作業リスト!G:G, "対応しない", 作業リスト!F:F)', '状態が完了または対応しないの作業の合計'],
            ["速度", f"=B9 / IF(COUNTIF(稼働日!A:A, TODAY()), MATCH(TODAY(), 稼働日!A:A), MATCH(MAX(稼働日!A:A), 稼働日!A:A))", "完了工数 / 作業n日目"],
        ]

        rows = []
        for _, rowValue in enumerate(rowValues):
            cells = []
            for _, cellValue in enumerate(rowValue):
                cellStyle = ExcelSheetCellStyle()
                cell = ExcelSheetCell(cellValue, cellStyle)
                cells.append(cell)
            rows.append(cells)

        # 列幅
        widths = [14, 10, 78]

        return ExcelSheet("進捗", rows, widths)

    # 作業リストシートのヘッダ作成
    @classmethod
    def createScheduleSheetHeader(cls, config):
        # ヘッダの値
        values = [
            [
                {'value': 'ID', 'border':{'top': True, 'right': True, 'left': True}},
                {'value': 'チケット', 'border':{'top': True, 'right': True, 'left': True}},
                {'value': 'フェーズ', 'border':{'top': True, 'right': True, 'left': True}},
                {'value': '作業名', 'border':{'top': True, 'right': True, 'left': True}},
                {'value': '見積(h)', 'border':{'top': True, 'right': True, 'left': True}},
                {'value': '実績(h)', 'border':{'top': True, 'right': True, 'left': True}},
                {'value': '状態', 'border':{'top': True, 'right': True, 'left': True}},
                {'value': '担当者', 'border':{'top': True, 'right': True, 'left': True}}
            ]
        ]
        values.append([{'value': '', 'border':{'left': True, 'right': True, 'bottom': True}} for i in range(len(values[0]))])

        # ヘッダの値にサポート追加
        members = config.getMembers()
        if len(members) > 1:
            for i, member in enumerate(members):
                values[0].append({
                    'value': 'サポート' if i == 0 else '',
                    'border': {'bottom': True, 'left': True} if i == 0 else {'bottom': True}
                })
                values[1].append({
                    'value': member,
                    'border': {'bottom': True, 'left': True} if i == 0 else {'bottom': True}
                })

        # ヘッダの値に施策を追加
        initiatives = config.getInitiatives()
        if initiatives != None and len(initiatives) > 0:
            for i, initiative in enumerate(initiatives):
                values[0].append({
                    'value': '施策' if i == 0 else '',
                    'border':{'bottom': True, 'left': True} if i == 0 else {'bottom': True}
                })
                values[1].append({
                    'value': initiative,
                    'border': {'bottom': True, 'left': True} if i == 0 else {'bottom': True}
                })

        # 備考追加
        values[0].append({'value': '備考', 'border':{'left': True, 'right': True}})
        values[1].append({'value': '', 'border': {'bottom': True, 'left': True, 'right': True}})

        # 行作成
        rows = []
        for rowIndex, row in enumerate(values):
            rows.append([])
            for _, value in enumerate(row):
                line = ExcelSheetCellLine('thin', '000000')
                cellStyle = ExcelSheetCellStyle(
                    ExcelSheetCellBorder(
                        line if 'top' in value['border'] else None,
                        line if 'bottom' in value['border'] else None,
                        line if 'right' in value['border'] else None,
                        line if 'left' in value['border'] else None,
                    ),
                    ExcelSheetCellFill('solid', 'c8e6c6'),
                    ExcelSheetCellAlignment('top')
                )
                cell = ExcelSheetCell(value['value'], cellStyle)
                rows[rowIndex].append(cell)
        return rows

    @classmethod
    def toCell(
        cls,
        value = "",
        isTop = True,
        isBottom = True,
        isRight = True,
        validationData = None,
        wrapText = False
    ):
        line = ExcelSheetCellLine('thin', '000000')
        return ExcelSheetCell(
            value,
            ExcelSheetCellStyle(
                ExcelSheetCellBorder(
                    line if isTop else None,
                    line if isBottom else None,
                    line if isRight else None,
                    None
                ),
                ExcelSheetCellFill('solid', 'ffffff'),
                ExcelSheetCellAlignment('top', wrapText),
                # 白字はフィルタ用
                ExcelSheetCellFont('000000') if isTop else ExcelSheetCellFont('ffffff'),
            ),
            validationData
        )

    @classmethod
    def toExcel(cls, schedule, config, startDate, endDate):
        sheets = [
            cls.toSheet(schedule, config),
            cls.createSheetProgress(config, startDate, endDate),
            cls.createAnalysisSheet(schedule, config),
            cls.createBusinessDaysSheet(config, startDate, endDate),
        ]
        return Excel(
            f"スケジュール_{schedule.getName()}.xlsx",
            sheets
        )

    @classmethod
    def toSheet(cls, schedule, config):
        # シート行の作成
        sheetRows = cls.createScheduleSheetHeader(config)

        # チケット別、フェーズ別の作業行を作成
        for _, ticket in enumerate(schedule.getTickets()):
            for phaseIndex, phase in enumerate(ticket.getPhases()):
                for taskIndex, task in enumerate(phase.getTasks()):
                    # チケット、フェーズが同じか
                    isTicketTop = phaseIndex == 0 and taskIndex == 0
                    isTicketLast = phaseIndex == len(ticket.getPhases()) - 1 and taskIndex == len(phase.getTasks()) - 1
                    isPhaseTop = taskIndex == 0
                    isPhaseLast = taskIndex == len(phase.getTasks()) - 1

                    # IDセル
                    IdCell = cls.toCell("=ROW()-2")
                    # チケットセル
                    ticketCell = cls.toCell(ticket.getName(), isTicketTop, isTicketLast)
                    # フェーズセル
                    phaseCell = cls.toCell(
                        phase.getName(),
                        isPhaseTop,
                        isPhaseLast,
                        task.getName() != ""
                    )
                    # タスクセル
                    taskCell = cls.toCell(task.getName())
                    # 見積のセル
                    estimateCell = cls.toCell(task.getEstimate())
                    # 実績のセル
                    achievementCell = cls.toCell(task.getAchievement())
                    # 状態のセル
                    statusCell = cls.toCell(validationData = ["未着手", "作業中", "完了", "対応しない"])
                    # 担当者のセル
                    memberCell = cls.toCell(task.getMember(), validationData = config.getMembers())
                    # サポートセル
                    memberCells = []
                    for _ in config.getMembers():
                        memberCells.append(cls.toCell())
                    # 施策セル
                    initiativeCells = []
                    for _ in config.getInitiatives():
                        initiativeCells.append(cls.toCell(validationData = ['あり', 'なし', '対象外']))
                    # 備考セル
                    remarkCell = cls.toCell()

                    row = [
                        IdCell,
                        ticketCell,
                        phaseCell,
                        taskCell,
                        estimateCell,
                        achievementCell,
                        statusCell,
                        memberCell,
                    ] + memberCells + initiativeCells + [remarkCell]
                    sheetRows.append(row)

        # 列幅
        widths = [4, 22, 22, 22, 7, 7, 11, 10]

        return ExcelSheet(
            "作業リスト",
            sheetRows,
            widths,
            ExcelSheetAutoFilter('A2:N2')
        )
