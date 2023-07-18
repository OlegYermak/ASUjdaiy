import tkinter as tk
from datetime import datetime, timedelta
import dbhelper

FONT = {
    'font': ('Arial', 12, 'bold')
}


class DateEdit(tk.Frame):
    def __init__(self, master, minDate: str, maxDate: str, handler=None):
        super().__init__(master=master)
        self.handler = handler
        self.minDate = dbhelper.strToDateTime(minDate)
        self.maxDate = dbhelper.strToDateTime(maxDate)
        self.currDate = dbhelper.strToDateTime(maxDate)
        self.setWidgets()
        self.changeDate()

    def setWidgets(self, someString=''):
        self.prevDayBtn = tk.Button(
            self, text='< день', **FONT, command=self.prevDayClick)
        self.prevDayBtn.pack(side=tk.LEFT, expand=True)

        self.prevMonthBtn = tk.Button(
            self, text='< місяць', **FONT, command=self.prevMonthClick)
        self.prevMonthBtn.pack(side=tk.LEFT)

        self.dateLabel = tk.Label(self, text=someString, **FONT)
        self.dateLabel.pack(side=tk.LEFT)

        self.nextMonthBtn = tk.Button(
            self, text='місяць >', **FONT, command=self.nextMonthClick)
        self.nextMonthBtn.pack(side=tk.LEFT)

        self.nextDayBtn = tk.Button(
            self, text='день >', **FONT, command=self.nextDayClick)
        self.nextDayBtn.pack(side=tk.LEFT)

    def changeDate(self):
        self.dateLabel.config(text=dbhelper.toDateTimeStr(self.currDate))
        if self.handler:
            self.handler(self.currDate)

    def prevDayClick(self, *args):
        some_date = self.currDate - timedelta(days=1)
        if some_date >= self.minDate:
            self.currDate = some_date
            self.changeDate()

    def nextDayClick(self, *args):
        some_date = self.currDate + timedelta(days=1)
        if some_date <= self.maxDate:
            self.currDate = some_date
            self.changeDate()

    def prevMonthClick(self, *args):
        some_date = self.currDate - timedelta(weeks=4)
        if some_date >= self.minDate:
            self.currDate = some_date
            self.changeDate()

    def nextMonthClick(self, *args):
        some_date = self.currDate + timedelta(weeks=4)
        if some_date <= self.maxDate:
            self.currDate = some_date
            self.changeDate()

    def getDate(self):
        return self.currDate
