import sqlite3
import datetime
import npyscreen


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
        query_string = "INSERT INTO %s (" % table_name
        query_string = query_string[:-1] + " VALUES ("
        for x in range(0, len(columns)):
            query_string += "%s" + ","
        query_string = query_string[:-1] + ");"
        data = []
        for x in range(0, len(columns)):
            data.append(str(new_values[x]))
        self.cursorObj.execute(query_string, data)
        self.db.commit()

    def delete_row(self, table_name, columns, values):
        query_string = '('
        for x in range(0, len(columns)):
            query_string += (columns[x] + " = '" + str(values[x]) + "' AND ")
        query_string = "DELETE FROM %s WHERE " % table_name + query_string[:-5] + ');'  # debug
        self.cursorObj.execute(query_string)
        self.db.commit()
        npyscreen.notify_confirm("Row deleted.")

    def edit_row(self, table_name, columns, new_values, old_values):

        # This part is just building the query string
        query_string = "UPDATE %s SET " % table_name
        for x in range(0, len(columns)):
            query_string += (columns[x] + " = %s, ")
        query_string = query_string[:-2] + ' WHERE ('
        for x in range(0, len(columns)):
            query_string += (columns[x] + " = %s AND ")
        query_string = query_string[:-5] + ');'

        # pass parameters as separate list. psycopg2 automatically converts Python objects to
        # SQL literals, prevents injection attacks
        data = []
        for x in range(0, len(columns)):
            data.append(str(new_values[x]))
        for x in range(0, len(columns)):
            data.append(str(old_values[x]))
        print(query_string)
        npyscreen.notify_confirm(query_string)  # debug
        npyscreen.notify_confirm(data)  # debug
        self.cursorObj.execute(query_string, data)
        self.db.commit()
        npyscreen.notify_confirm("Row updated.")

    def select_table_by_id(self, table_name, id):
        self.cursorObj.execute("SELECT * FROM %s WHERE id=%d;" % (table_name, id))
        results = self.cursorObj.fetchall()
        return list(results)

    def select_table_by_name(self, table_name, name):
        self.cursorObj.execute("SELECT * FROM '{}' WHERE name='{}';".format(table_name, name))
        results = self.cursorObj.fetchall()
        return list(results)


def main():
    db = Database(filename='my_water.db', )
    db.select_table_by_name(table_name="stupidtest", name="tran hong quan")


if __name__ == '__main__':
    main()
