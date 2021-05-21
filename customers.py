from tkinter import *
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import *
import math
from db import Database

database = Database("water_database.db")


def center_window(root, width, height):
    positionRight = int(root.winfo_screenwidth() / 2 - width / 2)
    positionDown = int(root.winfo_screenheight() / 2 - height / 2 - 60)

    root.geometry("%dx%d+%d+%d" % (width, height, positionRight, positionDown))


class FrameSetting:
    def __init__(self, root, username):
        self.root = root
        self.setting_frame = LabelFrame()
        self.username = username
        self.entries = []
        self.image_fr = ImageTk.PhotoImage(Image.open("images//Change_pass_cus.png")
                                           .resize((882, 475), Image.ANTIALIAS))
        self.sub_btn = ImageTk.PhotoImage(Image.open("images//Sub_btn_cus.png")
                                          .resize((90, 30), Image.ANTIALIAS))
        self.draw()

    def draw(self):
        self.setting_frame = Label(self.root, image=self.image_fr, bg="white", relief=FLAT)
        self.setting_frame.place(x=300, y=126)

        record = database.search_exact('adminlogin', 'username', self.username)[0]

        user_entry = Entry(self.setting_frame, relief="flat", width=21, font=("Calibri", 12), bg="#d9eff4")
        user_entry.place(x=340, y=180)
        user_entry.insert(0, record[0])
        user_entry['state'] = DISABLED
        self.entries.append(user_entry)

        pass_entry = Entry(self.setting_frame, relief="flat", width=21, font=("Calibri", 12), bg="#d9eff4")
        pass_entry.place(x=340, y=260)
        pass_entry.insert(0, record[1])
        self.entries.append(pass_entry)

        btn_submit = Button(self.setting_frame, image=self.sub_btn, command=self.submit, relief=FLAT, bg="#d9eff4",
                            activebackground="#d9eff4")
        btn_submit.place(x=390, y=330)

    def submit(self):
        records = []
        for entry in self.entries:
            records.append(entry.get())

        database.update('adminlogin', records, records[0])

        print("To be Update: ", 'adminlogi ', records)

        messagebox.showinfo(title=None, message='Changing Password Successfully')


class Customers:
    def __init__(self, household_id, household_name, area, address):
        self.id = household_id
        self.username = household_name
        self.area = area
        self.address = address

        self.root = Tk()
        self.root.title("Welcome " + self.username)
        center_window(self.root, 1300, 720)
        # self.root.geometry("1300x720")

        self.frame1 = Frame()
        self.frame2 = Frame()
        self.search = Frame()

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
        # Background for home frame
        self.home_bg = ImageTk.PhotoImage(Image.open("images//home_frame.png").resize((882, 475), Image.ANTIALIAS))

        # =======================Set background image=====================
        image = ImageTk.PhotoImage(Image.open("images//customer_bg.png").resize((1300, 720), Image.ANTIALIAS))
        canvas = Canvas(self.root)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=image, anchor="nw")

        # =================================================================
        # =======================Create features frame=====================
        # =================================================================
        feature = LabelFrame(self.root, height=300, width=184.689, bg="#3f489d", relief="flat")
        feature.place(x=100, y=200)

        # Home button
        home_btn = Button(feature, text="HOME", font=("arial", 10, "bold"), width=22,
                          bg="#3f489d", fg="white", relief=GROOVE,
                          command=self.click_home)
        home_btn.place(x=-1, y=0)
        # View Detail button
        view_btn = Button(feature, text="VIEW DETAIL", font=("arial", 10, "bold"), width=22,
                          bg="#3f489d", fg="white", relief=GROOVE,
                          command=self.click_view)
        view_btn.place(x=-1, y=27)
        # Setting button
        setting_btn = Button(feature, text="SETTING", font=("arial", 10, "bold"), width=22,
                             bg="#3f489d", fg="white", relief=GROOVE,
                             command=self.click_setting)
        setting_btn.place(x=-1, y=54)
        # Exit button
        exit_btn = Button(feature, text="EXIT", font=("arial", 10, "bold"), width=22,
                          bg="#3f489d", fg="white", relief=GROOVE,
                          command=self.click_exit)
        exit_btn.place(x=-1, y=81)

        # =================================================================
        # =============================Log out panel=======================
        # =================================================================
        panel = LabelFrame(self.root, width=800, height=40, bg="white", relief=FLAT)
        panel.place(x=356, y=65)

        welcome = Label(panel, text="Hello, " + self.username, font=("arial", 12), bg='white', fg="#005580")
        welcome.place(x=530, y=6)

        # Log out button
        logout_btn = Button(panel, text="Log Out", command=self.click_logout, relief=FLAT,
                            font=("arial", 10), bg='white', fg="#005580", activebackground="white")
        logout_btn.place(x=720, y=6)

        self.click_home()
        self.root.mainloop()

    def click_view(self):
        view_frame = LabelFrame(self.root, width=882, height=475, bg="white", relief=FLAT)
        view_frame.place(x=300, y=126)

        self.style.theme_use('pastel')
        # ======================Create notebook===================
        notebook = ttk.Notebook(view_frame)
        notebook.place(x=30, y=2)

        self.frame1 = Frame(notebook, width=820, height=430, bg="#ccf3ff")
        self.frame2 = Frame(notebook, width=820, height=430, bg="#ccf3ff")
        self.search = Frame(notebook, width=820, height=430, bg="#ccf3ff")

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
        fig1.patch.set_facecolor('#ccf3ff')
        canvas1 = FigureCanvasTkAgg(fig1, master=self.frame1)

        average_amount, total_amount = self.chart_water_consumed(year)
        plt.legend(['Average'])

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
        fig2.patch.set_facecolor('#ccf3ff')
        canvas2 = FigureCanvasTkAgg(fig2, master=self.frame2)

        average_amount, total_amount = self.chart_money_consumed(year)
        plt.legend(['Average'])

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
        tree.column("Household ID", anchor=CENTER, width=100)
        tree.column("Water Consumption", anchor=CENTER, width=120)
        tree.column("From Date", anchor=CENTER, width=100)
        tree.column("To Date", anchor=CENTER, width=100)
        tree.column("Total Money", anchor=E, width=80)
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
        data = database.view_bill()

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
        ask = messagebox.askyesnocancel("Confirm Logout", "Are you sure you want to Log Out")
        if ask is True:
            from water import Login
            self.root.destroy()
            win = Tk()
            Login(win)

    def click_exit(self):
        self.root.deiconify()
        ask = messagebox.askyesnocancel("Confirm Exit", "Are you sure you want to Exit?")
        if ask is True:
            self.root.quit()

    def click_home(self):
        home_frame = Label(self.root,  image=self.home_bg, bg="white", relief=FLAT)
        home_frame.place(x=300, y=126)

        # ======================Information frame=============================

        id_ = Label(home_frame, text=str(self.id), fg="#004d99", bg="#e7f5fd", font=("arial", 13))
        id_.place(x=115, y=88)

        name = Label(home_frame, text=self.username, fg="#004d99", bg="#e7f5fd", font=("arial", 13))
        name.place(x=172, y=110)

        area = Label(home_frame, text=self.area, fg="#004d99", bg="#e7f5fd", font=("arial", 13))
        area.place(x=130, y=136)

        address = Label(home_frame, text=self.address, fg="#004d99", bg="#e7f5fd", font=("arial", 13))
        address.place(x=160, y=160)
        # ==========================Water spent frame============================
        water_frame = LabelFrame(home_frame, width=330, height=160, bg="#e7f5fd", relief=FLAT)
        water_frame.place(x=480, y=60)

        fig2 = plt.figure(figsize=(4, 2), dpi=80, tight_layout={'pad': 1})
        fig2.patch.set_facecolor('#e7f5fd')
        canvas2 = FigureCanvasTkAgg(fig2, master=water_frame)
        self.chart_water_consumed("2021")
        canvas2.draw()
        canvas2.get_tk_widget().place(x=0, y=0)

        # ==========================Calendar============================================
        cal_frame = LabelFrame(home_frame, width=240, height=180, bg="#e7f5fd", relief=FLAT)
        cal_frame.place(x=70, y=250)
        date = str(datetime.date(datetime.now()))
        cal = Calendar(cal_frame, selectmode="day", year=int(date[0:4]), month=int(date[5:7]), day=int(date[8:]),
                       showweeknumbers=False,
                       background="#e7f5fd", foreground='black', bordercolor="white",
                       headersbackground="white", headersforeground='#1a53ff',
                       selectbackground="#ccf3ff", selectforeground="black")
        cal.place(x=2, y=2)

        # ========================Money spent frame===============================
        money_frame = LabelFrame(home_frame, width=330, height=160, bg="#e7f5fd", relief=FLAT)
        money_frame.place(x=480, y=280)

        fig2 = plt.figure(figsize=(4, 2), dpi=80, tight_layout={'pad': 1})
        fig2.patch.set_facecolor('#e7f5fd')
        canvas2 = FigureCanvasTkAgg(fig2, master=money_frame)
        self.chart_money_consumed("2021")
        canvas2.draw()
        canvas2.get_tk_widget().place(x=0, y=0)

    def click_setting(self):
        setting_frame = LabelFrame(self.root, width=882, height=475, bg="white", relief=FLAT)
        setting_frame.place(x=300, y=126)
        FrameSetting(self.root, self.id)

    def chart_money_consumed(self, year):
        months, amount_of_money = database.money_consumed_per_month_by_year(self.id, year)
        total_amount = 0
        for i in range(len(amount_of_money)):
            total_amount += amount_of_money[i]
        average_amount = math.ceil((total_amount / len(amount_of_money)) * 10) / 10
        plt.clf()
        plt.bar(months, amount_of_money, width=0.4)
        plt.plot([0, 11], [average_amount, average_amount], "k--")
        plt.xlabel("Month")
        plt.ylabel("Money Spent")
        plt.title("Money spent in water in " + year)

        return average_amount, total_amount

    def chart_water_consumed(self, year):
        months, water_amounts = database.water_consumed_per_month_by_year(self.id, year)
        total_amount = 0
        for i in range(len(water_amounts)):
            total_amount += water_amounts[i]
        average_amount = math.ceil((total_amount / len(water_amounts)) * 10) / 10
        plt.clf()
        plt.bar(months, water_amounts, width=0.4)
        plt.plot([0, 11], [average_amount, average_amount], "k--")
        plt.xlabel("Month")
        plt.ylabel("Water amount")
        plt.title("Water consumption in " + year)

        return average_amount, total_amount


def CustomerWin(id_):
    data = database.get_customer_info()
    for record in data:
        if record[0] == id_:
            Customers(record[0], record[1], record[2], record[3])


if __name__ == '__main__':
    CustomerWin(3)
