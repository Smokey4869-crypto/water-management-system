from tkinter import *
import tkinter as tk
from tkinter import font as tkfont
from db import Database
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class LeftFrame(tk.Frame):
    """ This class creates a frame for my program window """

    def __init__(self, parent):
        super().__init__(parent)
        self.var1 = ""
        self.btn_frame = None
        self.canvasinter = None
        self.ax = None
        self.db = Database(filename="my_water.db")
        self.config(bd=3, bg="royal blue", relief=RIDGE)
        self.create_widget()

    def create_widget(self):
        self.btn1 = Button(self, text="View Water Consumption",
                           command=lambda: self.view_water_consumption(self.btn_frame), width=20).grid(row=0,
                                                                                                       column=0,
                                                                                                       padx=30,
                                                                                                       pady=30)
        self.btn2 = Button(self, text="Delete canvas",
                           width=20, command=lambda: self.delete_canvas).grid(row=1,
                                                                              column=0,
                                                                              padx=30,
                                                                              pady=30)
        self.btn3 = Button(self, text="View Money Paid ",
                           width=20, command=lambda: self.view_money_paid(self.btn_frame)).grid(row=2,
                                                                                                column=0,
                                                                                                padx=30,
                                                                                                pady=30)

    def view_water_consumption(self, fm3):
        customer_month = []
        water_amounts, months = self.db.total_amount_of_water_by_year(customer_id=self.var1)
        for month in months:
            if (month[5:7] == "01"):
                customer_month.append("January")
            elif (month[5:7] == "02"):
                customer_month.append("February")
            elif (month[5:7] == "03"):
                customer_month.append("March")
            elif (month[5:7] == "04"):
                customer_month.append("April")
            elif (month[5:7] == "05"):
                customer_month.append("May")
            elif (month[5:7] == "06"):
                customer_month.append("June")
            elif (month[5:7] == "07"):
                customer_month.append("July")
            elif (month[5:7] == "08"):
                customer_month.append("August")

            elif (month[5:7] == "09"):
                customer_month.append("September")
            elif (month[5:7] == "10"):
                customer_month.append("October")
            elif (month[5:7] == "11"):
                customer_month.append("November")
            elif (month[5:7] == "12"):
                customer_month.append("December")
        fig2 = plt.figure(figsize=(6, 6), dpi=80, tight_layout={'pad': 1})
        plt.bar(customer_month, water_amounts, color='maroon',
                width=0.5)
        plt.xlabel("Month")
        plt.ylabel("Water amount")
        plt.title("Water consumption in 2021")
        self.canvasinter = FigureCanvasTkAgg(fig2, master=fm3)
        self.canvasinter.draw()
        self.canvasinter.get_tk_widget().grid(row=0, column=0, padx=50, pady=50)

    def delete_canvas(self):
        self.canvasinter.delete("all")

    def view_money_paid(self, fm3):
        customer_month = []
        amount_of_money, months = self.db.total_amount_of_money_by_year(customer_id=self.var1)
        for month in months:
            if (month[5:7] == "01"):
                customer_month.append("January")
            elif (month[5:7] == "02"):
                customer_month.append("February")
            elif (month[5:7] == "03"):
                customer_month.append("March")
            elif (month[5:7] == "04"):
                customer_month.append("April")
            elif (month[5:7] == "05"):
                customer_month.append("May")
            elif (month[5:7] == "06"):
                customer_month.append("June")
            elif (month[5:7] == "07"):
                customer_month.append("July")
            elif (month[5:7] == "08"):
                customer_month.append("August")

            elif (month[5:7] == "09"):
                customer_month.append("September")
            elif (month[5:7] == "10"):
                customer_month.append("October")
            elif (month[5:7] == "11"):
                customer_month.append("November")
            elif (month[5:7] == "12"):
                customer_month.append("December")
        fig2 = plt.figure(figsize=(6, 6), dpi=80, tight_layout={'pad': 1})
        plt.bar(customer_month, amount_of_money, color='maroon',
                width=0.5)
        plt.xlabel("Month")
        plt.ylabel("Money spent")
        plt.title("Money spent in water in 2021")
        self.canvasinter = FigureCanvasTkAgg(fig2, master=fm3)
        self.canvasinter.draw()
        self.canvasinter.get_tk_widget().grid(row=0, column=0, padx=50, pady=50)


class RightFrame(tk.Frame):
    """ This class creates a frame for my program window """

    def __init__(self, parent):
        super().__init__(parent)
        self.config(bd=3, bg="#000000", relief=RIDGE)
