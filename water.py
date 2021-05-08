# import tkinter module
from tkinter import *
from tkinter import font as tkfont
from db import Database
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from testt import LeftFrame, RightFrame

database = Database("my_water.db")


class MainApp():
    def __init__(self, master):
        self.master = master
        self.master.title("Water management system")
        self.master.geometry("1350x800+250+150")
        self.init_login()

    def init_login(self):
        self.fm = Frame(self.master, height=800, width=1350, bg='white')
        self.fm.place(x=0, y=0)

        self.canvas = Canvas(self.fm, height=800, width=1350, bg='#22224b')
        self.canvas.place(x=0, y=0)

        self.fm1 = Frame(self.canvas, height=260, width=300, bg='white', bd=3, relief='ridge')
        self.fm1.place(x=500, y=170)

        self.b1 = Label(self.fm1, text='User ID', bg='white', font=('Arial', 10, 'bold'))
        self.b1.place(x=20, y=42)

        self.e1 = Entry(self.fm1, width=22, font=('arial', 9, 'bold'), bd=4, relief='groove')
        self.e1.place(x=100, y=40)

        self.lb2 = Label(self.fm1, text='Password', bg='white', font=('Arial', 10, 'bold'))
        self.lb2.place(x=20, y=102)

        self.e2 = Entry(self.fm1, width=22, show='*', font=('arial', 9, 'bold'), bd=4, relief='groove')
        self.e2.place(x=100, y=100)

        self.btn1 = Button(self.fm1, text='  login', fg='white', bg='red', width=100, font=('Arial', 11, 'bold'),
                           activebackground='white', activeforeground='black', command=self.login, bd=3,
                           relief='flat',
                           cursor='hand2')
        self.btn1.place(x=25, y=160)
        self.logo = PhotoImage(file='images/user.png')
        self.btn1.config(image=self.logo, compound=LEFT)
        self.small_logo = self.logo.subsample(1, 1)
        self.btn1.config(image=self.small_logo)

        self.btn2 = Button(self.fm1, text='  Clear', fg='white', bg='blue', width=100, font=('Arial', 11, 'bold'),
                           activebackground='white', activeforeground='black', bd=3, relief='flat', cursor='hand2',
                           command=self.mainclear)
        self.btn2.place(x=155, y=160)
        self.log = PhotoImage(file='images/cart.png')
        self.btn2.config(image=self.log, compound=LEFT)
        self.small_log = self.log.subsample(1, 1)
        self.btn2.config(image=self.small_log)

        # -----------------------label clicked change password---------------------

        self.forgot = Label(self.fm1, text='forgotten password', fg='red', bg='#fff', activeforeground='black',
                            font=('cursive', 9, 'bold'))
        self.forgot.place(x=80, y=220)
        self.forgot.bind("<Button>", self.mouseClick)

    def cur(self):
        self.fm3 = Frame(self.master, bg='#1184e8', height=690, width=1350)
        self.fm3.place(x=0, y=110)

        # fig = plt.figure(figsize=(5, 5), dpi=100)
        # fig.set_size_inches(5, 3)
        # labels, water_amount = database.total_amount_of_water_by_area()
        # colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'Orange', 'red', 'blue', 'yellow', 'pink']
        # plt.pie(water_amount, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        #
        # plt.axis('equal')  # creates the pie chart like a circle
        #
        # canvasbar = FigureCanvasTkAgg(fig, master=self.fm3)
        # canvasbar.draw()
        # canvasbar.get_tk_widget().place(x=800, y=175, anchor=CENTER)

        # show the barchart on the ouput window

        self.bt1 = Button(self.fm3, text='  Customers', fg='#fff', bg='#ff0076', font=('Arial', 15, 'bold'), bd=7,
                          width=10,
                          relief='flat',
                          command=self.move_to_customers, cursor='hand2')
        self.bt1.place(x=40, y=40)

        # -------------------------Issuebutton--------------

        self.bt2 = Button(self.fm3, text='Area', fg='#fff', bg='#ff0076', font=('Arial', 15, 'bold'), bd=7, width=10,
                          relief='flat', command=self.move_to_area, cursor='hand2')
        self.bt2.place(x=250, y=40)

        # ---------------------------Editbutton----------------

        self.bt3 = Button(self.fm3, text='Feedback', fg='#fff', bg='#ff0076', font=('Arial', 15, 'bold'), bd=7,
                          width=10,
                          relief='flat', cursor='hand2', command=self.move_to_feedback)
        self.bt3.place(x=40, y=120)

        # -----------------------------Returnbutton----------------

        self.bt4 = Button(self.fm3, text='Service', fg='#fff', bg='#ff0076', font=('Arial', 15, 'bold'), bd=7, width=10,
                          relief='flat', cursor='hand2', command=self.move_to_service)
        self.bt4.place(x=250, y=120)

        # ----------------------Deletebutton---------------------

        self.bt5 = Button(self.fm3, text='Supplier', fg='#fff', bg='#ff0076', font=('Arial', 15, 'bold'), bd=7,
                          width=10,
                          relief='flat', cursor='hand2', command=self.move_to_supplier)
        self.bt5.place(x=40, y=200)

        # --------------------Show Button-----------------------------

        self.bt6 = Button(self.fm3, text='Billing', fg='#fff', bg='#ff0076', font=('Arial', 15, 'bold'), bd=7, width=10,
                          relief='flat', cursor='hand2', command=self.move_to_billing)
        self.bt6.place(x=250, y=200)

        # -------------------------Seearch Button------------------

        self.bt7 = Button(self.fm3, text='Employee', fg='#fff', bg='#ff0076', font=('Arial', 15, 'bold'), bd=7,
                          width=10,
                          relief='flat', cursor='hand2', command=self.move_to_employee)
        self.bt7.place(x=40, y=280)

        try:

            self.bt8 = Button(self.fm3, text='Log Out', fg='#fff', bg='#ff0076', font=('Arial', 15, 'bold'), bd=7,
                              relief='flat', cursor='hand2', command=self.logout)
            self.bt8.place(x=250, y=280)

        except:

            self.bt9 = ttk.Button(self.fm3, text="ram", bg='#11d09a', font=('Arial', 15, 'bold'))
            self.bt9.place(x=40, y=350)

    def login(self):
        self.var1 = self.e1.get()
        self.var2 = self.e2.get()
        if (self.var1 == "admin"):
            self.ab = database.check_user_admin(self.var1, self.var2)
            print(self.ab)
            if self.ab != None:

                self.under_fm = Frame(self.master, height=700, width=1350, bg='#fff')
                self.under_fm.place(x=0, y=0)
                self.fm2 = Frame(self.master, bg='#0f624c', height=80, width=1350)
                self.fm2.place(x=0, y=0)

                self.lbb = Label(self.fm2, bg='#0f624c')
                self.lbb.place(x=15, y=5)
                self.ig = PhotoImage(file='images/library.png')
                self.lbb.config(image=self.ig)
                self.lb3 = Label(self.fm2, text='DASHBOARD', fg='White', bg='#0f624c', font=('Arial', 30, 'bold'))
                self.lb3.place(x=325, y=17)

                # ----------------------------name------------------------

                self.name = Label(self.master, text="Name : ", bg='#fff', fg="black", font=('Arial', 10, 'bold'))
                self.name.place(x=5, y=83)
                self.name1 = Label(self.master, text=self.ab[1], fg='black', bg='#fff', font=('Arial', 10, 'bold'))
                self.name1.place(x=60, y=83)

                self.cur()

            else:
                messagebox.showerror('Library System', 'Your ID or Password is not Valid')
        else:
            self.ab = database.check_customer(self.var1, self.var2)
            print(self.ab)
            if self.ab != None:

                self.under_fm = Frame(self.master, height=700, width=1350, bg='#fff')
                self.under_fm.place(x=0, y=0)
                self.fm2 = Frame(self.master, bg='#0f624c', height=80, width=1350)
                self.fm2.place(x=0, y=0)

                self.lbb = Label(self.fm2, bg='#0f624c')
                self.lbb.place(x=15, y=5)
                self.ig = PhotoImage(file='images/library.png')
                self.lbb.config(image=self.ig)
                self.lb3 = Label(self.fm2, text='DASHBOARD', fg='White', bg='#0f624c', font=('Arial', 30, 'bold'))
                self.lb3.place(x=325, y=17)

                # ----------------------------name------------------------

                self.name = Label(self.master, text="Name : ", bg='#fff', fg="black", font=('Arial', 10, 'bold'))
                self.name.place(x=5, y=83)
                self.name1 = Label(self.master, text=self.ab[1], fg='black', bg='#fff', font=('Arial', 10, 'bold'))
                self.name1.place(x=70, y=83)

                # self.btn_frame = Frame(self.master, bd=3, bg="royal blue", relief=RIDGE)
                # self.btn_frame.place(x=0, y=110, width=500, height=690)

                self.right_frame = RightFrame(self.master)
                self.right_frame.place(x=500, y=110, width=850, height=690)

                self.left_frame = LeftFrame(self.master)
                self.left_frame.var1 = self.var1
                self.left_frame.btn_frame = self.right_frame
                self.left_frame.place(x=0, y=110, width=500, height=690)

                # self.btn1 = Button(self.btn_frame, text="View Water Consumption",
                #                    command=lambda: self.view_water_consumption(self.var1, self.btn_frame),
                #                    width=20).grid(row=0,
                #                                   column=0,
                #                                   padx=10,
                #                                   pady=10)
                # btn2 = Button(self.btn_frame, text="delete canvas",
                #               width=20).grid(row=0,
                #                              column=1,
                #                              padx=10,
                #                              pady=10)


            else:
                messagebox.showerror('Library System', 'Your ID or Password is not Valid')

    def move_to_customers(self):
        # ALL VARIABLES##
        self.cus_id = StringVar()
        self.name = StringVar()
        self.address = StringVar()
        self.area = StringVar()
        self.phone = StringVar()
        self.water_allowance = StringVar()

        self.search_by = StringVar()
        self.search_txt = StringVar()

        # LEFT FRAME
        left_frame = Frame(self.master, bg='#1184e8')
        left_frame.place(x=0, y=110, width=430, height=690)
        left_title = Label(left_frame, text="Manage Customers", font=("times new roman", 20, "bold"), bg="#1184e8",
                           fg="white")
        left_title.grid(row=0, columnspan=2, pady=20)

        left_cus_id = Label(left_frame, text="Customer Id.", font=("times new roman", 20, "bold"), bg="#1184e8",
                          fg="white").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        cus_id = Entry(left_frame, textvariable=self.cus_id, font=("times new roman", 15, "bold"), bd=5,
                          relief=GROOVE).grid(row=1, column=1, padx=00, pady=10, sticky="w")

        left_name = Label(left_frame, text="Customer Name", font=("times new roman", 20, "bold"), bg="#1184e8",
                          fg="white").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        name_text = Entry(left_frame, textvariable=self.name, font=("times new roman", 15, "bold"), bd=5,
                          relief=GROOVE).grid(row=2, column=1, padx=00, pady=10, sticky="w")

        left_area = Label(left_frame, text="Area Id", font=("times new roman", 20, "bold"), bg="#1184e8",
                           fg="white").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        area_id = Entry(left_frame, textvariable=self.area, font=("times new roman", 15, "bold"), bd=5,
                           relief=GROOVE).grid(row=3, column=1, padx=00, pady=10, sticky="w")

        left_address = Label(left_frame, text="Address", font=("times new roman", 20, "bold"), bg="#1184e8",
                            fg="white").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        address_text = ttk.Combobox(left_frame, textvariable=self.address, font=("times new roman", 13),
                                    state="readonly")
        left_phone = Label(left_frame, text="Phone", font=("times new roman", 20, "bold"), bg="#1184e8",
                             fg="white").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        phone_text = Entry(left_frame, textvariable=self.phone, font=("times new roman", 15, "bold"), bd=5,
                             relief=GROOVE).grid(row=5, column=1, padx=00, pady=10, sticky="w")

        left_water_allowance = Label(left_frame, text="Water Allowance", font=("times new roman", 20, "bold"), bg="#1184e8",
                         fg="white").grid(row=6, column=0, padx=10, pady=10, sticky="w")
        water_allowance_text = Entry(left_frame, textvariable=self.water_allowance, font=("times new roman", 15, "bold"), bd=5,
                         relief=GROOVE).grid(row=6, column=1, padx=00, pady=10, sticky="w")

        left_complain = Label(left_frame, text="Complain", font=("times new roman", 20, "bold"), bg="#1184e8",
                            fg="white").grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.address_text = Text(left_frame, width=25, height=5, font=("", 10), bd=5, relief=GROOVE)
        self.address_text.grid(row=7, column=1, padx=00, pady=10, sticky="w")

        # Button Frame
        btn_frame = Frame(self.master, bd=3, bg="royal blue", relief=RIDGE)
        btn_frame.place(x=10, y=675, width=430)

        btn1 = Button(btn_frame, text="Add", command=self.add_customers, width=10).grid(row=0, column=0, padx=10,
                                                                                        pady=10)
        btn2 = Button(btn_frame, text="Update", command=self.update_customers, width=10).grid(row=0, column=1, padx=10,
                                                                                              pady=10)
        btn3 = Button(btn_frame, command=self.delete_customers, text="Delete", width=10).grid(row=0, column=2, padx=10,
                                                                                              pady=10)
        btn4 = Button(btn_frame, text="Clear", command=self.clear_data, width=10).grid(row=0, column=3, padx=10,
                                                                                       pady=10)

        # RIGHT FRAME
        r_frame = Frame(self.master, bd=3, bg="royal blue", relief=RIDGE)
        r_frame.place(x=500, y=110, width=800, height=610)
        right_title = Label(r_frame, text="Search By", font=("times new roman", 20, "bold"), bg="royal blue",
                            fg="white").grid(row=0, column=0, padx=5, pady=15)

        combo_search = ttk.Combobox(r_frame, textvariable=self.search_by, font=("times new roman", 13),
                                    state="readonly")
        combo_search["values"] = ("custid", "name", "waterallowance")
        combo_search.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        search_text = Entry(r_frame, font=(" ", 12), bd=5, textvariable=self.search_txt, relief=GROOVE).grid(row=0,
                                                                                                             column=2,
                                                                                                             padx=10,
                                                                                                             pady=10,
                                                                                                             sticky="w")

        src_btn1 = Button(r_frame, text="Search", command=self.search_data, width=10, height=2).grid(row=0, column=3,
                                                                                                     padx=10, pady=10)
        shw_btn1 = Button(r_frame, text="Show All", command=self.fetch_data, width=10, height=2).grid(row=0, column=4,
                                                                                                      padx=10, pady=10)

        # Table FRAME
        table_frame = Frame(r_frame, bd=4, relief=RIDGE, bg="royal blue")
        table_frame.place(x=0, y=75, width=790, height=525)

        scrool_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scrool_y = Scrollbar(table_frame, orient=VERTICAL)
        self.customer_table = ttk.Treeview(table_frame,
                                          columns=("cus_id", "name", "area", "address", "phone", "complain", "water_allowance"),
                                          xscrollcommand=scrool_x.set, yscrollcommand=scrool_y.set)
        scrool_x.pack(side=BOTTOM, fill=X)
        scrool_y.pack(side=RIGHT, fill=Y)
        scrool_x.config(command=self.customer_table.xview)
        scrool_y.config(command=self.customer_table.yview)

        self.customer_table.heading("cus_id", text="CustomerId")
        self.customer_table.heading("name", text="Name")
        self.customer_table.heading("area", text="AreaId")
        self.customer_table.heading("address", text="Address")
        self.customer_table.heading("phone", text="Phone")
        self.customer_table.heading("complain", text="Complain")
        self.customer_table.heading("water_allowance", text="WaterAllowance")
        self.customer_table["show"] = "headings"

        self.customer_table.column("cus_id", width=100)
        self.customer_table.column("name", width=100)
        self.customer_table.column("area", width=100)
        self.customer_table.column("address", width=100)
        self.customer_table.column("phone", width=100)
        self.customer_table.column("complain", width=100)
        self.customer_table.column("water_allowance", width=100)
        # self.customer_table.column("address", width=160)

        self.customer_table.pack(fill=BOTH, expand=1)
        self.customer_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()

    def get_cursor(self, ev):
        cursor_row = self.customer_table.focus()
        contents = self.customer_table.item(cursor_row)
        row = contents["values"]
        self.cus_id.set(row[0]),
        self.name.set(row[1]),
        self.area.set(row[2]),
        self.address.set(row[3]),
        self.phone.set(row[4]),
        self.complain.set(row[5]),
        self.adress_text.delete("1.0", END),
        self.adress_text.insert(END, row[6])

    def search_data(self):
        self.results = database.search(str(self.search_by.get()), "1")
        print("TEST", self.results)
        if len(self.results) != 0:
            self.customer_table.delete(*self.customer_table.get_children())
            for self.row in self.results:
                self.customer_table.insert("", END, values=self.row)

    def fetch_data(self):
        self.rows = database.select_customers()
        if len(self.rows) != 0:
            self.customer_table.delete(*self.customer_table.get_children())
            for self.row in self.rows:
                self.customer_table.insert("", END, values=self.row)

    def add_customers(self, customer_id, name, area, address, phone, water_allowance):
        pass

    def update_customers(self):
        pass

    def delete_customers(self):
        pass

    def search_data(self):
        pass

    def clear_data(self):
        pass

    def logout(self):
        pass

    def move_to_employee(self):
        pass

    def move_to_billing(self):
        pass

    def move_to_feedback(self):
        pass

    def move_to_supplier(self):
        pass

    def move_to_service(self):
        pass

    def move_to_area(self):
        pass

    def mouseClick(self):
        pass

    def mainclear(self):
        pass


if __name__ == "__main__":
    root = Tk()
    app = MainApp(root)
    root.mainloop()
