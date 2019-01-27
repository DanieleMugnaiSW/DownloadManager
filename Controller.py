from View import *
import requests
#from Downloader import *
from DownloadThread import *
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit,QFileDialog,QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap, QIcon, QBrush,QKeySequence,QColor,QFont

import sys
from inputdialog import *
class Controller:

    def __init__(self):

        self.view=MyWindow()
        self.downloaders=[]


        #TOOLBAR

        #ADD
        self.view.addDownload.triggered.connect(self.createDownload)
        self.view.tb.addAction(self.view.addDownload)



        #PAUSE ALL
        self.view.pauseDownload.triggered.connect(self.pauseAllDownload)
        self.view.tb.addAction(self.view.pauseDownload)

        #RESUME ALL
        self.view.resumeDownload.triggered.connect(self.resumeAllDownload)
        self.view.tb.addAction(self.view.resumeDownload)

        #DELETE ALL
        self.view.deleteDownload.triggered.connect(self.removeAllDownload)
        self.view.tb.addAction(self.view.deleteDownload)



    def createDownload(self):

        try:
            url, dest = InputDialog.getInput()
            newThread=DownloadThread(url,dest)

        except requests.exceptions.MissingSchema:
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setText("Invalid URL")
            msg.setFixedHeight(100)
            msg.setFixedWidth(200)
            msg.exec_()
        else:
            item = QListWidgetItem(self.view.list)
            item_widget = CustomQWidget(newThread.name)
            item_widget.buttonPauseResume.clicked.connect(self.pauseResumeDownload)
            item_widget.buttonDelete.clicked.connect(self.removeDownload)
            item_widget.labelName.setText(newThread.getFilenameFromUrl())
            item_widget.dim.setText(str(newThread.getSize()))
            item.setSizeHint(item_widget.sizeHint())
            self.view.list.addItem(item)
            self.view.list.setItemWidget(item, item_widget)
            newThread.donechanged.connect(item_widget.progress.setValue)
            newThread.finishchanged.connect(item_widget.finish)
            newThread.startDownload()
            self.downloaders.append(newThread)
    def pauseResumeDownload(self):
        for i in self.downloaders:
            for item in self.view.list.selectedItems():
                if self.view.list.itemWidget(item).name==i.name:
                    i.work()
                    if(i.paused==True):
                        self.view.list.itemWidget(item).buttonPauseResume.setIcon(QIcon("icon/resume.png"))
                    else:
                        self.view.list.itemWidget(item).buttonPauseResume.setIcon(QIcon("icon/pause.png"))

    def removeDownload(self):


        for i in self.downloaders:
            for item in self.view.list.selectedItems():
               if self.view.list.itemWidget(item).name == i.name:

                    if (i.paused == False):
                        i.pause()
        reply=QMessageBox.question(self.view,"Continue?","Your are going to delete; if the download is not finished, the file will be LOST.",QMessageBox.Yes,QMessageBox.No)
        if(reply==QMessageBox.Yes):
            for i in self.downloaders:
                for item in self.view.list.selectedItems():
                    if self.view.list.itemWidget(item).name==i.name:
                        self.downloaders.remove(i)
                        self.view.list.takeItem(self.view.list.row(item))
        else:
            for i in self.downloaders:
                i.resume()


    def pauseAllDownload(self):
        for i in self.downloaders:
            if i.paused==False:
                i.pause()
        self.view.pauseDownload.setEnabled(False)
        self.view.resumeDownload.setEnabled(True)


    def resumeAllDownload(self):

        for i in self.downloaders:
            if i.paused==True:
                i.resume()
        self.view.resumeDownload.setEnabled(False)
        self.view.pauseDownload.setEnabled(True)



    def removeAllDownload(self):
        if len(self.downloaders)!=0:
            for i in self.downloaders:
                if i.paused == False:
                    i.pause()
            reply = QMessageBox.question(self.view, "Continue?", "You are going to delete all the download; the unfinished downloads will be lost", QMessageBox.Yes, QMessageBox.No)
            if (reply == QMessageBox.Yes):
                self.view.list.clear()
                del self.downloaders[:]
            else:
                for i in self.downloaders:
                    i.resume()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    contr=Controller()
    contr.view.show()
sys.exit(app.exec_())







