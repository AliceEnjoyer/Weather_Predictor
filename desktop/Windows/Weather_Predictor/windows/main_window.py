from PySide6 import QtWidgets
from PySide6.QtCore import qDebug
from PySide6 import QtCore
import pyqtgraph as pg
from PySide6 import QtGui
import requests
import os
import shutil
import json
import http

#class Widget(QWidget):
#    def __init__(self, parent=None):
#        super().__init__(parent)

class Main_window(QtWidgets.QWidget):
    def __init__(self, screen, parent=None):
        super().__init__(parent)
#Auth
        checkAuth = 0
        self._token = ""
        if os.path.isfile("token.tok"):
            checkAuth = 1
            with open('token.tok', 'r') as file:
                 self._token = file.read()
        else:
            authVbl = QtWidgets.QVBoxLayout()
            authVbl.addWidget(QtWidgets.QLabel("Choose your token file:"))
            buttonChooseToken = QtWidgets.QPushButton("Pick a token...")
            authVbl.addWidget(buttonChooseToken)
            authVbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.setLayout(authVbl)

            buttonChooseToken.clicked.connect(self.slotChooseTokenButtonClicked)


#

#setup main vbl
        self._buttonCountry = QtWidgets.QPushButton()
        self._textLine = QtWidgets.QLineEdit()
        self._buttonPredict = QtWidgets.QPushButton()


        self._labelShowWeather1 = QtWidgets.QLabel("Show weather from")
        self._dateEdit1 = QtWidgets.QDateEdit(calendarPopup=True)
        self._labelShowWeather2 = QtWidgets.QLabel("to")
        self._dateEdit2 = QtWidgets.QDateEdit(calendarPopup=True)
        self._buttonSettings = QtWidgets.QPushButton()

        self._buttonArrowLeft = QtWidgets.QPushButton()
        self._plot_graph = pg.PlotWidget()
        self._buttonArrowRight = QtWidgets.QPushButton()

        self._labelPickedDate = QtWidgets.QLabel("Write something into text line")

        #self._textLine.setPlaceholderText("type a city here")
        self._dateEdit1.setDateTime(QtCore.QDateTime.currentDateTime())
        self._dateEdit2.setDateTime(QtCore.QDateTime.currentDateTime())

        self._textLine.setMinimumHeight(35)

        pm1 = QtGui.QPixmap("icons/icoEarth2.png")
        self._country = "None"
        self._buttonCountry.setIcon(QtGui.QIcon(pm1))
        self._buttonCountry.setMinimumWidth(40)
        self._buttonCountry.setMinimumHeight(40)
        pm1 = QtGui.QPixmap("icons/icoSearch.png")
        self._buttonPredict.setIcon(QtGui.QIcon(pm1))
        self._buttonPredict.setMinimumWidth(40)
        self._buttonPredict.setMinimumHeight(40)
        pm1 = QtGui.QPixmap("icons/icoSettings.png")
        self._buttonSettings.setIcon(QtGui.QIcon(pm1))
        self._buttonSettings.setMaximumWidth(35)
        pm1 = QtGui.QPixmap("icons/icoArrowRight.png")
        self._buttonArrowRight.setIcon(QtGui.QIcon(pm1))
        pm1 = QtGui.QPixmap("icons/icoArrowLeft.png")
        self._buttonArrowLeft.setIcon(QtGui.QIcon(pm1))
        self._buttonArrowRight.setMinimumHeight(70)
        self._buttonArrowLeft.setMinimumHeight(70)

        self._dateEdit1.setMinimumHeight(30)
        self._dateEdit2.setMinimumHeight(30)
        self._dateEdit1.setMinimumWidth(85)
        self._dateEdit2.setMinimumWidth(85)

        self._plot_graph.setBackground("w")




        self._mainVbl = QtWidgets.QVBoxLayout()

        self._hbl1 = QtWidgets.QHBoxLayout()
        self._hbl1.addWidget(self._buttonCountry)
        self._hbl1.addWidget(self._textLine)
        self._hbl1.addWidget(self._buttonPredict)
        self._mainVbl.addLayout(self._hbl1)

        self._hbl2 = QtWidgets.QHBoxLayout()
        self._hbl21 = QtWidgets.QHBoxLayout()
        self._hbl21.addWidget(self._labelShowWeather1)
        self._hbl21.addWidget(self._dateEdit1)
        self._hbl21.addWidget(self._labelShowWeather2)
        self._hbl21.addWidget(self._dateEdit2)
        self._hbl21.setSpacing(15)
        self._hbl2.addLayout(self._hbl21)
        self._hbl2.addWidget(self._buttonSettings)
        self._hbl21.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self._mainVbl.addLayout(self._hbl2)

        self._mainVbl.addSpacing(14)

        self._hbl3 = QtWidgets.QHBoxLayout()
        self._hbl3.addWidget(self._buttonArrowLeft)
        self._hbl3.addWidget(self._plot_graph)
        self._hbl3.addWidget(self._buttonArrowRight)
        self._mainVbl.addLayout(self._hbl3)

        self._hbl4 = QtWidgets.QHBoxLayout()
        self._hbl4.addWidget(self._labelPickedDate)
        self._hbl4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._mainVbl.addLayout(self._hbl4)

        if checkAuth == 1: self.setLayout(self._mainVbl)
#end of setup vbl

        self.setMinimumHeight(630)
        self.setObjectName("main_window")
        self.setWindowTitle("Weather Predictor")

        self._config = json.load(open("configs\dev.json"))

        self._buttonPredict.clicked.connect(self.slotPredictButtonClicked)



    def paintEvent(self, event: QtGui.QPaintEvent):
            with QtGui.QPainter(self) as p:
                rect1 = self._hbl1.geometry()
                rect2 = self._hbl2.geometry()
                temp = rect1.height()+rect1.height()*0.333

                p.setPen(QtGui.QColor("#FFC700"))
                p.setBrush(QtGui.QBrush(QtGui.QColor("#FFC700"), QtCore.Qt.SolidPattern))
                p.drawRect(0, 0, self.width(), temp)

                p.setPen(QtGui.QColor("#FFD53F"))
                p.setBrush(QtGui.QBrush(QtGui.QColor("#FFD53F"), QtCore.Qt.SolidPattern))
                p.drawRect(0, temp, self.width(), rect2.height()+rect2.height()*0.40)

    def slotChooseTokenButtonClicked(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Pick a token", "", "token.tok")

        if os.path.isfile(path[0]):
            shutil.copy(path[0], "token.tok")

            #TODO: Fix bug with unchangeable Layout
            self.setLayout(self._mainVbl)
            self.update()
            with open('token.tok', 'r') as file:
                 self._token = file.read()

    def slotPredictButtonClicked(self):
        url1 = self._config["Host"] + "/Predict/" + self._country + "-" + self._textLine.text().replace(" ", "")
        headers1={"Authorization": "Bearer " + self._token}
        self.setDisabled(1)
        #TODO: Fix checkConnection
#        if not checkConnection(self._config["Host"]):
#            self.setDisabled(0)
#            self._labelPickedDate.setText("Server is unreachable")
#            qDebug(self._config["Host"])
#            return
        response = requests.get(url=url1, headers=headers1)
        self.setDisabled(0)
        if response.status_code != 200:
            self._labelPickedDate.setText("Unauthorized")
            return

        #some vizualization stuff
        self._labelPickedDate.setText(response.json()["Data"])


def checkConnection(url="localhost", timeout=3):
    connection = http.client.HTTPConnection(url, timeout=timeout)
    try:
        connection.request("HEAD", "/")
        connection.close()
        return True
    except Exception as exep:
        return False

