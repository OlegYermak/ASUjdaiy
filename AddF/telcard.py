from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(500, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("AddF/Photos/2(ico).ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        widget.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(widget)
        self.label.setGeometry(QtCore.QRect(10, -90, 471, 271))
        font = QtGui.QFont()
        font.setFamily("Modern No. 20")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(widget)
        self.label_2.setGeometry(QtCore.QRect(0, 80, 501, 150))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("AddF/Photos/tel.png"))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(widget)
        self.label_3.setGeometry(QtCore.QRect(130, 240, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "Технічна підтримка"))
        self.label.setText(_translate("widget", "Якщо у вас виникли проблеми з програмою, є загальні зауваження або побажання щодо її покращення, звертайтеся до нашої технічної підтримки в телеграмі."))
        self.label_3.setText(_translate("widget", "@daiMeniRedky"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_widget()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
