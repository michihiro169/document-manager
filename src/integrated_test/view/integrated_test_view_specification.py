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

class IntegratedTestViewSpecification():
    @classmethod
    def createPerspectiveSheet(cls, config):
        perspectives = config.getPerspectives()
        rows = []
        for name in perspectives:
            cells = [
                ExcelSheetCell(name),
                ExcelSheetCell('') if perspectives[name] == None else ExcelSheetCell(perspectives[name])
            ]
            rows.append(cells)
        return ExcelSheet("テスト観点", rows)

    @classmethod
    def createStatusSheet(cls):
        values = [
            ['テストケース数', f"=MAX(テストケース!A:A)"],
            ['実施予定数', f'=B1 - COUNTIF(テストケース!H:H,"-")'],
            ['正常数', f'=COUNTIF(テストケース!H:H,"○")'],
            ['エラー数', f'=COUNTIF(テストケース!H:H,"×")'],
            ['進捗率', '=B3/B2'],
        ]

        # 行作成
        rows = [[ExcelSheetCell('{環境名}')]]
        for _, row in enumerate(values):
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
        widths = [14, 8]

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
    def createTestCaseAndEvidenceSheet(cls, testBlock, testConfig):
        # シート行の作成
        testCaseSheetRows = [cls.createTestCaseSheetHeaderCells()]
        evidenceSheetRows = []

        # テストオブジェクトと共通のテストを結合
        elements = [testConfig.getTestBlock()] + testBlock.getBlocks()

        # テストオブジェクトのテストケース行の作成
        headerLen = len(testCaseSheetRows)
        testCaseCount = 0
        evidenceSheetRowLen = 30
        evidenceSheetRowIndex = 1
        for _, element in enumerate(elements):
            for perspectiveIndex, perspective in enumerate(element.getPerspectives()):
                for caseIndex, case in enumerate(perspective.getCases()):
                    testCaseCount += 1

                    # 要素名、テスト観点が同じか
                    isElementTop = perspectiveIndex == 0 and caseIndex == 0
                    isElementLast = perspectiveIndex == len(element.getPerspectives()) - 1 and caseIndex == len(perspective.getCases()) - 1
                    isPerspectiveTop = caseIndex == 0
                    isPerspectiveLast = caseIndex == len(perspective.getCases()) - 1

                    # IDセル
                    IdCell = cls.createTestCaseCell("=ROW()-1")
                    # 要素セル
                    elementCell = cls.createTestCaseCell(element.getName(), isElementTop, isElementLast)
                    # テスト観点セル
                    perspectiveCell = cls.createTestCaseCell(
                        perspective.getName(),
                        isPerspectiveTop,
                        isPerspectiveLast,
                        list(testConfig.getPerspectives().keys())
                    )
                    # テストパターンセル
                    patternCell = cls.createTestCaseCell(case.getPattern())

                    # 手順セル
                    procedures = ['・' + procedure for procedure in case.getProcedures()]
                    procedureCell = cls.createTestCaseCell(
                        "\r\n".join(procedures + ['・結果をエビデンスシートに記載(クリックで記載場所へ)'] if case.needsEvidence else procedures),
                        wrapText  = True,
                        hyperLink = f"#エビデンス!A{evidenceSheetRowIndex}" if case.needsEvidence else None
                    )
                    if case.needsEvidence:
                        value = element.getName() + '/' + perspective.getName() + '/' + ''.join([forecast for forecast in case.getForecasts()]) + '(クリックでテストケースへ)'
                        evidenceSheetRows.append([ExcelSheetCell(
                            value,
                            hyperLink = f"#テストケース!E{testCaseCount + headerLen}"
                        )])

                        for _ in range(evidenceSheetRowLen - 1):
                            evidenceSheetRows.append([])
                        evidenceSheetRowIndex = evidenceSheetRowIndex + evidenceSheetRowLen

                    # 想定結果セル
                    forecastCell = cls.createTestCaseCell(
                        "\r\n".join(['・' + forecast for forecast in case.getForecasts()]),
                        wrapText = True
                    )
                    # 実施結果、実施日、実施者、備考セル
                    resultCell = cls.createTestCaseCell(validationData = ["○", "×", "-"])
                    dateCell = cls.createTestCaseCell()
                    personCell = cls.createTestCaseCell()
                    remarkCell = cls.createTestCaseCell()

                    testCaseSheetRows.append([
                        IdCell,
                        elementCell,
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
        widths = [5, 16, 18, 16, 46, 40, 11, 9, 9, 40]

        return [
            ExcelSheet(
                "テストケース",
                testCaseSheetRows,
                widths,
                ExcelSheetAutoFilter('A1:J1')
            ),
            ExcelSheet("エビデンス", evidenceSheetRows)
        ]

    @classmethod
    def createTestCaseSheetHeaderCells(cls):
        headerValues = [
            "ID",
            "要素名",
            "テスト観点",
            "テストパターン",
            "手順",
            "想定結果",
            "実施結果\n{環境名}",
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
                ExcelSheetCellAlignment('top', wrapText = True)
            )
            cell = ExcelSheetCell(value, cellStyle)
            headerCells.append(cell)
        return headerCells

    @classmethod
    def createTestCaseCell(cls, value = "", isTop = True, isBottom = True, validationData = None, fontColor = '000000', wrapText = False, hyperLink=None):
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
                ExcelSheetCellFont(fontColor) if isTop else ExcelSheetCellFont('ffffff'),
            ),
            validationData,
            hyperLink
        )

    @classmethod
    def toExcel(cls, testBlock, testConfig):
        testBlockName = testBlock.getName()

        sheets = [
            cls.createStatusSheet()
        ]

        if testBlock.hasImage():
            image = ExcelSheetImage(
                testBlock.getImage().getPath(),
                testBlock.getImage().getWidth(),
                testBlock.getImage().getHeight()
            )
            sheets.append(ExcelSheet("画面イメージ", images=[image]))

        sheets.append(cls.createPreparationSheet(testBlock.getPreparation()))
        sheets = sheets + cls.createTestCaseAndEvidenceSheet(testBlock, testConfig)
        sheets.append(cls.createPerspectiveSheet(testConfig))

        return Excel(
            f"結合テスト仕様書_{testBlockName}.xlsx",
            sheets
        )
