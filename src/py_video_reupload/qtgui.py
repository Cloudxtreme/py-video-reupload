import sys
from PyQt4 import QtGui

""" QT4 frontend for py-video-reupload """

class ProgressBar(QtGui.QWidget):
    def __init__(self, parent=None, total=20):
        super(ProgressBar, self).__init__(parent)
        self.name_line = QtGui.QLineEdit()

        self.progressbar = QtGui.QProgressBar()
        self.progressbar.setMinimum(1)
        self.progressbar.setMaximum(total)

        main_layout = QtGui.QGridLayout()
        main_layout.addWidget(self.progressbar, 0, 0)

        self.setLayout(main_layout)
        self.setWindowTitle("Progress")

    def update_progressbar(self, val):
        self.progressbar.setValue(val)   
        
class mainWidget(QtGui.QWidget):
    def __init__(self, app):
        self.app = app
        
        super(mainWidget, self).__init__()
        self.initUI()
    
    def downloadButtonPressed(self):
        info = self.app.getVideoInfo(self.urlEdit.text())
        
        if not info == None:
            self.showDescription()
            self.urlEdit.setEnabled(False)
            
            if not info['meta'] == None:
                self.titleEdit.setText(info['meta']['title'])
                self.descriptionEdit.setText(info['meta']['description'])
                
            self.app.hooks['downloadCheck'] = self.updateProgress
            self.app.startDownload(info)
            
    def updateProgress(self, downloaded, total):
        """ Update progress bars """
        
        if self.app.state == "downloaded":
            self.uploadButton.show()

        if self.app.state == "uploading":
            self.downloadBarTitle.setText("Uploading: "+downloaded+"%")
            self.downloadBar.hide()
        else:
            self.downloadBar.update_progressbar(((int(downloaded)*100)/int(total)))
        
        if int(downloaded) == int(total):
            self.downloadBar.update_progressbar(100)
        
    def uploadButtonPressed(self):
        self.app.startUpload()
        self.uploadButton.hide()
        
    def initUI(self):
        """ Main window GUI """
    
        self.url = QtGui.QLabel('URL')
        self.title = QtGui.QLabel('Title')
        self.description = QtGui.QLabel('Description')
        
        # buttons
        self.downloadButton = QtGui.QPushButton("Submit")
        self.downloadButton.clicked.connect(self.downloadButtonPressed)
        
        self.uploadButton = QtGui.QPushButton("Upload")
        self.uploadButton.clicked.connect(self.uploadButtonPressed)
        
        self.urlEdit = QtGui.QLineEdit()
        self.titleEdit = QtGui.QLineEdit()
        self.descriptionEdit = QtGui.QTextEdit()
        
        self.downloadBarTitle = QtGui.QLabel('Download')
        self.downloadBar = ProgressBar(total=101)
        self.progressText = QtGui.QLabel('500/600 bytes')
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(self.url, 1, 0)
        grid.addWidget(self.urlEdit, 1, 1)
        
        # additional fields
        grid.addWidget(self.title, 2, 0)
        grid.addWidget(self.titleEdit, 2, 1)
        
        grid.addWidget(self.description, 3, 0)
        grid.addWidget(self.descriptionEdit, 3, 1)
        
        # progress bars'
        grid.addWidget(self.downloadBarTitle, 4, 0)
        grid.addWidget(self.downloadBar, 4, 1)
        grid.addWidget(self.progressText, 5, 1)
        grid.addWidget(self.uploadButton, 5, 1)
        
        # buttons
        grid.addWidget(self.downloadButton, 1, 2)
        
        self.setLayout(grid) 
        
        self.setGeometry(200, 300, 350, 300)
        self.resize(350, 20)
        self.setWindowTitle('Re-upload a video')  
        self.show()
        
        # default layout
        self.showLinkSelection()

    def showLinkSelection(self):
        self.downloadBar.hide()
        self.downloadBarTitle.hide()
        self.title.hide()
        self.titleEdit.hide()
        self.description.hide()
        self.descriptionEdit.hide()
        self.progressText.hide()
        self.uploadButton.hide()
        
        self.downloadButton.show()
        
    def showDescription(self):
        self.downloadBar.show()
        self.downloadBarTitle.show()
        self.title.show()
        self.titleEdit.show()
        self.description.show()
        self.descriptionEdit.show()
        #self.progressText.show()
        
        self.downloadButton.hide()
        
        
        
def main(mainApp):
    app = QtGui.QApplication(sys.argv)
    app.aboutToQuit.connect(mainApp.exit)
    w = mainWidget(mainApp)
    sys.exit(app.exec_())
