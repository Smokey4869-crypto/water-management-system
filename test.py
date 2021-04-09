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

    def select_area(self):
        self.cursorObj.execute("SELECT * FROM area")
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

    def update_area(self,id):
        self.sql_update_query='UPDATE area SET empid = ? where areaid = ?'
        self.data = (12, id)
        self.cursorObj.execute(self.sql_update_query,self.data)
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

def main():
    db = Database(filename='my_water.db', )
    db.update_area(10)


if __name__ == '__main__':
    main()
