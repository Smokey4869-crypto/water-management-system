# import tkinter module
from tkinter import *
from tkinter import font as tkfont
from db import Database
from tkinter import ttk
from tkinter import messagebox

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
        self.ab = database.check_user_admin(self.var1, self.var2)
        print(self.ab)
        if self.ab != None:
            # messagebox.showinfo('Library System',ab[1])
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

    def move_to_customers(self):
        # ALL VARIABLES##
        self.roll = StringVar()
        self.name = StringVar()
        self.email = StringVar()
        self.gender = StringVar()
        self.contact = StringVar()
        self.dob = StringVar()

        self.search_by = StringVar()
        self.search_txt = StringVar()

        # LEFT FRAME
        left_frame = Frame(self.master, bg='#1184e8')
        left_frame.place(x=0, y=110, width=430, height=690)
        left_title = Label(left_frame, text="Manage Customers", font=("times new roman", 20, "bold"), bg="royal blue",
                           fg="white")
        left_title.grid(row=0, columnspan=2, pady=20)

        left_roll = Label(left_frame, text="Customer Id.", font=("times new roman", 20, "bold"), bg="royal blue",
                          fg="white").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        roll_text = Entry(left_frame, textvariable=self.roll, font=("times new roman", 15, "bold"), bd=5,
                          relief=GROOVE).grid(row=1, column=1, padx=00, pady=10, sticky="w")

        left_name = Label(left_frame, text="Customer Name", font=("times new roman", 20, "bold"), bg="royal blue",
                          fg="white").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        name_text = Entry(left_frame, textvariable=self.name, font=("times new roman", 15, "bold"), bd=5,
                          relief=GROOVE).grid(row=2, column=1, padx=00, pady=10, sticky="w")

        left_email = Label(left_frame, text="Area Id", font=("times new roman", 20, "bold"), bg="royal blue",
                           fg="white").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        email_text = Entry(left_frame, textvariable=self.email, font=("times new roman", 15, "bold"), bd=5,
                           relief=GROOVE).grid(row=3, column=1, padx=00, pady=10, sticky="w")

        left_gender = Label(left_frame, text="Address", font=("times new roman", 20, "bold"), bg="royal blue",
                            fg="white").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        combo_gender = ttk.Combobox(left_frame, textvariable=self.gender, font=("times new roman", 13),
                                    state="readonly")
        left_contact = Label(left_frame, text="Phone", font=("times new roman", 20, "bold"), bg="royal blue",
                             fg="white").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        contact_text = Entry(left_frame, textvariable=self.contact, font=("times new roman", 15, "bold"), bd=5,
                             relief=GROOVE).grid(row=5, column=1, padx=00, pady=10, sticky="w")

        left_dob = Label(left_frame, text="Water Allowance", font=("times new roman", 20, "bold"), bg="royal blue",
                         fg="white").grid(row=6, column=0, padx=10, pady=10, sticky="w")
        dob_text = Entry(left_frame, textvariable=self.dob, font=("times new roman", 15, "bold"), bd=5,
                         relief=GROOVE).grid(row=6, column=1, padx=00, pady=10, sticky="w")

        left_adress = Label(left_frame, text="Complain", font=("times new roman", 20, "bold"), bg="royal blue",
                            fg="white").grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.adress_text = Text(left_frame, width=25, height=5, font=("", 10), bd=5, relief=GROOVE)
        self.adress_text.grid(row=7, column=1, padx=00, pady=10, sticky="w")

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
        self.student_Table = ttk.Treeview(table_frame,
                                          columns=("roll", "name", "email", "gender", "contact", "dob", "address"),
                                          xscrollcommand=scrool_x.set, yscrollcommand=scrool_y.set)
        scrool_x.pack(side=BOTTOM, fill=X)
        scrool_y.pack(side=RIGHT, fill=Y)
        scrool_x.config(command=self.student_Table.xview)
        scrool_y.config(command=self.student_Table.yview)

        self.student_Table.heading("roll", text="CustomerId")
        self.student_Table.heading("name", text="Name")
        self.student_Table.heading("email", text="AreaId")
        self.student_Table.heading("gender", text="Address")
        self.student_Table.heading("contact", text="Phone")
        self.student_Table.heading("dob", text="Complain")
        self.student_Table.heading("address", text="WaterAllowance")
        self.student_Table["show"] = "headings"

        self.student_Table.column("roll", width=100)
        self.student_Table.column("name", width=100)
        self.student_Table.column("email", width=100)
        self.student_Table.column("gender", width=100)
        self.student_Table.column("contact", width=100)
        self.student_Table.column("dob", width=100)
        self.student_Table.column("contact", width=100)
        self.student_Table.column("address", width=160)

        self.student_Table.pack(fill=BOTH, expand=1)
        self.student_Table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()

    def get_cursor(self, ev):
        cursor_row = self.student_Table.focus()
        contents = self.student_Table.item(cursor_row)
        row = contents["values"]
        self.roll.set(row[0]),
        self.name.set(row[1]),
        self.email.set(row[2]),
        self.gender.set(row[3]),
        self.contact.set(row[4]),
        self.dob.set(row[5]),
        self.adress_text.delete("1.0", END),
        self.adress_text.insert(END, row[6])

    def search_data(self):
        self.results = database.search(str(self.search_by.get()), "1")
        print("TEST", self.results)
        if len(self.results) != 0:
            self.student_Table.delete(*self.student_Table.get_children())
            for self.row in self.results:
                self.student_Table.insert("", END, values=self.row)

    def fetch_data(self):
        self.rows = database.select_customers()
        if len(self.rows) != 0:
            self.student_Table.delete(*self.student_Table.get_children())
            for self.row in self.rows:
                self.student_Table.insert("", END, values=self.row)

    def add_customers(self):
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
