import sys
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QLabel, QPushButton, QListWidgetItem, QHBoxLayout,QProgressBar,QMainWindow,QAction,QDialog,QDesktopWidget,QFormLayout,QLineEdit,QInputDialog,QFileDialog,QDialogButtonBox
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon,QPixmap
from os.path import expanduser


class InputDialog(QDialog):

    def __init__(self, parent = None):
        super(InputDialog, self).__init__(parent)

        self.initUI()

    def initUI(self):
        #self.btn = QPushButton('URL:', self)
        #self.btn.move(20, 20)
        self.labelName=QLabel("Insert your URL: ",self)
        self.labelName.move(20,27)
#        self.btn.clicked.connect(self.showDialogUrl)

        self.le = QLineEdit(self)
        self.le.setFixedWidth(650)
        self.le.move(130, 22)

        self.btnfolder=QPushButton("Select folder...",self)
        #self.btnfolder.setIcon(QIcon("icon/folder.png"))
        self.btnfolder.move(20,80)
        self.btnfolder.clicked.connect(self.showDialogDirectory)

        self.le1=QLineEdit(self)
        self.le1.move(130,80)
        self.le1.setText(expanduser("~"))

        self.button=QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel,Qt.Horizontal,self)
        self.button.move(80,120)

        self.button.accepted.connect(self.accept)
        self.button.rejected.connect(self.reject)


        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()

    def showDialogDirectory(self):
        dest = QFileDialog.getExistingDirectory(self, "Choose dir",expanduser("~") )

        print(str(dest))
        if(str(dest)!=""):
            self.le1.setText(str(dest))



    @staticmethod
    def getInput(parent=None):
        dialog=InputDialog()
        dialog.setFixedWidth(800)
        result=dialog.exec_()
        url=dialog.le.text()
        dest=dialog.le1.text()
        return (url,dest)



if __name__ == '__main__':
    app = QApplication(sys.argv)

    url,dest=InputDialog.getInput()
    print(url,dest)




