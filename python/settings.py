import os
from typing import Tuple, Dict
import re
import sys
from PySide2.QtWidgets import \
    QMainWindow, QPushButton, QLineEdit, QApplication, QFormLayout, QWidget, QLabel

setting_path = './setting.cfg'
valuereg = re.compile(r'^[\w\.:/\-,;=}{[\]\\ ]+$')
settingreg = re.compile(r'^[\w]+$')
setting_regex = re.compile(r'([\w]+):\s*([\w\.:/\-,;=}{[\]\\#*+\- ]+)')


class setting_model():
    settings = {}
    settingschanged = True

    def __init__(self):
        self.settingschanged = True
        self.settings = {}
        self.loadsettings()

    def loadsettings(self) -> Dict:
        if not self.settingfileexists():
            return self.settings
        if self.settingschanged:
            self.settingschanged = False
            file = open(setting_path, "r")
            for l in file.readlines():
                if self.linefitspattern(l):
                    t = self.getvaluesfromline(l)
                    self.settings[t[0]] = t[1]

            file.close()
        self.settingschanged = False
        # print(self.settings)
        return self.settings

    def savesettings(self) -> Dict:
        if not self.didsettingschanged():
            return
        self.deletesettingfile()
        self.createsettingfile()
        file = open(setting_path, "w")
        for x in self.settings.items():
            l:str = self.getlinefromvalues(x[0], x[1])
            file.write(l)
        file.close()
        self.settingschanged = False

    def getsetting(self, set: str) -> str:
        return self.settings[set]

    def changesetting(self, setting: str, value: str) -> Dict:
        if not (self.valuefitspattern(value) and self.settingfitspattern(setting)):
            return None
        self.settings[setting] = value
        self.settingschanged = True
        return self.settings

    def delsetting(self, setting: str) -> Dict:
        del self.settings[setting]
        self.settingschanged = True

    def didsettingschanged(self) -> bool:
        return self.settingschanged == True

    def settingfileexists(self) -> bool:
        return os.path.isfile(setting_path)

    def createsettingfile(self) -> bool:
        if self.settingfileexists():
            return False
        f = open(setting_path, "x")
        f.close()
        return True

    def deletesettingfile(self) -> bool:
        if not self.settingfileexists():
            return False
        os.remove(setting_path)
        return True

    def linefitspattern(self, line: str) -> bool:
        return not setting_regex.search(line) is None

    def valuefitspattern(self, value: str) -> bool:
        return not valuereg.match(value) is None

    def settingfitspattern(self, set: str) -> bool:
        return not settingreg.match(set) is None

    def getvaluesfromline(self, line: str) -> Tuple[str, str]:
        if not self.linefitspattern(line):
            return None
        mo = setting_regex.search(line)
        return tuple((mo.groups()))

    def getlinefromvalues(self, val1: str, val2: str):
        return val1 + ":\t" + val2 + "\n"


class setting_view(QMainWindow):

    model: setting_model
    

    def __init__(self, model: setting_model):
        super(setting_view, self).__init__()
        self.layout = QFormLayout()
        self.model = model

        self.homeurlLabel = QLabel("Home Url: ")
        self.homeurlLineEdit = QLineEdit()
        self.homeurlLineEdit.setText(self.model.getsetting("homeurl"))
        self.layout.addRow(self.homeurlLabel, self.homeurlLineEdit)

        for i in range(3):
            wa = QLabel(" ")
            wb = QLabel(" ")
            self.layout.addRow(wa, wb)

        self.cancelButton: QPushButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.cancel)
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.save)
        self.layout.addRow(self.cancelButton, self.saveButton)



        width = 72
        height = 30
        self.aqw = QWidget()
        self.aqw.setLayout(self.layout)
        self.setCentralWidget(self.aqw)

        self.resize(width * 3 + 50, height * 4)
        print(str(self.homeurlLabel.geometry().width()) + " " + str(self.homeurlLabel.geometry().height()))

    def cancel(self):
        self.close()

    def save(self):
        self.model.changesetting("homeurl", self.homeurlLineEdit.text())
        self.model.savesettings()
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    sm = setting_model()
    sv = setting_view(sm)
    sys.exit(app.exec_())
