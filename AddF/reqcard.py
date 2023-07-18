from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(500, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("AddF/Photos/2(ico).ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        widget.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(widget)
        self.label.setGeometry(QtCore.QRect(-70, -20, 471, 91))
        font = QtGui.QFont()
        font.setFamily("Modern No. 20")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(widget)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 471, 121))
        font = QtGui.QFont()
        font.setFamily("Modern No. 20")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "Про програму"))
        self.label.setText(_translate("widget", "Вимоги для використання програми:"))
        self.label_2.setText(_translate("widget", "-обов\'язкове з\'єднання з інтернетом для оновлення даних;    -512 мб оперативної пам\'яті;                                                                     -передвстановлені бібліотеки Python згідно зі списком в файлі Readme."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_widget()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
