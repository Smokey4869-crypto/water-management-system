from tkinter import *
from tkinter import font as tkfont
from db import Database
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
from customers import CustomerWin

database = Database("water.db")


def center_window(root, width, height):
    positionRight = int(root.winfo_screenwidth() / 2 - width / 2)
    positionDown = int(root.winfo_screenheight() / 2 - height / 2 - 60)

    root.geometry("%dx%d+%d+%d" % (width, height, positionRight, positionDown))


# For Billing only
class WinAdd:
    def __init__(self, root, frame_table, hh_id):
        self.root = root
        self.frame_table = frame_table
        self.hh_id = hh_id

        self.winAdd = Toplevel(root, bg="#ccffcc")
        center_window(self.winAdd, 400, 400)
        self.winAdd.title("Adding Things")

        self.frame_form = LabelFrame()
        self.btn_sub = Button()
        self.labels = []
        self.entries = []

        self.draw()

    def draw(self):
        self.frame_form = LabelFrame(self.winAdd, text="Form", bg="white")
        self.frame_form.place(x=70, y=50)
        columns = database.get_col('billing')
        i_row = 0

        for column in columns:
            lb = Label(self.frame_form, text=column, bg="white")
            lb.grid(row=i_row, column=0, padx=5, pady=5)
            en = Entry(self.frame_form)
            en.grid(row=i_row, column=1, columnspan=4, padx=5, pady=5)
            if column == 'household_id':
                en.insert(0, self.hh_id)
                en['state'] = DISABLED
            self.labels.append(lb)
            self.entries.append(en)

            i_row += 1

        self.btn_sub = Button(self.frame_form, text='Submit', bg="white", command=lambda: self.submit('billing'))
        self.btn_sub.grid(row=i_row, columnspan=5, padx=10, pady=10)

    def submit(self, table_name):
        records = []
        for entry in self.entries:
            records.append(entry.get())
            entry.delete(0, END)
        database.insert_gui(table_name, tuple(records))

        self.frame_table.redraw('billing', 'household_id', self.hh_id)


class WinUpdate:
    def __init__(self, root, fr_table, hh_id):
        self.root = root
        self.fr_table = fr_table
        self.hh_id = hh_id

        self.win_update = Toplevel(root, bg="#ccffcc")
        center_window(self.win_update, 400, 400)
        self.win_update.title("Update Things")

        self.fr_update = LabelFrame()
        self.btn_sub = Button()
        self.entries = []
        self.labels = []

        self.draw()

    def draw(self):
        self.fr_update = LabelFrame(self.win_update, text="Form", bg="white")
        self.fr_update.place(x=100, y=50)
        row = self.fr_table.curr_row
        columns = database.get_col('billing')
        i_row = 0

        for column in columns:
            lb = Label(self.fr_update, text=column, bg="white")
            lb.grid(row=i_row, column=0, padx=5, pady=5)
            en = Entry(self.fr_update)
            en.grid(row=i_row, column=1, columnspan=4, padx=5, pady=5)
            en.insert(END, row[i_row])
            if i_row == 0 or i_row == 1:
                en['state'] = DISABLED
            self.labels.append(lb)
            self.entries.append(en)

            i_row += 1

        self.btn_sub = Button(self.fr_update, text='Submit', bg="white", command=lambda: self.submit('billing'))
        self.btn_sub.grid(row=i_row, columnspan=5, padx=10, pady=10)

    def submit(self, table_name):
        records = []
        for entry in self.entries:
            records.append(entry.get())

        database.delete_row(table_name, records[0])
        database.insert_gui(table_name, tuple(records))

        self.fr_table.redraw('billing', 'household_id', self.hh_id)

        print("To be Update: ", table_name, records)
        self.win_update.destroy()


class WinDelete:
    def __init__(self, root, frame_tables, hh_id):
        self.frame_table = frame_tables
        self.root = root
        self.hh_id = hh_id

        self.draw()

    def draw(self):
        row = self.frame_table.curr_row

        response = messagebox.askquestion("Delete ?", "Do you want to delete ?")
        if response == 'yes':
            database.delete_row('billing', row[0])

        self.frame_table.redraw('billing', 'household_id', self.hh_id)


class FrameSetting:
    def __init__(self, frame, username):
        # self.root = root
        # self.win_sett.title('Change Password')
        self.fr_sett = frame
        self.profile = LabelFrame()
        self.username = username
        self.entries = []
        self.draw()

    def draw(self):
        self.profile = LabelFrame(self.fr_sett, text='Change Password', bg="#ccffcc")
        self.profile.place(x=330, y=50)
        record = database.search_exact('adminlogin', 'username', self.username)[0]
        cols = database.get_col('adminlogin')

        row_id = 0
        for col in cols:
            lb = Label(self.profile, text=col, bg="white")
            lb.grid(row=row_id, column=0, padx=5, pady=5)
            en = Entry(self.profile)
            en.insert(0, record[row_id])
            self.entries.append(en)
            if row_id == 0:
                en['state'] = DISABLED
            en.grid(row=row_id, column=1, padx=5, pady=5)

            row_id += 1

        btn_submit = Button(self.profile, text='submit', command=self.submit, bg="white")
        btn_submit.grid(row=row_id, column=0, columnspan=2, padx=5, pady=5)

    def submit(self):
        records = []
        for entry in self.entries:
            records.append(entry.get())

        database.delete_row('adminlogin', records[0])
        database.insert_gui('adminlogin', tuple(records))

        print("To be Update: ", 'adminlogi ', records)


class FrameFeatureWinEmployee:
    def __init__(self, root, fr_result):
        self.root = root
        self.fr_feature = LabelFrame()
        self.fr_result = fr_result
        self.btn_home = Button()
        self.btn_profile = Button()
        self.btn_mana = Button()
        self.btn_sett = Button()
        self.btn_exit = Button()
        self.btn_logout = Button()

    def draw(self):
        self.fr_feature = LabelFrame(self.root, height=300, width=184.689, bg="#098040", relief="flat")
        self.fr_feature.place(x=100, y=200)
        # Home button
        self.btn_home = Button(self.fr_feature, text="HOME", font=("arial", 10, "bold"), width=22,
                               bg="#098040", fg="white", relief=GROOVE,
                               activebackground="white",
                               command=self.fr_result.home)
        self.btn_home.place(x=-1, y=0)
        # Manage button
        self.btn_mana = Button(self.fr_feature, text="MANAGE", font=("arial", 10, "bold"), width=22,
                               bg="#098040", fg="white", relief=GROOVE,
                               command=self.fr_result.mana)
        self.btn_mana.place(x=-1, y=27)
        # Setting button
        self.btn_sett = Button(self.fr_feature, text="SETTING", font=("arial", 10, "bold"), width=22,
                               bg="#098040", fg="white", relief=GROOVE,
                               command=self.fr_result.setting)
        self.btn_sett.place(x=-1, y=54)
        # Exit button
        self.btn_exit = Button(self.fr_feature, text="EXIT", font=("arial", 10, "bold"), width=22,
                               bg="#098040", fg="white", relief=GROOVE,
                               command=self.fr_result.exit)
        self.btn_exit.place(x=-1, y=81)


class FrameActionWinEmployee:
    def __init__(self, root, frame, emp, fr_table):
        self.root = root
        self.emp = emp
        self.frame = frame
        self.fr_action = LabelFrame()
        self.lb_address = Label()
        self.cbx_address = ttk.Combobox()
        self.lb_hh = Label()
        self.cbx_hh = ttk.Combobox()
        self.btn_search = Button()
        self.fr_table = fr_table

        self.btn_add = Button()
        self.btn_update = Button()
        self.btn_delete = Button()
        self.btn_chart = Button()

        # area_id of employee
        self.area_id = self.emp[6]

    def draw(self):
        self.fr_action = LabelFrame(self.frame, bg="white", relief=FLAT, width=900)
        self.fr_action.place(x=50, y=10)

        # take addresses in area
        values = []
        addresses = database.search_exact('address', 'area_id', self.area_id)
        for address in addresses:
            values.append(address[2])

        self.lb_address = Label(self.fr_action, text="Address", bg="white")
        self.lb_address.grid(row=0, column=0)
        self.cbx_address = ttk.Combobox(self.fr_action, values=values)
        self.cbx_address.grid(row=0, column=1, columnspan=3)

        self.cbx_address.bind("<<ComboboxSelected>>", lambda _: self.change_cbx_hh(self.cbx_address.get()))

        self.lb_hh = Label(self.fr_action, text="Household", bg="white")
        self.lb_hh.grid(row=0, column=4)
        self.cbx_hh = ttk.Combobox(self.fr_action)
        self.cbx_hh.grid(row=0, column=5)

        self.btn_search = Button(self.fr_action, text="Search", command=self.search, bg="#85e085")
        self.btn_search.grid(row=0, column=6, padx=5, pady=5)

        self.btn_add = Button(self.fr_action, text="Add", command=self.add, bg="#85e085")
        self.btn_add.grid(row=1, column=0, padx=5, pady=5)
        self.btn_update = Button(self.fr_action, text="Update", command=self.update, bg="#85e085")
        self.btn_update.grid(row=1, column=1, padx=5, pady=5)
        self.btn_delete = Button(self.fr_action, text="Delete", command=self.delete, bg="#85e085")
        self.btn_delete.grid(row=1, column=2, padx=5, pady=5)
        self.btn_chart = Button(self.fr_action, text="Chart", command=self.chart, bg="#85e085")
        self.btn_chart.grid(row=1, column=3, padx=5, pady=5)

    def change_cbx_hh(self, address):
        # get address_id
        address_id = database.search_exact('address', 'address_name', address)[0][0]

        # get hh by address_id
        households = database.search_exact('household', 'address_id', address_id)
        values = []
        for household in households:
            values.append(household[0])

        self.cbx_hh['values'] = values
        self.cbx_hh.current(0)

    def search(self):
        self.fr_table.redraw('billing', 'household_id', self.cbx_hh.get())

    def add(self):
        WinAdd(self.root, self.fr_table, self.cbx_hh.get())

    def update(self):
        WinUpdate(self.root, self.fr_table, self.cbx_hh.get())

    def delete(self):
        WinDelete(self.root, self.fr_table, self.cbx_hh.get())

    def chart(self):
        pass


class FrameTableWinEmployee:
    def __init__(self, frame):
        # self.root = root
        self.frame = frame
        self.fr_table = LabelFrame()
        self.table_results = ttk.Treeview()
        self.curr_row = []

    # Input ('billing', 'household_id', 'exact', txt)
    def draw(self):
        self.fr_table.destroy()
        self.fr_table = LabelFrame(self.frame, text="Tables", bg="#ccffcc")
        self.fr_table.place(x=50, y=100)

    def redraw(self, table, by_column, txt):
        self.draw()
        tree_scroll = Scrollbar(self.fr_table)
        tree_scroll.pack(side=RIGHT, fill=Y)
        self.table_results = ttk.Treeview(self.fr_table, yscrollcommand=tree_scroll.set, selectmode="extended")
        tree_scroll.config(command=self.table_results.yview)
        columns = database.get_col(table)
        self.table_results['columns'] = columns
        self.table_results.column('#0', width=0, stretch=NO)

        for column in columns:
            self.table_results.column(column, anchor=CENTER, width=105, minwidth=25)
            self.table_results.heading(column, text=column, anchor=CENTER)

        data_results = database.search_exact(table, by_column, txt)

        count_area = 0
        for record in data_results:
            self.table_results.insert(parent='', index='end', iid=count_area, values=record)
            count_area += 1

        self.table_results.bind('<ButtonRelease-1>', lambda _: self.track_row())
        self.table_results.pack(fill='both', padx=10, pady=10)

    def track_row(self):
        curItem = self.table_results.focus()
        self.curr_row = self.table_results.item(curItem)['values']


class FrameResultWinEmployee:
    def __init__(self, root, emp):
        self.root = root
        self.fr_result = LabelFrame()
        self.emp = emp
        self.fr_action = LabelFrame()
        self.fr_table = LabelFrame()
        self.fr_feature = LabelFrame()
        self.home_bg = ImageTk.PhotoImage(Image.open("images//home_frame_emp.png").resize((882, 475), Image.ANTIALIAS))

    def draw(self):
        self.fr_result.destroy()
        self.fr_result = LabelFrame(self.root, width=882, height=475, relief=FLAT, bg="white")
        self.fr_result.place(x=300, y=126)

    def home(self):
        self.fr_result = Label(self.root, image=self.home_bg, relief=FLAT, bg="white")
        self.fr_result.place(x=300, y=126)
        # ====================Info=============
        name = Label(self.fr_result, text=self.emp[1], bg="#a0d4ad", fg="#008662", font=("arial", 14))
        name.place(x=570, y=284)

        desig = Label(self.fr_result, text=self.emp[4], bg="#a0d4ad", fg="#008662", font=("arial", 14))
        desig.place(x=626, y=311)

        id = Label(self.fr_result, text=self.emp[0], bg="#a0d4ad", fg="#008662", font=("arial", 14))
        id.place(x=540, y=338)
        # =================Total households=================
        house_num = database.total_household_by_area(self.emp[6])[0]
        total_households = Label(self.fr_result, text=str(house_num), bg="#a0d4ad", fg="white", font=("arial", 25))
        total_households.place(x=248, y=118)

        # =================Total employees=================
        emp_num = database.total_employee_by_area(self.emp[6])[0]
        total_emps = Label(self.fr_result, text=str(emp_num), bg="#a0d4ad", fg="white", font=("arial", 25))
        total_emps.place(x=598, y=118)

        # =================Total suppliers=================
        unpaid_num = database.total_household_not_paid(self.emp[6])[1]
        total_unpaid = Label(self.fr_result, text=str(unpaid_num), bg="#a0d4ad", fg="white", font=("arial", 25))
        total_unpaid.place(x=253, y=301)

    def mana(self):
        self.draw()

        self.fr_table = FrameTableWinEmployee(self.fr_result)
        self.fr_action = FrameActionWinEmployee(self.root, self.fr_result, self.emp, self.fr_table)
        self.fr_action.draw()
        self.fr_table.draw()

    def setting(self):
        self.draw()
        FrameSetting(self.fr_result, self.emp[0])

    def exit(self):
        self.root.destroy()


class EmployeeWindow:
    def __init__(self, emp_id):
        self.emp_id = emp_id
        self.emp = database.search_exact('employee', 'employee_id', emp_id)[0]
        self.emp_win = Tk()

        self.emp_win.geometry("1300x720")
        self.emp_win.title('Welcome back: ' + self.emp[1] + '!')
        # =======================Set background image=====================
        image = ImageTk.PhotoImage(Image.open("images//Employee_bg.png").resize((1300, 720), Image.ANTIALIAS))
        canvas = Canvas(self.emp_win)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=image, anchor="nw")
        # =============================Log out panel=======================
        # =================================================================
        panel = LabelFrame(self.emp_win, width=800, height=40, bg="white", relief=FLAT)
        panel.place(x=356, y=65)

        welcome = Label(panel, text="Hello, " + self.emp[1], font=("arial", 12), bg='white', fg="#098040")
        welcome.place(x=530, y=9)

        # Log out button
        logout_btn = Button(panel, text="Log Out", command=self.logout, relief=FLAT,
                            font=("arial", 10), bg='white', fg="#098040", activebackground="white")
        logout_btn.place(x=720, y=6)
        self.fr_result = FrameResultWinEmployee(self.emp_win, self.emp)
        self.fr_feature = FrameFeatureWinEmployee(self.emp_win, self.fr_result)
        self.draw()

        self.emp_win.mainloop()

    def draw(self):
        self.fr_feature.draw()
        self.fr_result.home()

    def logout(self):
        from water import Login
        self.emp_win.destroy()
        win = Tk()
        Login(win)


if __name__ == '__main__':
    emp_win = EmployeeWindow('emp3')
