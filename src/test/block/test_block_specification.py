from src.excel.excel import Excel
from src.excel.sheet.excel_sheet import ExcelSheet
from src.excel.sheet.cell.excel_sheet_cell import ExcelSheetCell
from src.excel.sheet.auto_filter.excel_sheet_auto_filter import ExcelSheetAutoFilter
from src.excel.sheet.cell.alignment.excel_sheet_cell_alignment import ExcelSheetCellAlignment
from src.excel.sheet.cell.border.excel_sheet_cell_border import ExcelSheetCellBorder
from src.excel.sheet.cell.fill.excel_sheet_cell_fill import ExcelSheetCellFill
from src.excel.sheet.cell.font.excel_sheet_cell_font import ExcelSheetCellFont
from src.excel.sheet.image.excel_sheet_image import ExcelSheetImage
from src.excel.sheet.cell.line.excel_sheet_cell_line import ExcelSheetCellLine
from src.excel.sheet.cell.style.excel_sheet_cell_style import ExcelSheetCellStyle
import datetime

class TestObjectSpecification():
    @classmethod
    def createStatusSheet(cls):
        values = [
            ["テストケース総数", f"=MAX(テストケース!A:A)"],
            ["実施予定数", f'=B1 - COUNTIF(テストケース!H:H,"-")'],
            ["正常数", f'=COUNTIF(テストケース!H:H,"○")'],
            ["エラー数", f'=COUNTIF(テストケース!H:H,"×")'],
            ["進捗率", "=B3/B2"],
        ]

        # 行作成
        rows = []
        for rowIndex, row in enumerate(values):
            cells = []
            for cellIndex, cell in enumerate(row):
                line = ExcelSheetCellLine('thin', '000000')
                cellStyle = ExcelSheetCellStyle(
                    ExcelSheetCellBorder(line, line, line, line),
                    ExcelSheetCellFill('solid', 'c8e6c6') if cellIndex == 0 else ExcelSheetCellFill('solid', 'ffffff'),
                    ExcelSheetCellAlignment('top'),
                )
                cell = ExcelSheetCell(cell, cellStyle)
                cells.append(cell)
            rows.append(cells)

        # 列幅
        widths = [16, 8]

        return ExcelSheet("実施状況", rows, widths)

    # 事前準備・注意点シート
    @classmethod
    def createPreparationSheet(cls, preparation):
        # 行作成
        rows = []
        for value in [] if preparation == None else preparation.getList():
            cellStyle = ExcelSheetCellStyle(
                ExcelSheetCellBorder(None, None, None, None),
                ExcelSheetCellFill('solid', 'ffffff'),
                ExcelSheetCellAlignment('top'),
            )
            cell = ExcelSheetCell(value, cellStyle)
            rows.append([cell])

        return ExcelSheet("事前準備・注意点", rows)

    @classmethod
    def createTestCaseSheetHeaderCells(cls):
        headerValues = [
            "ID",
            "部品名",
            "テスト観点",
            "テストパターン",
            "手順",
            "想定結果",
            "実施結果",
            "実施日",
            "実施者",
            "備考"
        ]

        headerCells = []
        for i, value in enumerate(headerValues):
            line = ExcelSheetCellLine('thin', '000000')
            cellStyle = ExcelSheetCellStyle(
                ExcelSheetCellBorder(line, line, line, line),
                ExcelSheetCellFill('solid', 'c8e6c6'),
                ExcelSheetCellAlignment('top')
            )
            cell = ExcelSheetCell(value, cellStyle)
            headerCells.append(cell)
        return headerCells

    @classmethod
    def toCell(cls, value = "", isTop = True, isBottom = True, validationData = None, wrapText = False):
        line = ExcelSheetCellLine('thin', '000000')
        return ExcelSheetCell(
            value,
            ExcelSheetCellStyle(
                ExcelSheetCellBorder(
                    line if isTop else None,
                    line if isBottom else None,
                    line,
                    line
                ),
                ExcelSheetCellFill('solid', 'ffffff'),
                ExcelSheetCellAlignment('top', wrapText),
                # 白字はフィルタ用
                ExcelSheetCellFont('000000') if isTop else ExcelSheetCellFont('ffffff'),
            ),
            validationData
        )

    @classmethod
    def toExcel(cls, testObject, testConfig):
        testObjectName = testObject.getName()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d')

        sheets = [
            cls.createStatusSheet(),
            cls.createPreparationSheet(testObject.getPreparation()),
            # テストケースシート
            cls.toSheet(testObject, testConfig),
        ]

        if testObject.hasImage():
            image = ExcelSheetImage(
                testObject.getImage().getPath(),
                testObject.getImage().getWidth(),
                testObject.getImage().getHeight()
            )
            sheets.append(ExcelSheet("画面イメージ", images=[image]))

        sheets.append(ExcelSheet("エビデンス"))

        return Excel(
            f"結合テスト仕様書_{testObjectName}_{timestamp}.xlsx",
            sheets
        )

    @classmethod
    def toSheet(cls, testObject, testConfig):
        # シート行の作成
        sheetRows = [cls.createTestCaseSheetHeaderCells()]

        # テストオブジェクトと共通のテストを結合
        parts = [testConfig.getTestObjectPart()] + testObject.getParts()

        # テストオブジェクトのテストケース行の作成
        for partIndex, element in enumerate(parts):
            for perspectiveIndex, perspective in enumerate(element.getPerspectives()):
                for caseIndex, case in enumerate(perspective.getCases()):
                    # 部品名、テスト観点が同じか
                    isPartTop = perspectiveIndex == 0 and caseIndex == 0
                    isPartLast = perspectiveIndex == len(element.getPerspectives()) - 1 and caseIndex == len(perspective.getCases()) - 1
                    isPerspectiveTop = caseIndex == 0
                    isPerspectiveLast = caseIndex == len(perspective.getCases()) - 1

                    # IDセル
                    IdCell = cls.toCell("=ROW()-1")
                    # 部品セル
                    partCell = cls.toCell(element.getName(), isPartTop, isPartLast)
                    # テスト観点セル
                    perspectiveCell = cls.toCell(
                        perspective.getName(),
                        isPerspectiveTop,
                        isPerspectiveLast,
                        testConfig.getPerspectives()
                    )
                    # テストパターンセル
                    patternCell = cls.toCell(case.getPattern())
                    # 手順のセル
                    procedureCell = cls.toCell(
                        "\r\n".join(['・' + procedure for procedure in case.getProcedures()]),
                        wrapText = True
                    )
                    # 想定結果のセル
                    forecastCell = cls.toCell(
                        "\r\n".join(['・' + forecast for forecast in case.getForecasts()]),
                        wrapText = True
                    )
                    # 実施結果、実施日、実施者、備考セル
                    resultCell = cls.toCell(validationData = ["○", "×", "-"])
                    dateCell = cls.toCell()
                    personCell = cls.toCell()
                    remarkCell = cls.toCell()

                    sheetRows.append([
                        IdCell,
                        partCell,
                        perspectiveCell,
                        patternCell,
                        procedureCell,
                        forecastCell,
                        resultCell,
                        dateCell,
                        personCell,
                        remarkCell,
                    ])

        # 列幅
        widths = [5, 16, 15, 16, 40, 40, 11, 9, 9, 40]

        return ExcelSheet(
            "テストケース",
            sheetRows,
            widths,
            ExcelSheetAutoFilter('A1:J1')
        )
