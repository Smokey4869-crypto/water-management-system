import sys
import datetime
import curses
from curses import wrapper
import sqlite3
import datetime


class Database:
    def __init__(self, filename):
        self.db = sqlite3.connect(filename)
        self.cursorObj = self.db.cursor()

    def insert(self):
        self.values = 800
        self.data = [(11, self.values, datetime.date(2017, 1, 2), datetime.date(2017, 3, 2), self.values * 20)]
        self.cursorObj.executemany("INSERT INTO billing VALUES(?,?,?,?,?)", self.data)
        self.db.commit()

    def select_employee(self):
        self.cursorObj.execute("SELECT * FROM employee")
        rows = self.cursorObj.fetchall()
        return rows

    def delete_employee(self, id):
        self.sql = '''DELETE FROM employee WHERE '''
        self.cursorObj.execute(self.sql, (id))
        self.db.commit()

    def insert_area(self):
        areaid = int(input("Enter area id"))
        areaname = input("enter area name")
        empid = int(input("Enter emp id"))
        self.data = [(areaid, areaname, empid)]
        self.cursorObj.executemany("INSERT INTO area VALUES(?,?,?)", self.data)
        self.db.commit()

    def update_area(self, id):
        self.sql_update_query = 'UPDATE area SET empid = ? where areaid = ?'
        self.data = (12, id)
        self.cursorObj.execute(self.sql_update_query, self.data)
        self.db.commit()

    def join_billing_and_customer(self):
        self.sql = '''SELECT * from customers INNER JOIN billing ON billing.custid = customers.custid WHERE billing.custid=1'''
        self.cursorObj.execute(self.sql)
        self.result = self.cursorObj.fetchall()
        print(self.result)

    def join_area_and_employee(self):
        self.sql = '''SELECT name,phone,sex,designation,salary,areaname from employee JOIN area ON employee.empid = area.empid'''
        self.cursorObj.execute(self.sql)
        self.result = self.cursorObj.fetchall()
        print(self.result)

    def join_services_and_customer(self):
        self.sql = '''SELECT name,areaname,servicetype,servicerequest from 
        customers,area,service WHERE customers.custid = service.custid AND customers.areaid=area.areaid'''
        self.cursorObj.execute(self.sql)
        self.result = self.cursorObj.fetchall()
        print(self.result)

    def join_feedback_and_customer(self):
        self.sql = '''SELECT name,feedbackdescription from 
                feedback,customers WHERE customers.custid = feedback.custid'''
        self.cursorObj.execute(self.sql)
        self.result = self.cursorObj.fetchall()
        print(self.result)

    def join_supplier_and_area(self):
        self.sql = '''SELECT suppliername,phone,areaname from 
                        supplier,area WHERE supplier.areaid = area.areaid'''
        self.cursorObj.execute(self.sql)
        self.result = self.cursorObj.fetchall()
        print(self.result)


class Engine(object):
    def __init__(self):
        self.stdscr = None
        self.n = 0
        self.db = None

    def init_view(self):
        self.db = Database(filename="my_water.db")
        self.stdscr = curses.initscr()
        self.stdscr.clear()
        curses.curs_set(False)
        while self.n != ord('3'):
            self.stdscr.clear()
            self.stdscr.addstr(2, 0, 'Enter a Number:')
            self.stdscr.addstr(3, 2, '1 - View Employee')
            self.stdscr.addstr(4, 2, '2 - Cancel Appointment')
            self.stdscr.addstr(5, 2, '3 - Exit')
            self.stdscr.refresh()
            self.n = self.stdscr.getch()

            if self.n == ord('1'):
                self.stdscr.clear()
                self.stdscr.addstr(2, 5, 'NAME')
                self.stdscr.addstr(2, 25, 'PHONE')
                self.stdscr.addstr(2, 38, 'SEX')
                self.stdscr.addstr(2, 45, 'DESIGNATION')
                self.stdscr.addstr(2, 75, 'salary')
                results = self.db.select_employee()
                print(results)
                row = 3
                for result in results:
                    employeeName = str(result[1])
                    employeePhone = str(result[2])
                    employeeGender = str(result[3])
                    employeeDesignation = str(result[4])
                    employeeSalary = str(result[5])
                    self.stdscr.addstr(row, 5, employeeName)
                    self.stdscr.addstr(row, 22, employeePhone)
                    self.stdscr.addstr(row, 38, employeeGender)
                    self.stdscr.addstr(row, 45, employeeDesignation)
                    self.stdscr.addstr(row, 75, employeeSalary)
                    row += 1
                self.stdscr.refresh()
                self.stdscr.getkey()

    def initWrapper(self):
        # curses wrapper initiates and exits window/curses
        wrapper(self.init_view())


if __name__ == "__main__":
    view = Engine()
    view.initWrapper()
