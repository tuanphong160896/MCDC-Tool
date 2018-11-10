import Core as Core
import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, QLabel

class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'MCDC Test Cases Support Tool - Version 2.0'
        self.setWindowIcon(QtGui.QIcon('github.ico'))
        self.left = 100
        self.top = 100
        self.width = 560
        self.height = 300
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #create Menu
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')
        # mainMenu.setStyleSheet("\
        #     border: 0px solid #2475D6")

        # Create label
        instruction_text = '1. Each condition should be put in a bracket.\n\n2. Copy your expression to the textbox.\n\n3. Click Create .xlsx file then Open to see report.'
        self.label = QLabel(instruction_text, self)
        self.label.setFont(QtGui.QFont('MS San Serif', 9))
        self.label.move(20,95)              #(widht, height)
        self.label.setAlignment(Qt.AlignLeft)
        self.label.adjustSize()

        copyright_text = 'COPYRIGHT © 2018 BY D.T.P'
        self.copyright = QLabel(copyright_text, self)
        self.copyright.setFont(QtGui.QFont('MS San Serif', 8))
        self.copyright.move(202,277)              #(widht, height)
        self.copyright.setAlignment(Qt.AlignCenter)
        self.copyright.adjustSize()

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 180)
        self.textbox.resize(315,40)
 
        # Create button in the window
        self.button = QPushButton('Create .xlsx file', self)
        self.button.move(20,235)
        # self.button.setStyleSheet("\
        #     border: 2px solid #2475D6")
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)

        # Open button in the window
        self.button_open = QPushButton('Open', self)
        self.button_open.move(140,235)
        # self.button_open.setStyleSheet("\
        #     border: 2px solid #2475D6")
        self.button_open.resize(50,30)
        self.button_open.clicked.connect(self.open_on_click)
        self.button_open.setEnabled(False)
        
        
        # insert BOSCH logo
        self.lb = QLabel(self)
        self.lb.pic = QtGui.QPixmap('bosch.png')
        self.lb.setPixmap(self.lb.pic)
        #self.lb.resize((self.lb.pic.width())/32, (self.lb.pic.height())/32)
        self.lb.adjustSize()
        self.lb.move(20,35)
        self.lb.show()

        #insert PYTHON logo
        self.lb_python_logo = QLabel(self)
        self.lb_python_logo.pic = QtGui.QPixmap('python_logo.png')
        self.lb_python_logo.setPixmap(self.lb_python_logo.pic)

        self.lb_python_logo.adjustSize()
        self.lb_python_logo.move(370,75)
        self.lb_python_logo.show()

        # #Bài thơ củ chuối
        # text = 'Hỏi thế gian tình là chi\nMà dôi lứa nguyện thề sống chết\nNam Bắc hai đàng rồi ly biệt\nMưa dầm dãi nắng hai ngã quan san'
        # self.tho_cu_chuoi = QLabel(text, self)
        # self.tho_cu_chuoi.setFont(QtGui.QFont('MS San Serif', 7, italic = 1))
        # self.tho_cu_chuoi.setStyleSheet("QLabel {color : #414141}")
        # self.tho_cu_chuoi.move(375,129)              #(widht, height)
        # self.tho_cu_chuoi.setAlignment(Qt.AlignCenter)
        # self.tho_cu_chuoi.adjustSize()

        self.move(380,200)
        self.show()    
 
    #@pyqtSlot()
    def on_click(self):
        try:
            self.button_open.setEnabled(False)
            textboxValue = self.textbox.text()
            if not (str(textboxValue) == ''):
                Core.preProcessing(str(textboxValue))
                QMessageBox.warning(self, 'MCDC Tool', "DONE ! Check your .xlsx file.")
            else:
                QMessageBox.warning(self, 'MCDC Tool', "Please input expression !")
            self.button_open.setEnabled(True)

        except Exception as e:
            QMessageBox.warning(self, 'MCDC Tool', "Error occured: " + str(e))

    def open_on_click(self):
        try:
            Core.Open_latest_file()
        except Exception as e:
            QMessageBox.warning(self, 'MCDC Tool', "Error occured: " + str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())