import sys
from PyQt5.QtWidgets import QApplication,QDialogButtonBox,QWidget,QListWidget, QVBoxLayout, QLabel, QPushButton, QListWidgetItem, QHBoxLayout,QProgressBar,QMainWindow,QAction,QDialog,QDesktopWidget
from PyQt5.QtCore import QRect,QSize
from PyQt5.QtGui import QPixmap, QIcon, QBrush,QKeySequence,QColor,QFont


class CustomQWidget(QWidget):
    def __init__(self,name, parent=None):
        super(CustomQWidget, self).__init__(parent)
        self.name=name
        self.labelName = QLabel()
        self.labelName.setFont(QFont('SansSerif',10))
        self.labelName.setFixedWidth(220)
        self.dim = QLabel()
        self.dim.setFixedWidth(80)
        self.progress = QProgressBar()
        self.progress.setStyleSheet(open('style.css').read())
        self.progress.setFixedWidth(250)
        self.progress.setRange(0,100)
        self.buttonPauseResume=QPushButton()
        self.buttonPauseResume.setIcon(QIcon("icon/pause.png"))
        self.buttonPauseResume.setFixedWidth(40)
        self.buttonDelete=QPushButton()
        self.buttonDelete.setIcon(QIcon("icon/delete.png"))
        self.buttonDelete.setFixedWidth(40)

        layout = QHBoxLayout()
        layout.addWidget(self.labelName)
        layout.addWidget(self.dim)

        layout.addWidget(self.progress)

        layout.addWidget(self.buttonPauseResume)
        layout.addWidget((self.buttonDelete))
        self.setLayout(layout)
    def finish(self):
        self.labelName.setStyleSheet('QLabel {text-decoration: line-through}')
class InputDialog(QDialog):
    def __init__(self,parent=None):
        super(InputDialog,self).__init__(parent)


class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Download Manager")
        self.setFixedWidth(800)
        self.setFixedHeight(600)
        self.tb = self.addToolBar("edit")
        self.addDownload = QAction(QIcon("icon/add.png"), "Add Download", self)
        self.pauseDownload=QAction(QIcon("icon/pause.png"),"Pause all Download",self)
        self.resumeDownload=QAction(QIcon("icon/resume.png"),"Resume all download",self)
        self.deleteDownload=QAction(QIcon("icon/delete.png"),"Delete all download",self)

        self.list = QListWidget(self)

        self.setCentralWidget(self.list)
