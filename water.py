# import tkinter module
from tkinter import *
from tkinter import font as tkfont
from db import Database
from tkinter import ttk
from tkinter import messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from customers import window

database = Database("water.db")


def center_window(root, width, height):
    positionRight = int(root.winfo_screenwidth()/2 - width/2)
    positionDown = int(root.winfo_screenheight()/2 - height/2 - 60)

    root.geometry("%dx%d+%d+%d" % (width, height, positionRight, positionDown))


class Login:
    def __init__(self):
        self.login = Tk()
        self.login.title('Login')
        self.lb_wel = Label(self.login, text='Welcome!')
        self.lb_wel.pack(pady=5)
        self.frame_login = LabelFrame(self.login, text="Login")
        self.frame_login.pack()
        center_window(self.login, 300, 180)

        def btn_login():
            result = database.login(en_username.get(), en_password.get())
            if result is not None:
                self.login.destroy()
                if result[0][0] == "e":
                    EmployeeWindow(result[0])
                else:
                    window(int(result[0]))

        lb_username = Label(self.frame_login, text='Username')
        lb_username.grid(row=0, column=0)
        en_username = Entry(self.frame_login)
        en_username.grid(row=0, column=1, columnspan=4)

        lb_password = Label(self.frame_login, text='Password')
        lb_password.grid(row=1, column=0)
        en_password = Entry(self.frame_login)
        en_password.grid(row=1, column=1, columnspan=4)

        btn_login = Button(self.frame_login, text='Login', command=btn_login)
        btn_login.grid(row=2, column=0, columnspan=5, pady=5)

        self.login.mainloop()


class WinAdd:
    def __init__(self, root, frame_tables):
        self.frame_table = frame_tables
        self.root = root

        self.labels = []
        self.entries = []
        self.win_add = Toplevel(self.root)
        self.win_add.title('Adding Things')
        center_window(self.win_add, 400, 400)
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
        center_window(self.win_update, 400, 400)
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
            database.delete_row(table_name, row[0])

        self.frame_table.redraw()


class FrameSelectWinChart:
    def __init__(self, root):
        self.root = root
        self.fr_select = LabelFrame()
        self.cbx_values = []
        self.lb_select = Label()
        self.lb_type = Label()
        self.btn_show = Button()
        self.cbx_select = ttk.Combobox()
        self.cbx_type = ttk.Combobox()
        self.btn_done = Button()

    def draw(self, fr_chart, cbx_values):
        self.fr_select = LabelFrame(self.root, text="Selection")
        self.fr_select.pack(fill=X, padx=10, pady=10)
        self.cbx_values = cbx_values
        self.lb_select = Label(self.fr_select, text="Get Info About")
        self.lb_select.grid(row=0, column=0, padx=5, pady=5)
        self.cbx_select = ttk.Combobox(self.fr_select, width=25, values=self.cbx_values)
        self.cbx_select.grid(row=0, column=1, padx=5, pady=5, columnspan=2)
        self.cbx_select.current(0)

        self.lb_type = Label(self.fr_select, text="Type ")
        self.lb_type.grid(row=1, column=0, padx=5, pady=5)
        self.cbx_type = ttk.Combobox(self.fr_select, width=25, values=['gender', 'role'])
        self.cbx_type.grid(row=1, column=1, padx=5, pady=5, columnspan=2)
        self.cbx_type.current(0)

        self.cbx_select.bind("<<ComboboxSelected>>", lambda _: self.change_cbx_type(self.cbx_select.get()))

        self.btn_show = Button(self.fr_select, text="Show",
                               command=lambda: fr_chart.draw([self.cbx_select.get(), self.cbx_type.get()]))
        self.btn_show.grid(row=1, column=3, padx=5, pady=5)

        self.btn_done = Button(self.fr_select, text="Done", command=self.done)
        self.btn_done.grid(row=1, column=4, padx=5, pady=5)

    def change_cbx_type(self, selection):
        if selection == 'employee':
            self.cbx_type['values'] = ['gender', 'role']
        elif selection == 'household':
            self.cbx_type['values'] = ['num in each area']
        elif selection == 'area':
            self.cbx_type['values'] = ['num of each supplier']
        elif selection == 'service':
            self.cbx_type['values'] = ['num of each supplier']
        elif selection == 'billing':
            self.cbx_type['values'] = ['amount of water in each area',
                                       'amount of water of each supplier',
                                       'amount of water of each household',
                                       'amount of money in each area',
                                       'amount of money of each supplier',
                                       'amount of money of each household',
                                       ]

        self.cbx_type.current(0)

    def done(self):
        plt.close('all')
        self.root.destroy()


class FrameChartWinChart:
    def __init__(self, root):
        self.root = root
        self.fr_chart = LabelFrame()
        self.c_type = []

    def draw(self, c_type):
        self.fr_chart.destroy()
        self.fr_chart = LabelFrame(self.root, text="Chart")
        self.fr_chart.pack(fill=X, padx=10, pady=10)
        self.c_type = c_type
        if c_type[0] == 'employee':
            if c_type[1] == 'gender':
                self.draw_chart_emp_gender()
            elif c_type[1] == 'role':
                self.draw_chart_emp_role()
        elif c_type[0] == 'household':
            if c_type[1] == 'num in each area':
                self.draw_chart_hh_in_area()
        elif c_type[0] == 'area':
            if c_type[1] == 'num of each supplier':
                self.draw_chart_area_of_supplier()
        elif c_type[0] == 'service':
            if c_type[1] == 'num of each supplier':
                self.draw_chart_ser_of_supplier()
        elif c_type[0] == 'billing':
            if c_type[1] == 'amount of water in each area':
                self.draw_chart_bill_water_area()
            elif c_type[1] == 'amount of water of each supplier':
                self.draw_chart_bill_water_supplier()
            elif c_type[1] == 'amount of water of each household':
                self.draw_chart_bill_water_hh()
            elif c_type[1] == 'amount of money in each area':
                self.draw_chart_bill_money_area()
            elif c_type[1] == 'amount of money of each supplier':
                self.draw_chart_bill_money_supplier()
            elif c_type[1] == 'amount of money of each household':
                self.draw_chart_bill_money_hh()

    def draw_chart_emp_gender(self):
        f = plt.figure(figsize=(6, 6), dpi=100)
        labels = ['F', 'M']
        values = []
        for label in labels:
            values.append(database.num_emp_gender(label))

        plt.bar(labels, values)
        plt.title(self.c_type[1])

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_emp_role(self):
        f = plt.figure(figsize=(6, 6), dpi=100)
        labels = ['director', 'analyst']
        values = []
        for label in labels:
            values.append(database.num_emp_role(label))

        plt.bar(labels, values)
        plt.title(self.c_type[1])

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_hh_in_area(self):
        f = plt.figure(figsize=(20, 10), dpi=50)

        ids = database.get_all_col_record_in_table('area', 0)
        labels = database.get_all_col_record_in_table('area', 1)
        values = database.num_households_in_area(ids)

        plt.bar(labels, values)
        plt.title(self.c_type[1])

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_area_of_supplier(self):
        f = plt.figure(figsize=(20, 10), dpi=50)

        ids = database.get_all_col_record_in_table('supplier', 0)
        labels = database.get_all_col_record_in_table('supplier', 1)
        values = database.num_area_of_suppliers(ids)

        plt.bar(labels, values)
        plt.title(self.c_type[1])

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_ser_of_supplier(self):
        pass

    def draw_chart_bill_water_area(self):
        f = plt.figure(figsize=(20, 10), dpi=50)
        supplier_ids = database.get_all_col_record_in_table('area', 0)
        results = database.value_consumed_by_suppliers_or_areas([{'area_id': supplier_ids}], "water_consumption")
        labels = database.get_all_col_record_in_table('area', 1)

        values = []
        for result in results:
            values.append(result[1])

        plt.bar(labels, values)
        plt.title(self.c_type[1])

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_bill_water_supplier(self):
        f = plt.figure(figsize=(20, 10), dpi=50)
        supplier_ids = database.get_all_col_record_in_table('supplier', 0)
        results = database.value_consumed_by_suppliers_or_areas([{'area_id': supplier_ids}], "water_consumption")
        labels = database.get_all_col_record_in_table('supplier', 1)

        values = []
        for result in results:
            values.append(result[1])

        plt.bar(labels, values)
        plt.title(self.c_type[1])

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_bill_water_hh(self):
        pass

    def draw_chart_bill_money_area(self):
        f = plt.figure(figsize=(20, 10), dpi=50)
        area_ids = database.get_all_col_record_in_table('area', 0)
        results = database.value_consumed_by_suppliers_or_areas([{'area_id': area_ids}], "total_money")
        labels = database.get_all_col_record_in_table('area', 1)

        values = []
        for result in results:
            values.append(result[1])

        plt.bar(labels, values)
        plt.title(self.c_type[1])

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_bill_money_supplier(self):
        f = plt.figure(figsize=(20, 10), dpi=50)
        supplier_ids = database.get_all_col_record_in_table('supplier', 0)
        results = database.value_consumed_by_suppliers_or_areas([{'area_id': supplier_ids}], "total_money")
        labels = database.get_all_col_record_in_table('supplier', 1)

        values = []
        for result in results:
            values.append(result[1])

        plt.bar(labels, values)
        plt.title(self.c_type[1])

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_bill_money_hh(self):
        pass

    def draw_chart_area(self):
        lb = Label(self.fr_chart, text="Area Chart")
        lb.pack()


class WinCharts:
    def __init__(self, root):
        self.root = root

        self.win_charts = Toplevel(self.root)
        self.win_charts.title('Charts Things')
        center_window(self.win_charts, 1000, 600)

        self.fr_select = FrameSelectWinChart(self.win_charts)
        self.fr_chart = FrameChartWinChart(self.win_charts)

    def draw(self):
        cbx_values = ['employee', 'household', 'area', 'service', 'billing']

        self.fr_select.draw(self.fr_chart, cbx_values)
        self.fr_chart.draw(self.fr_select.cbx_select.get())

        self.win_charts.mainloop()


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
        center_window(self.win_search_results, 700, 400)
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

        self.table_results.pack(fill='both', padx=10, pady=10)


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
        center_window(self.emp_win, 800, 600)
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
