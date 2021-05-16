from tkinter import *
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import *
import math


class Customers:
    def __init__(self, root, household_name, household_id):
        self.id = household_id
        self.username = household_name

        self.root = root
        self.root.title("Welcome " + self.username)
        self.root.geometry("1300x720+0+0")
        self.root.iconbitmap('water.ico')

        # Connect database
        self.database = sqlite3.connect('water.db')
        self.cursor = self.database.cursor()

        # Create a style for notebook
        self.style = ttk.Style()
        self.style.theme_create('pastel', settings={
            ".": {
                "configure": {
                    "background": 'white',  # All except tabs
                    "font": ('arial', '10')
                }
            },
            "TNotebook": {
                "configure": {
                    "background": 'white',  # Your margin color
                    "tabmargins": [2, 5, 0, 0],  # margins: left, top, right, separator
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "background": 'white',  # tab color when not selected
                    "padding": [10, 2],
                    "font": ('Calibri', '10', 'bold')
                },
                "map": {
                    "background": [("selected", '#ccf3ff')],  # Tab color when selected
                    "expand": [("selected", [1, 1, 1, 0])]  # text margins
                }
            }
        })
        # Images for home frame
        self.user_logo = ImageTk.PhotoImage(Image.open("images//user_logo.png").resize((40, 40), Image.ANTIALIAS))
        self.water_logo = ImageTk.PhotoImage(Image.open("images//water_logo.png").resize((40, 40), Image.ANTIALIAS))
        self.money_logo = ImageTk.PhotoImage(Image.open("images//money_logo.jpg").resize((55, 55), Image.ANTIALIAS))

        # =======================Set background image=====================
        self.image_bg = ImageTk.PhotoImage(
            Image.open('images//water_background.jpg').resize((1300, 720), Image.ANTIALIAS))
        self.background = Label(self.root, image=self.image_bg)
        self.background.place(x=0, y=0)

        # =================================================================
        # =======================Create features frame=====================
        # =================================================================
        self.feature = LabelFrame(self.root, height=561, width=1159, bg="white", highlightbackground="black")
        self.feature.place(x=60, y=50)

        self.user = ImageTk.PhotoImage(Image.open("images//user.png").resize((80, 80), Image.ANTIALIAS))
        self.user_label = Label(self.feature, image=self.user, bg="white")
        self.user_label.place(x=40, y=10)

        # Home button
        self.home_btn = Button(self.feature, text="HOME", font=("arial", 10, "bold"), width=20, bg="white",
                               command=self.click_home)
        self.home_btn.place(x=0, y=100)
        # View Detail button
        self.view_btn = Button(self.feature, text="VIEW DETAIL", font=("arial", 10, "bold"), width=20, bg="white",
                               command=self.click_view)
        self.view_btn.place(x=0, y=130)
        # Exit button
        self.exit_btn = Button(self.feature, text="EXIT", font=("arial", 10, "bold"), width=20, bg="white",
                               command=self.click_exit)
        self.exit_btn.place(x=0, y=160)

        # =================================================================
        # =============================Log out panel=======================
        # =================================================================
        self.panel = LabelFrame(self.feature, width=987, height=40, bg="white", highlightbackground="black")
        self.panel.place(x=170, y=-2)

        self.welcome = Label(self.panel, text="Hello, " + self.username, font=("Calibri", 12, "bold"), bg='white')
        self.welcome.place(x=711, y=6)

        # Log out button
        self.logout_btn = Button(self.panel, text="Log Out", command=self.click_logout, relief=FLAT,
                                 font=("Calibri", 10), bg='white')
        self.logout_btn.place(x=920, y=6)

        self.click_home()

    def click_view(self):
        view_frame = LabelFrame(self.feature, width=987, height=522, bg="white", highlightbackground="black")
        view_frame.place(x=170, y=37)

        self.style.theme_use('pastel')
        # ======================Create notebook===================
        notebook = ttk.Notebook(view_frame)
        notebook.place(x=52, y=6)

        self.frame1 = Frame(notebook, width=893, height=459, bg="#ccf3ff")
        self.frame2 = Frame(notebook, width=893, height=459, bg="#ccf3ff")
        self.search = Frame(notebook, width=893, height=459, bg="#ccf3ff")

        self.frame1.pack(fill="both", expand=1)
        self.frame2.pack(fill="both", expand=1)
        self.search.pack(fill="both", expand=1)

        notebook.add(self.frame1, text="View Water Consumption")
        notebook.add(self.frame2, text="View Money Paid")
        notebook.add(self.search, text="Search bill")

        # Create Option Menu
        MONTHS = [
            "All months",
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ]

        YEARS = [
            "2020",
            "2021"
        ]
        # ================================================================
        # ======================View water consumption====================
        # ================================================================
        search_label1 = Label(self.frame1, text="Search for:", font=("arial", 12, "bold"), bg="#ccf3ff")
        search_label1.place(x=19, y=19)

        year_label1 = Label(self.frame1, text="Year:", font=("arial", 10, "bold"), bg="#ccf3ff")
        year_label1.place(x=43, y=53)
        year1 = StringVar(self.frame1)
        year1.set(YEARS[1])
        search_year1 = OptionMenu(self.frame1, year1, *YEARS)
        search_year1.place(x=100, y=50)

        # Search button
        search_btn1 = Button(self.frame1, text="Search", font=("arial", 10, "bold"), bg="white",
                             command=lambda: self.view_water_consumption(year1.get()))
        search_btn1.place(x=200, y=50)

        # ================================================================
        # ==========================View money paid=======================
        # ================================================================
        search_label2 = Label(self.frame2, text="Search for:", font=("arial", 12, "bold"), bg="#ccf3ff")
        search_label2.place(x=19, y=19)

        year_label2 = Label(self.frame2, text="Year:", font=("arial", 10, "bold"), bg="#ccf3ff")
        year_label2.place(x=43, y=53)
        year2 = StringVar(self.frame2)
        year2.set(YEARS[1])
        search_year2 = OptionMenu(self.frame2, year2, *YEARS)
        search_year2.place(x=100, y=50)

        # Search button
        search_btn2 = Button(self.frame2, text="Search", font=("arial", 10, "bold"), bg="white",
                             command=lambda: self.view_money_paid(year2.get()))
        search_btn2.place(x=200, y=50)

        # ================================================================
        # ======================Search bill===============================
        # ================================================================
        search_label = Label(self.search, text="Search for:", font=("arial", 12, "bold"), bg="#ccf3ff")
        search_label.place(x=19, y=19)

        # Month
        month_label = Label(self.search, text="Month:", font=("arial", 10, "bold"), bg="#ccf3ff")
        month_label.place(x=43, y=53)
        month = StringVar(self.search)
        month.set(MONTHS[0])
        search_month = OptionMenu(self.search, month, *MONTHS)
        search_month.place(x=100, y=50)

        # Year
        year_label = Label(self.search, text="Year:", font=("arial", 10, "bold"), bg="#ccf3ff")
        year_label.place(x=219, y=53)
        year = StringVar(self.frame1)
        year.set(YEARS[1])
        search_year = OptionMenu(self.search, year, *YEARS)
        search_year.place(x=270, y=50)

        # Search button
        search_btn = Button(self.search, text="Search", font=("arial", 10, "bold"), bg="white",
                            command=lambda: self.search_bill(month.get(), year.get()))
        search_btn.place(x=370, y=50)

    def view_water_consumption(self, year):
        # Plot
        fig1 = plt.figure(figsize=(5, 5), dpi=80, tight_layout={'pad': 1})
        canvas1 = FigureCanvasTkAgg(fig1, master=self.frame1)

        months, water_amounts = self.water_consumed(year)
        total_amount = 0
        for i in range(len(water_amounts)):
            total_amount += water_amounts[i]
        average_amount = math.ceil((total_amount / len(water_amounts)) * 10) / 10
        plt.clf()
        plt.bar(months, water_amounts, width=0.4)
        plt.plot([0, 11], [average_amount, average_amount], "k--")
        plt.legend(['Average'])
        plt.xlabel("Month")
        plt.ylabel("Water amount")
        plt.title("Water consumption in " + year)

        canvas1.draw()
        canvas1.get_tk_widget().place(x=400, y=30)

        w_total = Label(self.frame1, text="Total amount: " + str(total_amount) + " m3", font=("arial", 12, "bold"),
                        bg="#ccf3ff")
        w_total.place(x=60, y=200)

        w_aver = Label(self.frame1, text="Average amount: " + str(average_amount) + " m3", font=("arial", 12, "bold"),
                       bg="#ccf3ff")
        w_aver.place(x=60, y=240)

    def view_money_paid(self, year):
        # Plot
        fig2 = plt.figure(figsize=(5, 5), dpi=80, tight_layout={'pad': 1})
        canvas2 = FigureCanvasTkAgg(fig2, master=self.frame2)

        months, amount_of_money = self.money_consumed(year)
        total_amount = 0
        for i in range(len(amount_of_money)):
            total_amount += amount_of_money[i]
        average_amount = math.ceil((total_amount / len(amount_of_money)) * 10) / 10
        plt.clf()
        plt.bar(months, amount_of_money, width=0.4)
        plt.plot([0, 11], [average_amount, average_amount], "k--")
        plt.legend(['Average'])
        plt.xlabel("Month")
        plt.ylabel("Money Spent")
        plt.title("Money spent in water in " + year)

        canvas2.draw()
        canvas2.get_tk_widget().place(x=400, y=30)

        m_total = Label(self.frame2, text="Total amount: " + str(total_amount) + " VND", font=("arial", 12, "bold"),
                        bg="#ccf3ff")
        m_total.place(x=60, y=200)

        m_aver = Label(self.frame2, text="Average amount: " + str(average_amount) + " VND", font=("arial", 12, "bold"),
                       bg="#ccf3ff")
        m_aver.place(x=60, y=240)

    def search_bill(self, month, year):
        # Create Treeview Frame
        tree_frame = Frame(self.search)
        tree_frame.place(x=30, y=144)

        # Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create Treeview
        tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        tree.pack()

        # Configure the scrollbar
        tree_scroll.config(command=tree.yview)

        # Define Columns
        tree['columns'] = ("Billing ID", "Household ID", "Water Consumption", "From Date", "To Date",
                           "Total Money", "Money Paid")
        # Format Columns
        tree.column("#0", width=0, stretch=NO)
        tree.column("Billing ID", anchor=CENTER, width=100)
        tree.column("Household ID", anchor=CENTER, width=120)
        tree.column("Water Consumption", anchor=CENTER, width=120)
        tree.column("From Date", anchor=CENTER, width=120)
        tree.column("To Date", anchor=CENTER, width=120)
        tree.column("Total Money", anchor=E, width=120)
        tree.column("Money Paid", anchor=CENTER, width=120)

        # Create Headings
        tree.heading("#0", text="", anchor=CENTER)
        tree.heading("Billing ID", text="Billing ID", anchor=CENTER)
        tree.heading("Household ID", text="Household ID", anchor=CENTER)
        tree.heading("Water Consumption", text="Water Consumption", anchor=CENTER)
        tree.heading("From Date", text="From Date", anchor=CENTER)
        tree.heading("To Date", text="To Date", anchor=CENTER)
        tree.heading("Total Money", text="Total Money", anchor=CENTER)
        tree.heading("Money Paid", text="Money Paid", anchor=CENTER)

        # Add Data
        self.cursor.execute("SELECT *, CASE WHEN is_paid = 1 THEN 'Yes' ELSE 'No' END as paid FROM billing")
        data = self.cursor.fetchall()

        if month == "January":
            month = "01"
        elif month == "February":
            month = "02"
        elif month == "March":
            month = "03"
        elif month == "April":
            month = "04"
        elif month == "May":
            month = "05"
        elif month == "June":
            month = "06"
        elif month == "July":
            month = "07"
        elif month == "August":
            month = "08"
        elif month == "September":
            month = "09"
        elif month == "October":
            month = "10"
        elif month == "November":
            month = "11"
        elif month == "December":
            month = "12"
        else:
            month = "0"

        count = 0
        for record in data:
            if record[1] == self.id:
                if record[3][0:4] == year and (record[3][5:7] == month or month == "0"):
                    tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2],
                                                                                    record[3], record[4], record[5],
                                                                                    record[7]))
            count += 1

    def click_logout(self):
        """Logouts the user to login page from where they will require password in order to login again"""
        win = Toplevel()
        # LoginScreen(win)
        self.root.withdraw()
        win.deiconify()

    def click_exit(self):
        """ Allows user to terminates the program when chosen yes"""
        self.root.deiconify()
        ask = messagebox.askyesnocancel("Confirm Exit", "Are you sure you want to Exit?")
        if ask is True:
            self.root.quit()

    def click_home(self):
        home_frame = LabelFrame(self.feature, width=987, height=522, bg="white", highlightbackground="black")
        home_frame.place(x=170, y=37)

        # ======================Information frame=============================
        info_frame = LabelFrame(home_frame, width=330, height=180, bg="white", relief="raised")
        info_frame.place(x=80, y=50)

        info_label = Label(info_frame, image=self.user_logo, bg="white", width=50, height=50, relief="flat")
        info_label.place(x=10, y=10)

        i_label1 = Label(info_frame, text="Personal Information:", fg="#1a53ff", bg="white",
                         font=("Calibri", 15))
        i_label1.place(x=70, y=20)

        id = Label(info_frame, text="ID: " + str(self.id), fg="#004d99", bg="white", font=("Calibri", 15))
        id.place(x=60, y=60)

        name = Label(info_frame, text="Full name: " + self.username, fg="#004d99", bg="white", font=("Calibri", 15))
        name.place(x=60, y=90)

        # ==========================Water spent frame============================
        water_frame = LabelFrame(home_frame, width=330, height=180, bg="white", relief="raised")
        water_frame.place(x=550, y=300)

        months, water_amounts = self.water_consumed("2021")
        total_amount = 0
        for i in range(len(water_amounts)):
            total_amount += water_amounts[i]

        water_label = Label(water_frame, image=self.water_logo, bg="white", width=50, height=50, relief="flat")
        water_label.place(x=10, y=10)

        w_label1 = Label(water_frame, text="Total amount of water\nused in 2021:", fg="#1a53ff", bg="white",
                         font=("Calibri", 15))
        w_label1.place(x=70, y=20)
        w_label2 = Label(water_frame, text=str(total_amount) + " m3", fg="#004d99", bg="white", font=("Calibri", 25))
        w_label2.place(x=110, y=100)

        # ==========================Calendar============================================
        cal_frame = LabelFrame(home_frame, width=330, height=180, bg="white", relief="raised")
        cal_frame.place(x=550, y=50)
        cal = Calendar(cal_frame, selectmode="day", year=2021, month=5, day=15, showweeknumbers=False,
                       background="white", foreground='black', bordercolor="white",
                       headersbackground="white", headersforeground='#1a53ff',
                       selectbackground="#ccf3ff", selectforeground="black")
        cal.place(x=50, y=2)

        # ========================Money spent frame===============================
        money_frame = LabelFrame(home_frame, width=330, height=180, bg="white", relief="raised")
        money_frame.place(x=80, y=300)

        months, amount_of_money = self.money_consumed("2021")
        total_amount = 0
        for i in range(len(amount_of_money)):
            total_amount += amount_of_money[i]

        money_label = Label(money_frame, image=self.money_logo, bg="white", width=55, height=55, relief="flat")
        money_label.place(x=10, y=10)

        m_label1 = Label(money_frame, text="Total amount of money\nused in 2021:", fg="#1a53ff", bg="white",
                         font=("Calibri", 15))
        m_label1.place(x=70, y=20)
        m_label2 = Label(money_frame, text=str(total_amount) + " VND", fg="#004d99", bg="white", font=("Calibri", 25))
        m_label2.place(x=70, y=100)

    def money_consumed(self, year):
        self.cursor.execute("SELECT * FROM billing")
        data = self.cursor.fetchall()
        amount_of_money = []
        months = []
        for record in data:
            if record[1] == self.id:
                if record[3][0:4] == year:
                    amount_of_money.append(record[5])
                    months.append(record[3][5:7])
        return months, amount_of_money

    def water_consumed(self, year):
        self.cursor.execute("SELECT * FROM billing")
        data = self.cursor.fetchall()
        water_amounts = []
        months = []
        for record in data:
            if record[1] == self.id:
                if record[3][0:4] == year:
                    water_amounts.append(record[2])
                    months.append(record[3][5:7])
        return months, water_amounts


def window(id):
    root = Tk()
    database = sqlite3.connect('water.db')
    c = database.cursor()
    c.execute("SELECT * FROM household")
    data = c.fetchall()
    for record in data:
        if record[0] == id:
            Customers(root, record[1], record[0])
    root.mainloop()


if __name__ == '__main__':
    window(3)
