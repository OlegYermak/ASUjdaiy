from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(500, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("AddF/Photos/2(ico).ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        widget.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(widget)
        self.label.setGeometry(QtCore.QRect(10, 0, 471, 91))
        font = QtGui.QFont()
        font.setFamily("Modern No. 20")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(widget)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 471, 91))
        font = QtGui.QFont()
        font.setFamily("Modern No. 20")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(widget)
        self.label_3.setGeometry(QtCore.QRect(158, 105, 180, 180))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("AddF/Photos/trf.png"))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "Про програму"))
        self.label.setText(_translate("widget", "\"Автоматизована система обліку втрат техніки та особового складу окупаційних військ на території України\""))
        self.label_2.setText(_translate("widget", "ver.1.0.0"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_widget()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())