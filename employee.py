from tkinter import *
from db import Database
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
from tkinter import messagebox

database = Database("database/water_database.db")


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

        self.winAdd = Toplevel(self.root)
        self.labels = []
        self.entries = []
        self.winAdd.title('Adding Things')
        center_window(self.winAdd, 400, 400)
        # self.winAdd.geometry("400x400")
        self.winAdd.resizable(False, False)
        self.frame = Label()
        self.add_bg = ImageTk.PhotoImage(Image.open("images//WinAddUpdate_emp.png").resize((400, 400), Image.ANTIALIAS))
        self.sub_btn = ImageTk.PhotoImage(Image.open("images//Sub_btn_emp.png").resize((90, 30), Image.ANTIALIAS))
        self.frame_form = LabelFrame()
        self.btn_sub = Button()

        self.draw()

    def draw(self):
        if len(self.hh_id) != 1:
            self.winAdd.destroy()
            messagebox.showwarning(title=None, message='Please pick a Household Id')
        else:
            self.frame = Label(self.winAdd, image=self.add_bg, bg="white", relief=FLAT)
            self.frame.place(x=0, y=0)
            self.frame_form = LabelFrame(self.frame, bg="#d1e7c5", relief=FLAT)
            self.frame_form.place(x=70, y=75)

            columns = database.get_col('billing')
            i_row = 0

            for column in columns:
                lb = Label(self.frame_form, text=column, bg="#d1e7c5", font=("Calibri", 10))
                lb.grid(row=i_row, column=0, padx=5, pady=5)
                en = Entry(self.frame_form)
                en.grid(row=i_row, column=1, columnspan=4, padx=5, pady=5)
                if column == 'billing_id':
                    en.insert(0, database.max_billing() + 1)
                if column == 'household_id':
                    en.insert(0, self.hh_id)
                    en['state'] = DISABLED
                self.labels.append(lb)
                self.entries.append(en)

                i_row += 1
            self.btn_sub = Button(self.frame_form, image=self.sub_btn, bg="#d1e7c5", relief=FLAT,
                                  command=lambda: self.submit('billing'), activebackground="#d1e7c5")
            self.btn_sub.grid(row=i_row, columnspan=5, padx=10, pady=10)

    def submit(self, table_name):
        columns = database.get_col(table_name)
        duplicate = database.search_exact(table_name, columns[0], self.entries[0].get())
        if len(duplicate) == 0:
            records = []
            for i in range(len(self.entries)):
                entry = self.entries[i]
                records.append(entry.get())
                entry.delete(0, END)
                if i == 0:
                    entry.insert(0, database.max_billing() + 2)
            database.insert_gui(table_name, tuple(records))

            self.frame_table.redraw('billing', 'household_id', self.hh_id)
        else:
            messagebox.showwarning(title=None, message='Duplicated Id')


class WinUpdate:
    def __init__(self, root, fr_table, hh_id):
        self.root = root
        self.fr_table = fr_table
        self.hh_id = hh_id

        self.win_update = Toplevel(root)
        self.win_update.title("Update Things")
        center_window(self.win_update, 400, 400)
        # self.win_update.geometry("400x400")
        self.win_update.resizable(False, False)
        self.frame = Label()
        self.add_bg = ImageTk.PhotoImage(Image.open("images//WinAddUpdate_emp.png").resize((400, 400), Image.ANTIALIAS))
        self.sub_btn = ImageTk.PhotoImage(Image.open("images//Sub_btn_emp.png").resize((90, 30), Image.ANTIALIAS))

        self.fr_update = LabelFrame()
        self.btn_sub = Button()
        self.entries = []
        self.labels = []

        self.draw()

    def draw(self):
        row = self.fr_table.curr_row
        if len(row) == 0:
            self.win_update.destroy()
            messagebox.showwarning(title=None, message='Please pick a Record')
        else:
            self.frame = Label(self.win_update, image=self.add_bg, bg="white", relief=FLAT)
            self.frame.place(x=0, y=0)
            self.fr_update = LabelFrame(self.win_update, bg="#d1e7c5", relief=FLAT)
            self.fr_update.place(x=70, y=75)
            row = self.fr_table.curr_row

            columns = database.get_col('billing')
            i_row = 0

            for column in columns:
                lb = Label(self.fr_update, text=column, bg="#d1e7c5", font=("Calibri", 10))
                lb.grid(row=i_row, column=0, padx=5, pady=5)
                en = Entry(self.fr_update)
                en.grid(row=i_row, column=1, columnspan=4, padx=5, pady=5)
                en.insert(END, row[i_row])
                if i_row == 0 or i_row == 1:
                    en['state'] = DISABLED
                self.labels.append(lb)
                self.entries.append(en)

                i_row += 1

            self.btn_sub = Button(self.fr_update, image=self.sub_btn, bg="#d1e7c5", relief=FLAT,
                                  command=lambda: self.submit('billing'), activebackground="#d1e7c5")
            self.btn_sub.grid(row=i_row, columnspan=5, padx=10, pady=10)

    def submit(self, table_name):
        records = []
        for entry in self.entries:
            records.append(entry.get())

        database.update(table_name, records, records[0])
        # database.delete_row(table_name, records[0])
        # database.insert_gui(table_name, tuple(records))

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
        if len(row) == 0:
            messagebox.showwarning(title=None, message='Please pick a Record')
        else:
            response = messagebox.askquestion("Delete ?", "Do you want to delete ?")
            if response == 'yes':
                database.delete_row('billing', row[0])

            self.frame_table.redraw('billing', 'household_id', self.hh_id)


class FrameSelectWinCharts:
    def __init__(self, win_chart):
        self.win_chart = win_chart
        self.fr_select = LabelFrame()
        self.lb_select = Label()
        self.cbx_select = ttk.Combobox()
        self.lb_type = Label()
        self.cbx_type = ttk.Combobox()

        self.btn_show = Button()

    def draw(self, fr_chart, values):
        self.fr_select = LabelFrame(self.win_chart, bg="#bfffc0", relief=FLAT)
        self.fr_select.place(x=50, y=50)

        self.lb_select = Label(self.fr_select, text="Get Info About", bg="#bfffc0")
        self.lb_select.grid(row=0, column=0)
        self.cbx_select = ttk.Combobox(self.fr_select, values=values)
        self.cbx_select.grid(row=0, column=1)
        self.cbx_select.current(0)

        self.lb_type = Label(self.fr_select, text="Type", bg="#bfffc0")
        self.lb_type.grid(row=1, column=0)
        self.cbx_type = ttk.Combobox(self.fr_select, values=['in each address'])
        self.cbx_type.grid(row=1, column=1)
        self.cbx_type.current(0)

        self.btn_show = Button(self.fr_select, text="Show", bg="#bfffc0",
                               command=lambda: fr_chart.draw([self.cbx_select.get(), self.cbx_type.get()]))
        self.btn_show.grid(row=1, column=2)

        self.cbx_select.bind("<<ComboboxSelected>>", lambda _: self.change_cbx_type(self.cbx_select.get()))

    def change_cbx_type(self, selection):
        if selection == 'household':
            self.cbx_type['values'] = ['in each address']
        elif selection == 'water':
            self.cbx_type['values'] = ['in each address', 'in each household']
        elif selection == 'money':
            self.cbx_type['values'] = ['in each address', 'in each household']

        self.cbx_type.current(0)


class FrameChartWinCharts:
    def __init__(self, root, emp):
        self.root = root
        self.fr_chart = LabelFrame()
        self.c_type = []
        self.emp = emp

    def draw(self, c_type):
        plt.close('all')
        self.fr_chart.destroy()
        self.fr_chart = LabelFrame(self.root, bg="#bfffc0", relief=FLAT)
        self.fr_chart.place(x=60, y=170)
        self.c_type = c_type

        if self.c_type[0] == 'household':
            if self.c_type[1] == 'in each address':
                self.draw_chart_hh_address()
        elif self.c_type[0] == 'water':
            if self.c_type[1] == 'in each address':
                self.draw_chart_water_address()
            elif self.c_type[1] == 'in each household':
                self.draw_chart_water_hh()
        elif self.c_type[0] == 'money':
            if self.c_type[1] == 'in each address':
                self.draw_chart_money_address()
            elif self.c_type[1] == 'in each household':
                self.draw_chart_money_hh()

    def draw_chart_hh_address(self):
        f = plt.figure(figsize=(6, 4), dpi=80)
        f.patch.set_facecolor('#bfffc0')
        addresses = database.search_exact('address', 'area_id', self.emp[6])
        labels = []
        ids = []
        for address in addresses:
            labels.append(address[2])
            ids.append(address[0])
        values = database.num_of_value('household', [{'address_id': ids}])

        plt.bar(labels, values)
        plt.xlabel("Addresses in the area")
        plt.ylabel("Number of households")
        plt.title("Number of households in each address")

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def draw_chart_water_address(self):
        f = plt.figure(figsize=(6, 4), dpi=80)
        f.patch.set_facecolor('#bfffc0')
        addresses = database.search_exact('address', 'area_id', self.emp[6])
        labels = []
        ids = []
        for address in addresses:
            labels.append(address[2])
            ids.append(address[1])
        values = []
        avg_by_addresses = database.average_water_by_address(ids)
        for record in avg_by_addresses:
            values.append(record[1])

        print(labels)
        plt.bar(labels, values)
        plt.xlabel("Addresses in the area")
        plt.ylabel("Amount of water")
        plt.title("Water spent in each address")

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()
        print('water_address')

    def draw_chart_water_hh(self):
        f = plt.figure(figsize=(6, 4), dpi=80)
        f.patch.set_facecolor('#bfffc0')

        addresses = database.search_exact('address', 'area_id', self.emp[6])
        address_ids = []
        for address in addresses:
            address_ids.append(address[0])

        household_ids = []
        labels = []
        for id_ in address_ids:
            households = database.search_exact('household', 'address_id', id_)
            for household in households:
                labels.append('HH' + str(household[0]))
                household_ids.append(household[0])
                print(labels)

        values = []
        records = database.average_water_by_household(household_ids)
        for record in records:
            values.append(record[1])

        plt.bar(labels, values)
        plt.xlabel("Households in the area")
        plt.ylabel("Amount of water")
        plt.title("Water spent in each household")

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()
        print('water_hh')

    def draw_chart_money_address(self):
        f = plt.figure(figsize=(6, 4), dpi=80)
        f.patch.set_facecolor('#bfffc0')

        labels = []
        ids = []
        addresses = database.search_exact('address', 'area_id', self.emp[6])
        for address in addresses:
            labels.append(address[2])
            ids.append(address[1])

        values = []
        avg_by_addresses = database.average_money_by_address(ids)
        for record in avg_by_addresses:
            values.append(record[1])

        plt.bar(labels, values)
        plt.xlabel("Addresses in the area")
        plt.title("Money spent in each address")

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()
        print('money_address')

    def draw_chart_money_hh(self):
        f = plt.figure(figsize=(6, 4), dpi=80)
        f.patch.set_facecolor('#bfffc0')

        addresses = database.search_exact('address', 'area_id', self.emp[6])
        address_ids = []
        for address in addresses:
            address_ids.append(address[0])

        household_ids = []
        labels = []
        for id_ in address_ids:
            households = database.search_exact('household', 'address_id', id_)
            for household in households:
                labels.append('HH' + str(household[0]))
                household_ids.append(household[0])
                print(labels)

        values = []
        records = database.average_money_by_household(household_ids)
        for record in records:
            values.append(record[1])

        plt.bar(labels, values)
        plt.xlabel("Households in the area")
        plt.title("Money spent in each household")

        canvas = FigureCanvasTkAgg(f, self.fr_chart)
        canvas.draw()
        canvas.get_tk_widget().pack()
        print('money_hh')


class WinCharts:
    def __init__(self, root, emp):
        self.root = root
        self.emp = emp
        self.win_chart = Toplevel(root)
        center_window(self.win_chart, 600, 600)
        # self.win_chart.geometry("600x600")
        self.win_chart.title("Chart Chart Chart")
        self.win_chart.resizable(False, False)
        self.chart_bg = ImageTk.PhotoImage(Image.open("images//Chart_emp-01.png").resize((600, 600), Image.ANTIALIAS))
        self.frame = Label(self.win_chart, image=self.chart_bg, bg="white", relief=FLAT)
        self.frame.place(x=0, y=0)
        self.fr_select = FrameSelectWinCharts(self.win_chart)
        self.fr_chart = FrameChartWinCharts(self.win_chart, self.emp)

        self.draw()

    def draw(self):
        values = ['household', 'water', 'money']

        self.fr_select.draw(self.fr_chart, values)
        self.fr_chart.draw(self.fr_select.cbx_select.get())

        self.win_chart.mainloop()


class FrameSetting:
    def __init__(self, root, username):
        self.root = root
        self.setting_frame = LabelFrame()
        self.username = username
        self.entries = []
        self.image_fr = ImageTk.PhotoImage(Image.open("images//Change_pass_emp.png")
                                           .resize((882, 475), Image.ANTIALIAS))
        self.sub_btn = ImageTk.PhotoImage(Image.open("images//Sub_btn_emp.png").resize((90, 30), Image.ANTIALIAS))
        self.draw()

    def draw(self):
        # self.profile = LabelFrame(self.fr_sett, text='Change Password', bg="#ccffcc")
        # self.profile.place(x=330, y=50)
        # record = database.search_exact('adminlogin', 'username', self.username)[0]
        # cols = database.get_col('adminlogin')
        self.setting_frame = Label(self.root, image=self.image_fr, bg="white", relief=FLAT)
        self.setting_frame.place(x=300, y=126)

        record = database.search_exact('adminlogin', 'username', self.username)[0]

        user_entry = Entry(self.setting_frame, relief="flat", width=21, font=("Calibri", 12), bg="#d1e7c5")
        user_entry.place(x=340, y=180)
        user_entry.insert(0, record[0])
        user_entry['state'] = DISABLED
        self.entries.append(user_entry)

        pass_entry = Entry(self.setting_frame, relief="flat", width=21, font=("Calibri", 12), bg="#d1e7c5")
        pass_entry.place(x=340, y=260)
        pass_entry.insert(0, record[1])
        self.entries.append(pass_entry)

        btn_submit = Button(self.setting_frame, image=self.sub_btn, command=self.submit, relief=FLAT, bg="#d1e7c5",
                            activebackground="#d1e7c5")
        btn_submit.place(x=390, y=330)

    def submit(self):
        records = []
        for entry in self.entries:
            records.append(entry.get())

        print(records)
        database.update('adminlogin', records, records[0])

        messagebox.showinfo(title=None, message='Changing Password Successfully')


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
        values = ["All Results"]
        addresses = database.search_exact('address', 'area_id', self.area_id)
        for address in addresses:
            values.append(address[2])

        self.lb_address = Label(self.fr_action, text="Address", bg="white")
        self.lb_address.grid(row=0, column=0)
        self.cbx_address = ttk.Combobox(self.fr_action, values=values)
        self.cbx_address.grid(row=0, column=1, columnspan=3)
        self.cbx_address.current(0)

        self.cbx_address.bind("<<ComboboxSelected>>", lambda _: self.change_cbx_hh(self.cbx_address.get()))

        self.lb_hh = Label(self.fr_action, text="Household", bg="white")
        self.lb_hh.grid(row=0, column=4)
        self.cbx_hh = ttk.Combobox(self.fr_action)
        self.cbx_hh.grid(row=0, column=5)
        self.cbx_hh['values'] = ['All Results']
        self.cbx_hh.current(0)

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
        if address == "All Results":
            values = ["All Results"]
            self.cbx_hh['values'] = values
            self.cbx_hh.current(0)
        else:
            values = []
            # get address_id
            address_id = database.search_exact('address', 'address_name', address)[0][0]

            # get hh by address_id
            households = database.search_exact('household', 'address_id', address_id)
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
        WinCharts(self.root, self.emp)


class FrameTableWinEmployee:
    def __init__(self, emp, frame):
        self.emp = emp
        self.frame = frame
        self.fr_table = LabelFrame()
        self.table_results = ttk.Treeview()
        self.curr_row = []

    def draw(self):
        self.fr_table.destroy()
        self.fr_table = LabelFrame(self.frame, text="Tables", bg="#ccffcc")
        self.fr_table.place(x=50, y=100)

    def redraw(self, table, by_column, txt):
        if txt == "All Results":
            self.draw_all_results(table)
        else:
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

    def draw_all_results(self, table):
        self.draw()
        area_id = self.emp[6]
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

        households = database.households_by_area(area_id)
        ids = []
        for household in households:
            ids.append(household[0])

        data_results = []
        for id_ in ids:
            data_results += database.search_exact('billing', 'household_id', id_)
        data_results = sorted(data_results, key=lambda x: x[0])

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
        name = Label(self.fr_result, text=self.emp[1], bg="#a0d4ad", fg="#008662", font=("arial", 13))
        name.place(x=560, y=286)

        desig = Label(self.fr_result, text=self.emp[4], bg="#a0d4ad", fg="#008662", font=("arial", 13))
        desig.place(x=613, y=313)

        id_ = Label(self.fr_result, text=self.emp[0], bg="#a0d4ad", fg="#008662", font=("arial", 13))
        id_.place(x=530, y=341)
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

        self.fr_table = FrameTableWinEmployee(self.emp, self.fr_result)
        self.fr_action = FrameActionWinEmployee(self.root, self.fr_result, self.emp, self.fr_table)
        self.fr_action.draw()
        self.fr_table.draw_all_results('billing')

    def setting(self):
        self.draw()
        FrameSetting(self.root, self.emp[0])

    def exit(self):
        self.root.deiconify()
        ask = messagebox.askyesnocancel("Confirm Exit", "Are you sure you want to Exit?")
        if ask is True:
            self.root.destroy()


class EmployeeWindow:
    def __init__(self, emp_id):
        self.emp_id = emp_id
        self.emp = database.search_exact('employee', 'employee_id', emp_id)[0]
        self.emp_win = Tk()

        # self.emp_win.geometry("1300x720")
        center_window(self.emp_win, 1300, 720)
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
        ask = messagebox.askyesnocancel("Confirm Logout", "Are you sure you want to Log Out")
        if ask is True:
            from water import Login
            self.emp_win.destroy()
            win = Tk()
            Login(win)


if __name__ == '__main__':
    emp_win = EmployeeWindow('emp3')
