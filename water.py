# import tkinter module
from tkinter import *
from tkinter import font as tkfont
from db import Database
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from customers import window

database = Database("water.db")


class Login:
    def __init__(self):
        self.login = Tk()
        self.login.title('Login')

        def btn_login():
            result = database.login(en_username.get(), en_password.get())
            if result is not None:
                self.login.destroy()
                if result[0][0] == "e":
                    EmployeeWindow(result[0])
                else:
                    window(int(result[0]))

        lb_username = Label(self.login, text='Username')
        lb_username.grid(row=0, column=0)
        en_username = Entry(self.login)
        en_username.grid(row=0, column=1, columnspan=4)

        lb_password = Label(self.login, text='Password')
        lb_password.grid(row=1, column=0)
        en_password = Entry(self.login)
        en_password.grid(row=1, column=1, columnspan=4)

        btn_login = Button(self.login, text='Login', command=btn_login)
        btn_login.grid(row=2, column=0, columnspan=5)

        self.login.mainloop()


class WinAdd:
    def __init__(self, root, frame_tables):
        self.frame_table = frame_tables
        self.root = root

        self.labels = []
        self.entries = []
        self.win_add = Toplevel(self.root)
        self.win_add.title('Adding Things')
        self.win_add.geometry('400x400')
        self.frame_select = LabelFrame()
        self.frame_form = LabelFrame(self.win_add, text="Form")
        self.btn_sub = Button()

    def draw(self):
        nb = self.frame_table.get_notebook()
        table_name = nb.tab(nb.select(), "text")
        print(table_name)

        self.frame_form.destroy()
        self.frame_form = LabelFrame(self.win_add, text="Form")
        self.frame_form.pack(padx=10, pady=10)

        columns = database.get_col(table_name)
        i_row = 0

        for column in columns:
            lb = Label(self.frame_form, text=column)
            lb.grid(row=i_row, column=0, padx=5, pady=5)
            en = Entry(self.frame_form)
            en.grid(row=i_row, column=1, columnspan=4, padx=5, pady=5)

            self.labels.append(lb)
            self.entries.append(en)

            i_row += 1

        self.btn_sub = Button(self.frame_form, text='Submit', command=lambda: self.submit(table_name))
        self.btn_sub.grid(row=i_row, columnspan=5, padx=10, pady=10)

    def submit(self, table_name):
        records = []
        for entry in self.entries:
            records.append(entry.get())
            entry.delete(0, END)
        database.insert_gui(table_name, tuple(records))

        self.frame_table.redraw()


class WinUpdate:
    def __init__(self, root, frame_tables):
        self.frame_table = frame_tables
        self.root = root

        self.labels = []
        self.entries = []
        self.win_update = Toplevel(self.root)
        self.win_update.title('Update Things')
        self.win_update.geometry('400x400')
        self.frame_select = LabelFrame()
        self.frame_form = LabelFrame(self.win_update, text="Form")
        self.btn_sub = Button()

    def draw(self):
        nb = self.frame_table.get_notebook()
        table_name = nb.tab(nb.select(), "text")
        row = self.frame_table.curr_row

        self.frame_form.destroy()
        self.frame_form = LabelFrame(self.win_update, text="Form")
        self.frame_form.pack(padx=10, pady=10)

        columns = database.get_col(table_name)
        i_row = 0

        for column in columns:
            lb = Label(self.frame_form, text=column)
            lb.grid(row=i_row, column=0, padx=5, pady=5)
            en = Entry(self.frame_form)
            en.grid(row=i_row, column=1, columnspan=4, padx=5, pady=5)
            en.insert(END, row[i_row])
            if i_row == 0:
                en['state'] = DISABLED
            self.labels.append(lb)
            self.entries.append(en)

            i_row += 1

        self.btn_sub = Button(self.frame_form, text='Submit', command=lambda: self.submit(table_name))
        self.btn_sub.grid(row=i_row, columnspan=5, padx=10, pady=10)

    def submit(self, table_name):
        records = []
        for entry in self.entries:
            records.append(entry.get())

        database.delete_row(table_name, records[0])
        database.insert_gui(table_name, tuple(records))

        self.frame_table.redraw()

        print("To be Update: ", table_name, records)
        self.win_update.destroy()


class WinDelete:
    def __init__(self, root, frame_tables):
        self.frame_table = frame_tables
        self.root = root

    def draw(self):
        nb = self.frame_table.get_notebook()
        table_name = nb.tab(nb.select(), "text")
        row = self.frame_table.curr_row

        response = messagebox.askquestion("Delete ?", "Do you want to delete ?")
        if response == 'yes':
            # database.delete_row(table_name, row[0])
            print("To be Deleted: ", table_name, row)
            database.delete_row(table_name, row[0])

        self.frame_table.redraw()


class WinCharts:
    def __init__(self, root):
        self.root = root

        self.win_charts = Toplevel(self.root)
        self.win_charts.title('Charts Things')
        self.win_charts.geometry('400x400')

    def draw(self):
        lb = Label(self.win_charts, text="This is chart window")
        lb.pack()


class FrameFeatures:
    def __init__(self, root, frame_tables):
        self.frame_tables = frame_tables
        self.root = root
        self.frame_features = LabelFrame(self.root, text="Features")
        self.frame_features.pack(fill=X, padx=10)

        self.btn_add = Button()
        self.btn_update = Button()
        self.btn_delete = Button()
        self.btn_charts = Button()

    def draw(self):
        # Button Add
        self.btn_add = Button(self.frame_features, text='Add', width=12, height=1, command=lambda: self.add())
        self.btn_add.grid(row=0, column=0, padx=5, pady=5)

        # Button Update
        self.btn_update = Button(self.frame_features, text='Update', width=12, height=1, command=lambda: self.update())
        self.btn_update.grid(row=0, column=1, padx=5, pady=5)

        # Button Delete
        self.btn_delete = Button(self.frame_features, text='Delete', width=12, height=1, command=lambda: self.delete())
        self.btn_delete.grid(row=0, column=2, padx=5, pady=5)

        # Button Charts
        self.btn_charts = Button(self.frame_features, text='Chart', width=12, height=1, command=lambda: self.charts())
        self.btn_charts.grid(row=0, column=3, padx=5, pady=5)

    def add(self):
        win_add = WinAdd(self.root, self.frame_tables)
        win_add.draw()

    def update(self):
        win_update = WinUpdate(self.root, self.frame_tables)
        win_update.draw()

    def delete(self):
        win_delete = WinDelete(self.root, self.frame_tables)
        win_delete.draw()

    def charts(self):
        win_charts = WinCharts(self.root)
        win_charts.draw()


class WinSearchResults:
    def __init__(self, root):
        self.root = root
        self.win_search_results = Toplevel(self.root)
        self.win_search_results.title('Search Results')
        self.table_results = ttk.Treeview()

    def draw(self, table, by_column, opt, txt):
        self.table_results = ttk.Treeview(self.win_search_results)
        columns = database.get_col(table)
        self.table_results['columns'] = columns

        self.table_results.column('#0', width=0, stretch=NO)

        for column in columns:
            self.table_results.column(column, anchor=CENTER, width=105, minwidth=25)
            self.table_results.heading(column, text=column, anchor=CENTER)

        data_results = []
        if opt == 'exact':
            data_results = database.search_exact(table, by_column, txt)
        elif opt == 'contains':
            data_results = database.search(table, by_column, txt)

        count_area = 0
        for record in data_results:
            self.table_results.insert(parent='', index='end', iid=count_area, values=record)
            count_area += 1

        self.table_results.pack(fill='both')


class FrameSearch:
    def __init__(self, root):
        self.root = root
        self.frame_search = LabelFrame(self.root, text='Search')
        self.frame_search.pack(fill=X, padx=10)
        self.cbx_tbl_search = ttk.Combobox()
        self.cbx_col_search = ttk.Combobox()
        self.cbx_opt_search = ttk.Combobox()
        self.en_search = Entry()
        self.btn_search = Button()

    def draw(self, table_names):
        self.cbx_tbl_search = ttk.Combobox(self.frame_search, width=10, values=table_names)
        self.cbx_tbl_search.current(0)
        self.cbx_tbl_search.grid(row=0, column=0, padx=5, pady=5)
        self.cbx_tbl_search.bind("<<ComboboxSelected>>", lambda _: self.change_cbx_col())

        columns = database.get_col(table_names[0])
        self.cbx_col_search = ttk.Combobox(self.frame_search, width=10, values=columns)
        self.cbx_col_search.current(0)
        self.cbx_col_search.grid(row=0, column=1, padx=5, pady=5)

        self.cbx_opt_search = ttk.Combobox(self.frame_search, width=10, values=['exact', 'contains'])
        self.cbx_opt_search.current(0)
        self.cbx_opt_search.grid(row=0, column=2, padx=5, pady=5)

        self.en_search = Entry(self.frame_search, width=25)
        self.en_search.grid(row=0, column=3, padx=5, pady=5)
        self.btn_search = Button(self.frame_search, text='Search', command=lambda: self.search())
        self.btn_search.grid(row=0, column=4, padx=5, pady=5)

    def search(self):
        curr_tbl = self.cbx_tbl_search.get()
        curr_col = self.cbx_col_search.get()
        curr_opt = self.cbx_opt_search.get()
        curr_txt = self.en_search.get()

        win_search_results = WinSearchResults(self.root)
        win_search_results.draw(curr_tbl, curr_col, curr_opt, curr_txt)

    def change_cbx_col(self):
        columns = database.get_col(self.cbx_tbl_search.get())
        self.cbx_col_search['values'] = columns
        self.cbx_col_search.current(0)


class FrameTable:
    def __init__(self, root, table_names):
        self.root = root
        self.frame_tables = LabelFrame()
        self.table_names = table_names

        self.notebook = ttk.Notebook()
        self.tabs = []
        self.tables = []
        self.btn_redraw = Button()

        self.curr_row = []

    def get_notebook(self):
        return self.notebook

    def draw(self):
        self.frame_tables = LabelFrame(self.root, text="Tables")
        self.frame_tables.pack(fill=X, padx=10)

        self.notebook = ttk.Notebook(self.frame_tables)
        self.notebook.pack(pady=15)

        for table_name in self.table_names:
            self.draw_tab(table_name)

    def redraw(self):
        self.frame_tables.destroy()
        self.draw()

    def draw_tab(self, table_name):
        tab = Frame(self.notebook, width=500, height=300)
        tab.pack(fill="both", expand=True)

        self.draw_table(tab, table_name)

    def draw_table(self, tab, table_name):
        self.notebook.add(tab, text=table_name)
        table = ttk.Treeview(tab, height=10)
        columns = database.get_col(table_name)
        table['columns'] = columns

        # Draw Cols
        table.column('#0', width=0, stretch=NO)
        for column in columns:
            table.column(column, anchor=CENTER, width=105, minwidth=25)
            table.heading(column, text=column, anchor=CENTER)

        # Draw Data
        data = database.show_table(table_name)
        count = 0
        for record in data:
            table.insert(parent='', index='end', iid=count, values=record)
            count += 1

        table.bind('<ButtonRelease-1>', lambda _: self.track_row(table))
        table.pack(fill='both')

    def track_row(self, table):
        curItem = table.focus()
        self.curr_row = table.item(curItem)['values']


class EmployeeWindow:
    def __init__(self, emp):
        self.emp = database.search('employee', 'employee_id', emp)
        self.emp_win = Tk()
        self.emp_win.geometry('800x600')
        self.emp_win.title('Welcome back: ' + self.emp[0][1] + ' !')
        self.table_names = ['supplier', 'household', 'employee', 'billing', 'area', 'service']
        self.tables = []

        self.frame_features = LabelFrame()
        self.frame_search = LabelFrame()
        self.frame_tables = FrameTable(self.emp_win, self.table_names)

        self.draw()

    def draw(self):
        self.frame_features = FrameFeatures(self.emp_win, self.frame_tables)
        self.frame_features.draw()

        self.frame_search = FrameSearch(self.emp_win)
        self.frame_search.draw(self.table_names)

        # Table Frame
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Treeview', rowheight=35)

        self.frame_tables.draw()

        self.emp_win.mainloop()


Login = Login()
# emp_win = EmployeeWindow(1)
