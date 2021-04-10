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

    def browse_table(self, table_name):
        self.cursorObj.execute("SELECT * FROM %s ORDER BY 1 ASC;" % table_name)
        colnames = [desc[0] for desc in self.cursorObj.description]
        results = self.cursorObj.fetchall()
        rows = []
        for result in results:
            rows.append(list(result))
        return colnames, rows

    def get_col_type(self, table_name):
        query = "pragma table_info({})".format(table_name)
        results = self.cursorObj.execute(query).fetchall()
        rows = []
        for result in results:
            rows.append(result[2])
        print(rows)
        return rows

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

    def list_tables(self):
        self.result = self.cursorObj.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        return self.result[1:len(self.result)]

    def add_row(self, table_name, columns, new_values):
        query_string = "INSERT INTO %s " % table_name
        query_string = query_string[:-1] + " VALUES ("
        for x in range(0, len(columns)):
            query_string += "?" + ","
        query_string = query_string[:-1] + ");"
        print(query_string)
        data = []
        for x in range(0, len(columns)):
            data.append(str(new_values[x]))
        self.cursorObj.execute(query_string, data)
        self.db.commit()
        print(data)


def main():
    db = Database(filename='my_water.db', )
    print(db.list_tables())


if __name__ == '__main__':
    main()
