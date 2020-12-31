
import sys
from PySide2.QtCore import QUrl
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QApplication, QLineEdit,
    QMainWindow, QPushButton, QToolBar, QVBoxLayout)

from PySide2.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from settings import setting_view, setting_model


class MainWindow(QMainWindow):

    settingdialog = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.smodel = setting_model()
        if not self.smodel.settingfileexists():
            self.smodel.createsettingfile()
        self.smodel.loadsettings()
        self.setWindowTitle('PySide2 WebEngineWidgets Example')
        def iconpath(x: str): return '../icons/' + x + '_16.png'

        self.toolBar = QToolBar()
        self.addToolBar(self.toolBar)

        self.homeButton = QPushButton()
        self.homeButton.setIcon(QIcon(iconpath('home')))
        self.homeButton.clicked.connect(self.goHome)
        self.toolBar.addWidget(self.homeButton)

        self.backButton = QPushButton()
        self.backButton.setIcon(QIcon(iconpath('back')))
        self.backButton.clicked.connect(self.back)
        self.toolBar.addWidget(self.backButton)

        self.forwardButton = QPushButton()
        self.forwardButton.setIcon(QIcon(iconpath('forward')))
        self.forwardButton.clicked.connect(self.forward)
        self.toolBar.addWidget(self.forwardButton)

        self.addressLineEdit = QLineEdit()
        self.addressLineEdit.returnPressed.connect(self.load)
        self.toolBar.addWidget(self.addressLineEdit)

        self.reloadButton = QPushButton()
        self.reloadButton.setIcon(QIcon(iconpath('sync')))
        self.reloadButton.clicked.connect(self.reload)
        self.toolBar.addWidget(self.reloadButton)

        self.settingsButton = QPushButton()
        self.settingsButton.setIcon(QIcon(iconpath('settings')))
        self.settingsButton.clicked.connect(self.openSettings)
        self.toolBar.addWidget(self.settingsButton)

        self.webEngineView = QWebEngineView()
        self.setCentralWidget(self.webEngineView)

        self.webEngineView.page().titleChanged.connect(self.setWindowTitle)
        self.webEngineView.page().urlChanged.connect(self.urlChanged)

        self.setting_dialogs = list()
        self.layouts = QVBoxLayout()
        self.setLayout(self.layouts)

        self.goHome()

    def load(self):
        url = QUrl.fromUserInput(self.addressLineEdit.text())
        if url.isValid():
            self.webEngineView.load(url)

    def back(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Back)

    def forward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Forward)

    def reload(self):
        url = self.webEngineView.url()
        self.addressLineEdit.setText(QUrl.toString(url))
        if url.isValid():
            self.webEngineView.load(url)

    def urlChanged(self, url):
        self.addressLineEdit.setText(url.toString())

    def goHome(self):
        self.addressLineEdit.setText(self.smodel.getsetting('homeurl'))
        self.load()

    def openSettings(self):
        sv = setting_view(self.smodel)
        self.settingdialog = sv
        sv.show()
        self.setting = list()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    availableGeometry = app.desktop().availableGeometry(mainWin)
    mainWin.resize(availableGeometry.width(), availableGeometry.height())
    mainWin.show()
    sys.exit(app.exec_())
