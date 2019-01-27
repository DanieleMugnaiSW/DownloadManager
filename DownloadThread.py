import threading
import requests
import time
import humanize
from PyQt5.QtCore import QThread, pyqtSignal
import os

def Is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

class DownloadThread(QThread):
    donechanged = pyqtSignal(int)
    finishchanged=pyqtSignal(bool)

    def __init__(self,url,dest):
        super().__init__()
        self._event = threading.Event()
        self.thread= threading.Thread(target=self.worker)
        self.done=0
        self.url=url
        self.dest=dest
        self.name=self.getFilenameFromUrl()
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())
        self.r=self.getRequest()
        self.finished=False

    def getRequest(self):
        r = requests.get(self.url, stream=True)
        return r

    def startDownload(self):
        self.thread.start()

    def worker(self):
        i = 0

        destination=self.dest + "/" + self.getFilenameFromUrl()
        while os.path.exists(destination):
            #print("esiste già  "+destination)
            destination = self.dest + "/" + str(i)+self.getFilenameFromUrl()
            i=i+1
        #response = requests.get(self.url, stream=True)
        total_length=int(self.r.headers.get('content-length', 0))
        #TODO CONTROLLARE SE GIA PRESENTE
        dl = 0
        with open(destination,"wb") as f:

            for data in self.r.iter_content(chunk_size=4096):
                with self.pause_cond:
                    while self.paused:
                        self.pause_cond.wait()

                    dl += len(data)
                    f.write(data)
                    self.done = int(100 * dl / total_length)
                    self.donechanged.emit(self.done)
                    time.sleep(0.1)
                self.finished=True
            self.finishchanged.emit(self.finished)

        return

    def getFilenameFromUrl(self):
        filename = self.url[self.url.rfind("/") + 1:]
        return str(filename)

    def pause(self):
        self.paused = True
        # If in sleep, we acquire immediately, otherwise we wait for thread
        # to release condition. In race, worker will still see self.paused
        # and begin waiting until it's set back to False
        self.pause_cond.acquire()

    #should just resume the thread
    def resume(self):
        self.paused = False
        # Notify so thread will wake after lock released
        self.pause_cond.notify()
        # Now release the lock
        self.pause_cond.release()

    def work(self):
        if(self.paused==False):
            self.pause()
        else:
            self.resume()
    def getSize(self):
        total_length = int(self.r.headers.get('content-length', 0))
        return humanize.naturalsize(total_length)

    @staticmethod
    def Is_downloadable(url):
        """
        Does the url contain a downloadable resource
        """
        h = requests.head(url, allow_redirects=True)
        header = h.headers
        content_type = header.get('content-type')
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False
        return True



if __name__ =="__main__":
    desti='/home/daniele/Scaricati'
    url = 'https://www.promuoviweb.net/wp-content/uploads/2018/07/immagini-google-1140x445.jpg'
    downloader=DownloadThread(url,desti)
    downloader.startDownload()


