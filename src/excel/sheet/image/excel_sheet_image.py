class ExcelSheetImage():
    def __init__(self, path, width, height, rowIndex=0, columnIndex=1) -> None:
        self.path = path
        self.width = width
        self.height = height
        self.rowIndex = rowIndex
        self.columnIndex = columnIndex

    def getColumnIndex(self):
        return self.columnIndex

    def getHeight(self):
        return self.height

    def getPath(self):
        return self.path

    def getRowIndex(self):
        return self.rowIndex

    def getWidth(self):
        return self.width
