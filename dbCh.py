from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

import datetime
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

DB_NAME = 'damage.db'

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(490, 280)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(70, -10, 361, 81))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(17)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(20, 120, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(60, 190, 170, 70))
        self.pushButton1 = QtWidgets.QPushButton(Form)
        self.pushButton1.setGeometry(QtCore.QRect(270, 190, 170, 70))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(110, 79, 351, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(Form)
        self.textEdit_2.setGeometry(QtCore.QRect(110, 120, 351, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.pushButton.clicked.connect(lambda: self.check_db_adm(Form))
        self.pushButton1.clicked.connect(lambda: self.check_db_user(Form))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Редагування облікових записів"))
        self.label.setText(_translate("Form", "Введіть дані користувача:"))
        self.label_2.setText(_translate("Form", " Логін:"))
        self.label_3.setText(_translate("Form", "Пароль:"))
        self.pushButton.setText(_translate("Form", "Додати/видалити \nдані(адмін)"))
        self.pushButton1.setText(_translate("Form", "Додати/видалити \nдані(користувач)"))
    
    def vigenere_encrypt(self, plaintext):
        key = "Key"
        padded_key = key.ljust(32)[:32]  # Призначення ключа AES довжиною 32 байти (256 біт)
        backend = default_backend()
        cipher = Cipher(algorithms.AES(padded_key.encode()), modes.ECB(), backend=backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return ciphertext.hex()

    def vigenere_decrypt(self, ciphertext):
        key = "Key"
        padded_key = key.ljust(32)[:32]  # Призначення ключа AES довжиною 32 байти (256 біт)
        backend = default_backend()
        cipher = Cipher(algorithms.AES(padded_key.encode()), modes.ECB(), backend=backend)
        decryptor = cipher.decryptor()
        decrypted_text = decryptor.update(bytes.fromhex(ciphertext)) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(decrypted_text) + unpadder.finalize()
        return plaintext.decode()
    
    def check_db_adm(self,Form):
        login = self.textEdit.toPlainText()
        password = self.textEdit_2.toPlainText()
        
        encrypted_login = self.vigenere_encrypt(login)
        encrypted_password = self.vigenere_encrypt(password)
        
        file_path = "enters.txt"
        
        c.execute("SELECT passAdm FROM admAccs WHERE logAdm = ?", (encrypted_login,))
        enLog=c.fetchone()
        c.execute("SELECT logAdm FROM admAccs WHERE passAdm = ?", (encrypted_password,))
        enPass=c.fetchone()
        if  enLog==None and enPass==None:
            c.execute(f"INSERT INTO admAccs (logAdm, passAdm) VALUES ('{encrypted_login}', '{encrypted_password}')")
            db.commit()
                      
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not os.path.exists(file_path):
                open(file_path, "w").close()
            with open(file_path, "a") as file:
                file.write("Created admin " + login + " " + current_datetime + "\n")        
        else: 
            c.execute(f"DELETE FROM admAccs WHERE logAdm='{encrypted_login}' AND passAdm='{encrypted_password}'")
            db.commit()
            
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not os.path.exists(file_path):
                open(file_path, "w").close()
            with open(file_path, "a") as file:
                file.write("Deleted admin " + login + " " + current_datetime + "\n")
            
    def check_db_user(self,Form):
        login = self.textEdit.toPlainText()
        password = self.textEdit_2.toPlainText()
        
        encrypted_login = self.vigenere_encrypt(login)
        encrypted_password = self.vigenere_encrypt(password)
        
        file_path = "enters.txt"
        
        c.execute("SELECT passUser FROM userAccs WHERE logUser = ?", (encrypted_login,))
        enLogUs=c.fetchone()
        c.execute("SELECT logUser FROM userAccs WHERE passUser = ?", (encrypted_password,))
        enPassUs=c.fetchone()
        if  enLogUs==None and enPassUs==None:
            c.execute(f"INSERT INTO userAccs (logUser, passUser) VALUES ('{encrypted_login}', '{encrypted_password}')")
            db.commit()
                      
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not os.path.exists(file_path):
                open(file_path, "w").close()
            with open(file_path, "a") as file:
                file.write("Created user " + login + " " + current_datetime + "\n")       
        else: 
            c.execute(f"DELETE FROM userAccs WHERE logUser='{encrypted_login}' AND passUser='{encrypted_password}'")
            db.commit()
            
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not os.path.exists(file_path):
                open(file_path, "w").close()
            with open(file_path, "a") as file:
                file.write("Deleted user " + login + " " + current_datetime + "\n")

if __name__ == "__main__":
    import sys
    db=sqlite3.connect("damage.db")
    c=db.cursor()
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())