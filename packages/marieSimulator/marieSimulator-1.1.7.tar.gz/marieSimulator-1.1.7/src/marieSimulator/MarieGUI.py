import sys
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QToolBar, QPushButton, QStatusBar, QFileDialog, QTableWidgetItem, QTableWidget, QAbstractItemView, QHeaderView
from PySide6.QtGui import QAction, QDesktopServices

from .Marie import Marie
from .MarieReader import MarieReader

app = QApplication(sys.argv)

class MarieGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setup
        self.setWindowTitle("Marie Simulator")
        self.setFixedSize(800, 600)

        # Variables
        self.filename = None
        self.M = []
        self.symbolTable = {}

        # Marie Variables
        self.marie = None
        self.marieReader = None

        # Widgets
        self.programTableWidget = None
        self.symbolTableWidget = None
        self.registerTableWidget = None
        self.memoryTableWidget = None

        # Define GUI
        self.setup()
    
    
    def setup(self):

        self.setupToolBarAndMenuBar()

        self.programTableWidget = QTableWidget()
        self.programTableWidget.setFixedSize(270, 250)
        self.programTableWidget.setStatusTip("Program Table")
        self.programTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.programTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.symbolTableWidget = QTableWidget()
        self.symbolTableWidget.setFixedSize(220, 250)
        self.symbolTableWidget.setStatusTip("Symbol Table")
        self.symbolTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.symbolTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.registerTableWidget = QTableWidget(7, 1, self)
        self.registerTableWidget.setStatusTip("Register Table")
        self.registerTableWidget.setHorizontalHeaderLabels(["Register", "Value"])
        self.registerTableWidget.setVerticalHeaderLabels(["AC", "PC", "MAR", "MBR", "IR", "InReg", "OutReg"])
        self.registerTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.registerTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.updateRegisterTableWidget()

        self.memoryTableWidget = QTableWidget(self)
        self.memoryTableWidget.setStatusTip("Memory Table")
        self.updateMemoryTableWidget()
    
        grid = QGridLayout()
        grid.addWidget(self.programTableWidget, 0, 0, 1, 1)
        grid.addWidget(self.symbolTableWidget, 0, 1, 1, 1)
        grid.addWidget(self.registerTableWidget, 0, 2, 1, 1)
        grid.addWidget(self.memoryTableWidget, 1, 0, 1, 3)
        container = QWidget()
        container.setLayout(grid)
        self.setCentralWidget(container)

    def setupToolBarAndMenuBar(self):
        toolbar = QToolBar(self)
        statusbar = QStatusBar(self)
        menu = self.menuBar()

        runButton = QPushButton("Run", self)
        stepButton = QPushButton("Step", self)
        resetButton = QPushButton("Reset", self)
        runButton.setStatusTip("Run the program")
        stepButton.setStatusTip("Step through the program - Disabled")
        resetButton.setStatusTip("Reset the Registers and Keeps the Memory")
        runButton.clicked.connect(self.guiRun)
        stepButton.clicked.connect(self.guiStep)
        resetButton.clicked.connect(self.guiReset)
        toolbar.addWidget(runButton)
        toolbar.addWidget(stepButton)
        toolbar.addWidget(resetButton)

        self.addToolBar(toolbar)
        self.setStatusBar(statusbar)

        def loadFunc():
            fileDialog = QFileDialog()
            fileDialog.setFileMode(QFileDialog.ExistingFile)
            self.fileName = fileDialog.getOpenFileName(self, "Open File", "")[0]
            reloadFunc()
        
        def reloadFunc():
            self.marieReader = MarieReader(self.fileName)
            self.marie = Marie(self.marieReader)

            self.M = self.marie.M[:]
            self.symbolTable = self.marie.symbolTable.copy()

            self.updateRegisterTableWidget()
            self.updateProgramTableWidget()
            self.updateSymbolTableWidget()
            self.updateMemoryTableWidget()

        def quitFunc():
            sys.exit(self.close())
        
        def editFunc():
            pass
        
        def saveFunc():
            pass
        
        def helpFunc():
            QDesktopServices.openUrl(QtCore.QUrl("https://github.com/dehadeaaryan/MarieSimulator/issues"))
        
        def aboutFunc():
            QDesktopServices.openUrl(QtCore.QUrl("https://github.com/dehadeaaryan/MarieSimulator/blob/main/README.md"))

        fileMenu = menu.addMenu("&File")
        fileLoad = QAction("&Load", self, shortcut="Ctrl+O")
        fileReload = QAction("&Reload", self, shortcut="Ctrl+R")
        fileClose = QAction("&Close", self)
        fileLoad.triggered.connect(loadFunc)
        fileReload.triggered.connect(reloadFunc)
        fileClose.triggered.connect(quitFunc)
        fileMenu.addActions([fileLoad, fileReload, fileClose])

        editMenu = menu.addMenu("&Edit")
        editEdit = QAction("&Edit", self)
        editSave = QAction("&Save", self)
        editEdit.triggered.connect(editFunc)
        editSave.triggered.connect(saveFunc)
        editMenu.addActions([editEdit, editSave])

        helpMenu = menu.addMenu("&Help")
        helpHelp = QAction("&Help", self)
        helpAbout = QAction("&More", self)
        helpHelp.setStatusTip("Open help")
        helpAbout.setStatusTip("About the application")
        helpHelp.triggered.connect(helpFunc)
        helpAbout.triggered.connect(aboutFunc)
        helpMenu.addActions([helpHelp, helpAbout])



    def updateProgramTableWidget(self):
        programLines = [i.split() for i in self.marieReader.input]
        self.programTableWidget.setRowCount(len(programLines))
        self.programTableWidget.setColumnCount(4)
        self.programTableWidget.setHorizontalHeaderLabels(["Label", "Opcode", "Address", "HEX"])
        self.programTableWidget.setVerticalHeaderLabels([hex(i)[2:].zfill(3).upper() for i in range(len(programLines))])
        for i in range(len(programLines)):
            ele = programLines[i]
            if ele[0][-1] != ",":
                programLines[i].insert(0, " ")
            if len(ele) == 2:
                programLines[i].insert(2, "000")
            self.programTableWidget.setItem(i, 0, QTableWidgetItem(str(programLines[i][0])))
            self.programTableWidget.setItem(i, 1, QTableWidgetItem(str(programLines[i][1])))
            self.programTableWidget.setItem(i, 2, QTableWidgetItem(str(programLines[i][2])))
            self.programTableWidget.setItem(i, 3, QTableWidgetItem(hex(self.M[i])[2:].zfill(4).upper()))

    def updateSymbolTableWidget(self):
        self.symbolTableWidget.setRowCount(len(self.symbolTable))
        self.symbolTableWidget.setColumnCount(2)
        self.symbolTableWidget.setHorizontalHeaderLabels(["Label", "Address"])
        self.symbolTableWidget.setVerticalHeaderLabels([str(i) for i in range(len(self.symbolTable))])
        for i, (label, address) in enumerate(self.symbolTable.items()):
            self.symbolTableWidget.setItem(i, 0, QTableWidgetItem(label))
            self.symbolTableWidget.setItem(i, 1, QTableWidgetItem(hex(address)[2:].zfill(3).upper()))
    
    def updateRegisterTableWidget(self):
        if self.marie == None:
            self.AC = 0
            self.PC = 0
            self.MAR = 0
            self.MBR = 0
            self.IR = 0
            self.InReg = 0
            self.OutReg =  0

            temp = [self.AC, self.PC, self.MAR, self.MBR, self.IR, self.InReg, self.OutReg]
            for i in range(7):
                self.registerTableWidget.setItem(i, 0, QTableWidgetItem(hex(temp[i])[2:].zfill(4).upper()))

        else:
            self.AC = self.marie.AC
            self.PC = self.marie.PC
            self.MAR = self.marie.MAR
            self.MBR = self.marie.MBR
            self.IR = self.marie.IR
            self.InReg = self.marie.InReg
            self.OutReg =  self.marie.OutReg
            self.M = self.marie.M

            temp = [self.AC, self.PC, self.MAR, self.MBR, self.IR, self.InReg, self.OutReg]
            for i in range(7):
                self.registerTableWidget.setItem(i, 0, QTableWidgetItem(hex(temp[i])[2:].zfill(4).upper()))
            
            self.updateMemoryTableWidget()

    def updateMemoryTableWidget(self):
        self.memoryTableWidget.setRowCount(16**2)
        self.memoryTableWidget.setColumnCount(16)
        self.memoryTableWidget.setVerticalHeaderLabels([(hex(i)[2:].zfill(2) + "0").upper() for i in range(16**2)])
        self.memoryTableWidget.setHorizontalHeaderLabels([("+" + hex(i)[2:].zfill(1)).upper() for i in range(16)])
        self.memoryTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.memoryTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.memoryTableWidget.setAlternatingRowColors(True)
        self.M = self.marie.M if self.marie != None else self.M
        self.M += [0] * (16**3 - len(self.M))
        for i in range(16**2):
            for j in range(16):
                self.memoryTableWidget.setItem(i, j, QTableWidgetItem(hex(self.M[i*16+j])[2:].zfill(4).upper()))



    def guiRun(self):
        self.AC = self.marie.AC
        self.PC = self.marie.PC
        self.MAR = self.marie.MAR
        self.MBR = self.marie.MBR
        self.IR = self.marie.IR
        self.InReg = self.marie.InReg
        self.OutReg =  self.marie.OutReg
        self.M = self.marie.M[:]
        self.marie.run()
        self.updateRegisterTableWidget()

    def guiStep(self):
        pass
    
    def guiReset(self):
        self.marie = None
        self.updateRegisterTableWidget()
        self.updateMemoryTableWidget()
        self.marie = Marie(self.marieReader)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MarieGUI()
    window.show()

    sys.exit(app.exec())