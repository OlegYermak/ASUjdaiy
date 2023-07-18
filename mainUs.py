import tkinter as tk
from tkinter.messagebox import showerror
from datetime import datetime
import dbhelper
from dateEdit import DateEdit

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QMainWindow, QStackedWidget, QWidget
import sqlite3
import subprocess

DB_NAME = 'damage.db'

GRID_ROWS = 4
GRID_COLUMNS = 4

LABELS = {
    'human': 'Особовий склад',
    'tank': 'Танки',
    'helicopter': 'Вертольоти',
    'armored_car': 'Броньовані\nмашини',
    'artillery_system': 'Артилерійські\nсистеми',
    'drone': 'БПЛА',
    'mlrs': 'РСЗВ',
    'cruise_missile': 'Крилаті\nракети',
    'anti_aircraft': 'ППО',
    'warship': 'Кораблі',
    'special_technique': 'Спец.техніка',
    'aircraft': 'Літаки',
    'tanker_trucks': 'Цистерни'
}


class EditWindow(tk.Tk):
    def __init__(self):

        super().__init__()
        # self.date = datetime.now().timestamp()
        self.fields = {}
        self.wasFilled = False
        self.db = dbhelper.DB(DB_NAME)
        self.title("Додавання та редагування даних")
        self.centerWindow()
        self.iconbitmap("img/favicon.ico")
        self.setWidgets()

    def centerWindow(self):
        self.resizable(width=False, height=False)
        w = 450
        h = 700
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f'{w}x{h}+{x}+{y}')

    def setWidgets(self):
        self.topFrame = tk.Frame(self)
        self.topFrame.pack()

        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack(fill=tk.X, pady=[5, 10])

        for key, value in LABELS.items():
            wrapper = tk.Frame(self.mainFrame)
            self.fields[key] = {
                'frame': wrapper,
                'label': tk.Label(wrapper, text=value, font=('Arial', 16, 'bold')),
                'entry': tk.Entry(wrapper, font=('Arial', 16, 'bold'), width=15)
            }

        self.topLabel = tk.Label(
            self.topFrame, text='Виберіть дату для внесення даних: ', font=('Arial', 14, 'bold'))
        self.topLabel.pack()

        self.dateEdit = DateEdit(
            self.topFrame, "24.02.2022", datetime.now().strftime(dbhelper.DATE_TIME_FORMAT), handler=self.dateChangeHandler)
        self.dateEdit.pack(pady=[15, 0])

        for key in LABELS.keys():
            self.fields[key]['frame'].pack(fill=tk.X, pady=[5, 0], padx=[5, 0])
            self.fields[key]['label'].pack(side=tk.LEFT)
            self.fields[key]['entry'].pack(side=tk.RIGHT, padx=[0, 20])

        self.saveBtn = tk.Button(self, text='Зберегти', font=(
            'Arial', 20, 'bold'), command=self.saveChanges)
        self.saveBtn.pack(pady=[10, 0])

    def dateChangeHandler(self, date: datetime):
        print("date was changed")
        self.date = date
        record = self.db.getRecord(date.timestamp())
        self.wasFilled = True if record else False
        for key, value in LABELS.items():
            str_value = str(record[key]) if record else '0'
            self.fields[key]['entry'].delete(0, tk.END)
            self.fields[key]['entry'].insert(0, str_value)

    def saveChanges(self):
        values = {}
        values['date'] = self.date.timestamp()
        try:
            for key in LABELS.keys():
                int_value = int(self.fields[key]['entry'].get())
                values[key] = int_value
            if self.wasFilled:
                self.db.updateRecord(values)
            else:
                self.wasFilled = True
                self.db.addRecord(values)
        except:
            showerror(
                title="!Помилка!", message="Помилкові дані в полях!\nПеревірте та спробуйте ще раз!", parent=self)


class ReportWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.today = dbhelper.toDateTimeStr(datetime.now())
        self.startDate = datetime.now()
        self.endDate = datetime.now()
        self.checkButtons = {}
        self.countLabels = {}
        self.selectedFields = set()
        self.changed = {key: tk.IntVar(self) for key in LABELS.keys()}
        self.db = dbhelper.DB(DB_NAME)
        self.title("Зведена інформація за період")
        self.centerWindow()
        self.setWidgets()

    def centerWindow(self):
        self.resizable(width=False, height=True)
        w = 1440
        h = 750
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f'{w}x{h}+{x}+{y}')

    def setWidgets(self):
        self.topFrame = tk.Frame(self)
        self.topFrame.pack(fill=tk.X, anchor=tk.N)
        self.topLabel = tk.Label(self.topFrame, text='Виберіть період:', fg='red', font=(
            'Arial', 20, 'bold'), pady=10)
        self.topLabel.pack()

        self.periodFrame = tk.Frame(self)
        self.periodFrame.pack(fill=tk.X, pady=[0, 10])

        self.startPeriod = DateEdit(
            self.periodFrame, "24.02.2022", self.today, handler=self.startDateChange)
        self.startPeriod.pack(side=tk.LEFT, padx=[20, 0])

        self.btn = tk.Button(self.periodFrame, text="Сформувати", font=(
            'Arial', 12, 'bold'), command=self.makeReport)
        self.btn.pack(side=tk.LEFT, padx=260)

        self.endPeriod = DateEdit(
            self.periodFrame, "24.02.2022", self.today, handler=self.endDateChange)
        self.endPeriod.pack(side=tk.RIGHT, padx=[0, 20])

        self.mainFrame = tk.Frame(self, bg='red')
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

        self.leftFrame = tk.Frame(self.mainFrame)
        self.leftFrame.pack(side=tk.LEFT, fill=tk.Y)

        for key in LABELS.keys():
            frame = tk.Frame(self.leftFrame)
            frame.pack(fill=tk.X, pady=[10, 0], padx=[5, 0])

            self.checkButtons[key] = tk.Checkbutton(frame, text=LABELS[key], font=(
                'Arial', 10, 'bold'), onvalue=1, offvalue=0, variable=self.changed[key], command=self.fieldSelect)
            self.checkButtons[key].pack(side=tk.LEFT)

            self.countLabels[key] = tk.Label(frame, text='0',
                                             font=('Arial', 10, 'bold'))
            self.countLabels[key].pack(side=tk.RIGHT, padx=[10,5])

        self.canvasFrame = tk.Frame(self.mainFrame, bg='brown')
        self.canvasFrame.pack(fill=tk.BOTH, expand=True)

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvasFrame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def fieldSelect(self):
        for key in LABELS.keys():
            if self.changed[key].get():
                self.selectedFields.add(key)
            else:
                self.selectedFields -= {key}

    def startDateChange(self, date: datetime):
        self.startDate = date

    def endDateChange(self,  date: datetime):
        self.endDate = date

    def makeReport(self):
        self.total = self.db.getTotal(
            self.startDate.timestamp(), self.endDate.timestamp())
        self.report = self.db.getReport(
            self.startDate.timestamp(), self.endDate.timestamp())

        for key in LABELS.keys():
            self.countLabels[key].config(text = str(self.total[key]))

        dates = []
        for item in self.report:
            dates.append(item['date'])

        selected = {key: [] for key in self.selectedFields}
        for line in self.report:
            for key in self.selectedFields:
                selected[key].append(line[key])

        self.ax.clear()
        for key in self.selectedFields:
            self.ax.plot(dates, selected[key], label=LABELS[key])

        self.ax.set_xlabel('Дата')
        self.ax.set_ylabel('Кількість')      

        self.ax.legend()
        self.canvas.draw()


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db = dbhelper.DB(DB_NAME)
        self.title("")
        self.centerWindow()
        self.iconbitmap("img/favicon.ico")
        self.setWidgets()
        self.bind("<FocusIn>", self.OnFocusIn)

    def centerWindow(self):
        self.resizable(width=False, height=False)
        w = 1100
        h = 760
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f'{w}x{h}+{x}+{y}')

    def OnFocusIn(self, *args):
        self.updateData()

    def updateData(self):
        today = datetime.now()
        self.topLabel.config(
            text="Втрати противника станом на: " + dbhelper.toDateTimeStr(today))
        values = self.db.getTotal(0, today.timestamp())
        for k, v in LABELS.items():
            self.labelsWidgets[k].config(text=v+'\n'+str(values[k]))

    def setWidgets(self):

        # Верхня панель
        self.topFrame = tk.Frame(self)
        self.topFrame.pack()
        self.topLabel = tk.Label(self.topFrame, text="Втрати противника станом на: ",
                                 fg='red', font=('Arial', 20, 'bold'), pady=20)
        self.topLabel.pack()

        # Центральна панель
        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack(fill=tk.X, anchor=tk.N)
        for row in range(GRID_ROWS):
            self.mainFrame.rowconfigure(index=row, weight=1)
        for col in range(GRID_COLUMNS):
            self.mainFrame.columnconfigure(index=col, weight=1)

        self.labelsWidgets = {}
        index = 0
        
        for key in LABELS.keys():
            row = index // GRID_ROWS
            col = index % GRID_COLUMNS

            wrapper = tk.Frame(self.mainFrame)
            wrapper.grid(row=row, column=col, stick=tk.NSEW, pady=5)

            img = tk.PhotoImage(file='./img/{}.png'.format(key))
            imgLabel = tk.Label(wrapper, image=img)
            imgLabel.image_ref = img
            imgLabel.pack()

            self.labelsWidgets[key] = tk.Label(
                wrapper, text='', fg='black', font=('Arial', 18))#, 'bold'))
            self.labelsWidgets[key].pack()

            index += 1

        # Нижня панель
        self.bottomFrame = tk.Frame(self)
        self.bottomFrame.pack(fill=tk.X, anchor=tk.N, pady=[20,0])
        for col in range(GRID_COLUMNS):
            self.bottomFrame.columnconfigure(index=col, weight=1)
            
        self.reportBtn = tk.Button(
            self.bottomFrame, text="Звіти/графіки", font=('Arial', 20, 'bold'))

        self.reportBtn.grid(row=0, column=2, sticky='we', padx=[200, 200])
        self.reportBtn.config(command=self.callReportWindow)
        
        self.rozrB = tk.Button(
            self.bottomFrame, text="Розробники", font=('Arial', 10, 'bold'))

        self.rozrB.grid(row=0, column=0, sticky='we', padx=[50, 30])
        self.rozrB.config(command=self.rozrBtn)
        
        self.hMeBtn = tk.Button(
            self.bottomFrame, text="Підтримка та версія", font=('Arial', 10, 'bold'))

        self.hMeBtn.grid(row=0, column=3, sticky='we', padx=[50, 30])
        self.hMeBtn.config(command=self.helpMeBtn)

    def callEditWindow(self):
        EW = EditWindow()

    def callReportWindow(self):
        RP = ReportWindow()
        
    def rozrBtn(self):
        subprocess.Popen(["python", "AddF/testcard.py"], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(["python", "AddF/analcard.py"], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(["python", "AddF/progcard.py"], creationflags=subprocess.CREATE_NO_WINDOW)
        
    def helpMeBtn(self):
        subprocess.Popen(["python", "AddF/techcard.py"], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(["python", "AddF/telcard.py"], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(["python", "AddF/abсard.py"], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(["python", "AddF/reqcard.py"], creationflags=subprocess.CREATE_NO_WINDOW)


if __name__ == "__main__":
    MW = MainWindow()
    MW.mainloop()
