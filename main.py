import curses
from math import *
import datetime
from math import floor
from decimal import Decimal
from threading import Timer
import time
# time in sec of showing
# feedback message to a user
import npyscreen
from test import Database

FEEDBACK_TIMEOUT = 6


class FieldText(npyscreen.Pager):
    def __init__(self, *args, **kwargs):
        kwargs["height"] = kwargs["text"].count("\n") + 1
        kwargs["values"] = kwargs["text"].split("\n")
        kwargs["name"] = "no bullshit please"
        kwargs["autowrap"] = True
        kwargs["editable"] = False
        del (kwargs["text"])

        npyscreen.Pager.__init__(self, *args, **kwargs)


class GridSettings(object):
    def __init__(self):
        self.limit = 5
        self.sort_direction = 'ASC'
        self.offset = 0
        self.table = ''
        self.sort_column = ''

        self.columns_list = []
        # contains all the fetched data (up to 10 rows of data)
        self.rows = []
        # location of the currently edited cell
        self.edit_cell = []
        # database engine type
        self.db_type = ''
        self.row_count = 0


class WelcomeList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(WelcomeList, self).__init__(*args, **keywords)

    def display_value(self, value):
        return "%s" % value

    def actionHighlighted(self, act_on_this, keypress):
        # get name of selected option
        selection = act_on_this
        if selection == 'Go To Table':
            self.parent.parentApp.switchForm('TableSelect')
        elif selection == 'About Us':
            self.parent.parentApp.switchForm('AboutUs')
        elif selection == 'Exit Application':
            self.parent.parentApp.exit_application()
        else:
            self.parent.parentApp.switchForm(None)


class WelcomeSelectForm(npyscreen.ActionFormMinimal):
    OK_BUTTON_TEXT = "Exit"

    def create(self):
        self.action = self.add(WelcomeList, max_height=3,
                               name='Welcome To Water Management System',
                               values=['Go To Table', 'About Us', 'Exit Application', ],
                               scroll_exit=True)
        self.nextrely += 1

        # define exit on Esc
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.parentApp.exit_application

    def on_ok(self):
        self.parentApp.switchForm(None)
        self.parentApp.switchFormNow()


class TableList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(TableList, self).__init__(*args, **keywords)

    def display_value(self, value):
        return "%s" % (value[0])

    def actionHighlighted(self, act_on_this, keypress):
        # get name of selected table
        selectedTableName = act_on_this[0]
        del self.parent.parentApp.tabMenuF
        self.parent.parentApp.tabMenuF = self.parent.parentApp.addForm('Menu', TableMenuForm)

        # save the name of selected table in settings object
        self.parent.parentApp.myGridSet.table = selectedTableName
        # initialize TableMenuForm object attributes and switch to TableMenuForm
        self.parent.parentApp.getForm('Menu').value = selectedTableName
        print(selectedTableName)
        self.parent.parentApp.switchForm('Menu')


class TableListDisplay(npyscreen.ActionFormMinimal):
    OK_BUTTON_TEXT = "Back"

    # Create Widgets
    def create(self):
        self.action = self.add(TableList,
                               name='Select Table',
                               scroll_exit=True)
        self.nextrely += 1

        # define action on Esc
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.on_ok

    def beforeEditing(self):
        self.update_list()

    # populate wMain.values with list of tables in the database
    def update_list(self):
        self.action.values = self.parentApp.db.list_tables()

    def on_ok(self):
        self.parentApp.switchForm('MAIN')
        self.parentApp.switchFormNow()


class AboutUsListDisplay(npyscreen.ActionFormMinimal):
    OK_BUTTON_TEXT = "Back"

    def create(self):
        self.add(FieldText,
                 text=" Members\n Lu Khanh Huyen\n Nguyen Quang Anh\n Nguyen Xuan Tung\n Tran Hong Quan\n Vu Duc Chinh")
        self.nextrely += 1
        self.add(FieldText, text=" Group\n 3\n")
        self.nextrely += 1
        self.add(FieldText, text=" Group Project Name\n Water Supply Management System")

        # define action on Esc
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.on_ok

    def on_ok(self):
        self.parentApp.switchForm('MAIN')
        self.parentApp.switchFormNow()


# class TableOptionList(npyscreen.MultiLineAction):
#     def __init__(self, *args, **keywords):
#         super(TableOptionList, self).__init__(*args, **keywords)
#
#     def display_value(self, value):
#         return "%s" % value
#
#     def actionHighlighted(self, act_on_this, keypress):
#         # get name of selected option
#         selection = act_on_this
#         if selection == 'Add Row':
#             self.parent.parentApp.switchForm('Add Row')
#         elif selection == 'Edit Row':
#             self.parent.parentApp.switchForm('Edit Row')
#         elif selection == 'Delete Row':
#             self.parent.parentApp.switchForm('Delete Row')
#         elif selection == 'Select Another Table':
#             self.parent.parentApp.switchForm('TableSelect')
#         elif selection == 'Exit Application':
#             self.parent.parentApp.tabMenuF.exit_application()
#         else:
#             self.parent.parentApp.switchForm(None)


class TableMenuForm(npyscreen.ActionForm):
    # set screen redirection based on user choice
    CANCEL_BUTTON_TEXT = "Back"

    # Create Widgets
    def create(self):
        self.page = 0
        self.colnames = []
        self.results = []

        # self.nextrely += 1
        # self.action = self.add(TableOptionList, max_height=6,
        #                        name='Select Action',
        #                        values=['Add Row', 'Edit Row', 'Delete Row', 'Select Another Table', 'Exit Application'],
        #                        scroll_exit=True
        #                        )

        # can try another way, this is ugly
        self.SQL_display = self.add(npyscreen.SelectOne, max_height=17, editable=True, scroll_exit=True,
                                    select_whole_line=True, rely=(4))

        # display column name
        self.col_display = self.add(npyscreen.FixedText, rely=(2))

        self.add_btn = self.add(npyscreen.ButtonPress, max_width=10, name='[Add]', relx=-73, rely=-5)
        self.add_btn.whenPressed = self.addRow

        self.edit_btn = self.add(npyscreen.ButtonPress, max_width=10, name='[Edit]', relx=-63, rely=-5)
        self.edit_btn.whenPressed = self.editRow

        self.delete_btn = self.add(npyscreen.ButtonPress, max_width=10, name='[Delete]', relx=-53, rely=-5)
        self.delete_btn.whenPressed = self.deleteRow

        self.first_page_btn = self.add(npyscreen.ButtonPress, max_width=10, name='[First]', relx=-73, rely=-3)
        self.first_page_btn.whenPressed = self.firstPage

        self.prev_page_btn = self.add(npyscreen.ButtonPress, max_width=10, name='[Prev]', relx=-63, rely=-3)
        self.prev_page_btn.whenPressed = self.prevPage

        self.next_page_btn = self.add(npyscreen.ButtonPress, max_width=10, name='[Next]', relx=-53, rely=-3)
        self.next_page_btn.whenPressed = self.nextPage

        self.last_page_btn = self.add(npyscreen.ButtonPress, max_width=10, name='[Last]', relx=-43, rely=-3)
        self.last_page_btn.whenPressed = self.lastPage

        # define exit on Esc
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.on_cancel

    def addRow(self):
        self.parentApp.getForm('EDITROW').col_names = self.colnames
        self.parentApp.getForm('EDITROW').action = "add"
        self.parentApp.getForm('EDITROW').table_name = self.value
        self.parentApp.switchForm('EDITROW')

    def deleteRow(self):
        pass

    def editRow(self):
        pass

    def firstPage(self):
        pass

    def prevPage(self):
        pass

    def nextPage(self):
        pass

    def lastPage(self):
        pass

    def beforeEditing(self):
        self.parentApp.rows_per_page = 15
        self.SQL_display.value = None
        self.colnames, self.results = self.parentApp.db.browse_table(self.value)
        col_names = ' ' * 3
        for x in range(0, len(self.colnames)):
            col_names += " | " + self.colnames[x]

        self.col_display.value = col_names

        # pagination
        self.page = 0
        self.total_pages = int(ceil(len(self.results) / float(self.parentApp.rows_per_page)))
        self.displayResultsGrid(self.page)

    def displayResultsGrid(self, page):
        # column titles
        # any thing you want, does not matter
        self.SQL_display.column_titles = self.colnames

        # pagination
        start = self.page * self.parentApp.rows_per_page
        end = start + self.parentApp.rows_per_page
        # grid results displayed from 2d array
        self.SQL_display.values = []
        for result in self.results[start:end]:
            row = []
            for i in range(0, len(self.colnames)):
                row.append(result[i])
            self.SQL_display.values.append(row)

    def exit_menu(self):
        self.h_exit_escape(None)

    def on_cancel(self):
        self.parentApp.switchForm('TableSelect')
        self.parentApp.switchFormNow()

    def exit_application(self):
        self.parentApp.switchForm(None)
        self.parentApp.switchFormNow()


class EditRowForm(npyscreen.ActionForm):
    def create(self):
        self.value = None

    def beforeEditing(self):

        # For a long time this was self.columns.
        # npyscreen fails to mention that this is a reserved name...
        self.cols = []
        yPos = 2

        self.col_types = (self.parentApp.db.get_col_type(self.table_name))

        if self.action == 'edit':
            self.name = "Edit Row"
            for i, (a, b) in enumerate(zip(self.col_names, self.col_values)):
                # equivalent to self.cols[x] = self.add ...
                self.cols.append(
                    self.add(npyscreen.TitleText, name=str(a) + " (" + str(self.col_types[i]) + ")", value=str(b),
                             rely=yPos, begin_entry_at=30))
                yPos += 1
        else:
            self.name = "Add Row"
            for i, a in enumerate(self.col_names):
                self.cols.append(
                    self.add(npyscreen.TitleText, name=str(a) + " (" + str(self.col_types[i]) + ")", rely=yPos,
                             begin_entry_at=30))
                yPos += 1

    # Iffy solution to a problem here. Can't define the values of the widgets when the application starts,
    # because each table will have different fields. So they have to go in beforeEditing. This copies them
    # every time the form is called. Call the same form twice, you see each widget twice. Call any form
    # enough times and the screen runs out of space and throws a fatal error.

    # self.cols is just a list of return values, if you delete them, the widgets are still part of the form.
    # Per npyscreen documentation, you CANNOT delete widgets. The recommended solution was to make the widgets
    # hidden (invisible) and uneditable. This still makes them take up space on the form, so they are all "shoved"
    # into a tiny, overlapping, hidden box in the corner of the field, and the new widgets manually placed where the
    # old widgets used to be. This is an inelegant solution, but a limitation of the npyscreen library.

    def afterEditing(self):
        if self.cols:
            for item in self.cols:
                item.rely = 22
                item.relx = 40
                item.hidden = True
                item.editable = False

    def on_ok(self):
        self.new_values = []
        for item in self.cols:
            self.new_values.append(item.value)
        # if user is adding a row, omit the old values.
        else:
            self.parentApp.db.add_row(self.table_name, self.col_names, self.new_values)

        self.parentApp.switchForm('TableSelect')

    def on_cancel(self):
        self.parentApp.switchForm('TableSelect')


class MyApplication(npyscreen.NPSAppManaged):
    add_row_count = 0  # count number of calls to Add Row Form
    edit_row_count = 0  # count number of calls to Edit Row Form

    def onStart(self):
        self.db = Database(filename="my_water.db")
        self.myGridSet = GridSettings()
        self.welcomeTableF = self.addForm('MAIN', WelcomeSelectForm, name='Welcome Table')
        self.aboutUsTableF = self.addForm('AboutUs', AboutUsListDisplay, name='Group Members')
        self.selectTableF = self.addForm('TableSelect', TableListDisplay, name='Select Table')
        self.tabMenuF = self.addForm('Menu', TableMenuForm, name='Menu Table')
        self.addForm('EDITROW', EditRowForm, name="Edit Row")

    def exit_application(self):
        self.switchForm(None)
        self.switchFormNow()


if __name__ == '__main__':
    MyApplication().run()
    print('Exited From the App')
