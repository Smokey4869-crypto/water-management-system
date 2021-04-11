from math import *
import npyscreen
from test import Database


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


class TableMenuForm(npyscreen.ActionForm):
    # set screen redirection based on user choice
    CANCEL_BUTTON_TEXT = "Back"

    # Create Widgets
    def create(self):
        self.page = 0
        self.colnames = []
        self.results = []

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

        self.search_btn = self.add(npyscreen.ButtonPress, max_width=10, name='[Search]', relx=-43, rely=-5)
        self.search_btn.whenPressed = self.search

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

    def search(self):
        self.parentApp.getForm('SEARCHROW').table_name = self.value
        self.parentApp.switchForm('SEARCHROW')

    def addRow(self):
        self.parentApp.getForm('EDITROW').col_names = self.colnames
        self.parentApp.getForm('EDITROW').action = "add"
        self.parentApp.getForm('EDITROW').table_name = self.value
        self.parentApp.switchForm('EDITROW')

    def deleteRow(self):
        if self.SQL_display.value:
            self.yesOrNo = npyscreen.notify_yes_no(
                "You are about to delete a row. This action cannot be undone. Proceed?", editw=1)
            if self.yesOrNo:
                # fix bug where always select index of first page result
                self.SQL_display.value[0] += (self.page * self.parentApp.rows_per_page)
                # This passes the table name, column names, column values to the function that deletes the row.
                self.parentApp.db.delete_row(self.value, self.colnames, self.results[self.SQL_display.value[0]])
                self.parentApp.switchForm('TableSelect')
            else:
                npyscreen.notify_confirm("Aborted. Your row was NOT deleted.", editw=1)
        else:
            npyscreen.notify_confirm("Please select a row to delete.", editw=1)

    def editRow(self):
        if self.SQL_display.value:
            # fix bug where always select index of first page result
            self.SQL_display.value[0] += (self.page * self.parentApp.rows_per_page)
            npyscreen.notify_confirm(str(self.SQL_display.value))
            self.parentApp.getForm('EDITROW').col_names = self.colnames
            self.parentApp.getForm('EDITROW').col_values = self.results[self.SQL_display.value[0]]
            self.parentApp.getForm('EDITROW').action = "edit"
            self.parentApp.getForm('EDITROW').table_name = self.value
            self.parentApp.switchForm('EDITROW')
        else:
            npyscreen.notify_confirm("Please select a row to edit.", editw=1)

    def firstPage(self):
        self.page = 0
        self.displayResultsGrid(self.page)
        self.SQL_display.update(clear=False)
        self.display()

    def lastPage(self):
        self.page = self.total_pages - 1
        self.displayResultsGrid(self.page)
        self.SQL_display.update(clear=False)
        self.display()

    def nextPage(self):
        if self.page < self.total_pages - 1:
            self.page += 1
        self.displayResultsGrid(self.page)
        self.SQL_display.update(clear=False)
        self.display()

    def prevPage(self):
        if self.page > 0:
            self.page -= 1
        self.displayResultsGrid(self.page)
        self.SQL_display.update(clear=False)
        self.display()

    def beforeEditing(self):
        self.parentApp.rows_per_page = 5
        self.SQL_display.value = None
        self.colnames, self.results = self.parentApp.db.browse_table(self.value)
        print(self.results)
        col_names = ' ' * 3
        for x in range(0, len(self.colnames)):
            col_names += "   |   " + self.colnames[x]

        self.col_display.value = col_names

        # pagination
        self.page = 0
        self.total_pages = int(ceil(len(self.results) / float(self.parentApp.rows_per_page)))
        self.displayResultsGrid(self.page)

    def displayResultsGrid(self, page):
        # column titles
        # any thing you want, does not matter
        # self.SQL_display.column_titles = self.colnames

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
        print(self.SQL_display.values)

    def exit_menu(self):
        self.h_exit_escape(None)

    def on_cancel(self):
        self.parentApp.switchForm('TableSelect')
        self.parentApp.switchFormNow()

    def exit_application(self):
        self.parentApp.switchForm(None)
        self.parentApp.switchFormNow()


class SearchRowForm(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.query_result = None
        self.nextrely += 1
        self.chooser = self.add(npyscreen.SelectOne, max_height=2,
                                scroll_exit=True)
        self.chooser.values = ["Search by id", "Search by name"]
        self.nextrely += 1
        self.user_query = self.add(npyscreen.TitleText, name="Search Query:",
                                   begin_entry_at=15, use_two_lines=False,
                                   field_width=54)
        self.nextrely -= 1
        self.query_confirm = self.add(npyscreen.ButtonPress, name="OK", relx=70)
        self.query_confirm.whenPressed = self.process_query

        self.results = self.add(npyscreen.Pager, name="Results:", height=16,
                                max_height=14, scroll_exit=True,
                                slow_scroll=True, exit_left=True,
                                exit_right=True)

    def process_query(self):
        if self.chooser.value[0] == 0:

            self.query_result = self.parentApp.db.select_table_by_id(self.table_name, int(self.user_query.value))
        elif self.chooser.value[0] == 1:
            self.query_result = self.parentApp.db.select_table_by_name(self.table_name, self.user_query.value)

        if not self.query_result:
            npyscreen.notify_confirm(
                "No results were found for your query. "
                "Either Name or Licence Number does not exist in database.",
                editw=1, title='Error')
            return
        print(self.query_result)
        self.results.values = ['\n']
        self.results.values = self.query_result

    def on_ok(self):
        self.parentApp.switchForm("Menu")

    def on_cancel(self):
        self.parentApp.switchForm('Menu')


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

    def onStart(self):
        self.db = Database(filename="my_water.db")
        self.myGridSet = GridSettings()
        self.welcomeTableF = self.addForm('MAIN', WelcomeSelectForm, name='Welcome Table')
        self.aboutUsTableF = self.addForm('AboutUs', AboutUsListDisplay, name='Group Members')
        self.selectTableF = self.addForm('TableSelect', TableListDisplay, name='Select Table')
        self.tabMenuF = self.addForm('Menu', TableMenuForm, name='Menu Table')
        self.editRowF = self.addForm('EDITROW', EditRowForm, name="Edit Row")
        self.searchRowF = self.addForm('SEARCHROW', SearchRowForm, name='Search Row')

    def exit_application(self):
        self.switchForm(None)
        self.switchFormNow()


if __name__ == '__main__':
    MyApplication().run()
    print('Exited From the App')
