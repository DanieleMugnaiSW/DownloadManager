# DownloadManager
Simple Usefull Download Manager


## Introduction 
A simple and useful download manager application written in Python.
The core uses Python Request Module  for downloading files and Threading module for managing more downloading process.
The user interface is created using PyQt5.


## ScreenShoot

### Input
The Download allow to start a download from a valid url and select the folder where download. If the url is not valid it send you a message; if the folder destination doesn’t exist it will download in a default directory

### Main Windows

At the top there is toolbar that permits to Create a New Download, Pause all download, Delete All download.
After creating a download, a item is added: each item has a name(the file), the size, a progress bar and two button the permits to pause and delete the selected download. 

NB: **Before push the button of each item, select the item.**

When a download is finish is name is ~~Strikethrough~~

 

## Requirements
- Pyhton 
- Pyqt5
- Threading
- Request
- Humanize
