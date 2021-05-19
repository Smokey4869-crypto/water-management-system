import sqlite3
import datetime
from sqlite3 import Error


class Database:
    def __init__(self, filename):
        self.db = sqlite3.connect(filename)
        self.cursorObj = self.db.cursor()
        self.cursorObj.execute("PRAGMA foreign_keys = ON")

    def login(self, username, password):
        try:
            self.cursorObj.execute(f"SELECT * FROM adminlogin WHERE username= '{username}' and password='{password}'")
            results = self.cursorObj.fetchone()
            self.db.commit()
            return results
        except Error as e:
            return e

    def search(self, table, search_by, search_txt):
        try:
            self.cursorObj.execute(f"SELECT * FROM {table} WHERE {search_by} LIKE '%{search_txt}%'")
            self.db.commit()
            return list(self.cursorObj.fetchall())
        except Error as e:
            return e

    def search_exact(self, table, search_by, search_txt):
        try:
            self.cursorObj.execute(f"SELECT * FROM {table} WHERE {search_by} LIKE '{search_txt}'")
            self.db.commit()
            return list(self.cursorObj.fetchall())
        except Error as e:
            return e

    def insert_txt(self):
        try:
            self.values = 800
            self.data = [(11, self.values, datetime.date(2017, 1, 2), datetime.date(2017, 3, 2), self.values * 20)]
            self.cursorObj.executemany("INSERT INTO billing VALUES(?,?,?,?,?)", self.data)
            self.db.commit()
        except Error as e:
            return e

    def browse_table(self, table):
        try:
            self.cursorObj.execute("SELECT * FROM %s ORDER BY 1 ASC;" % table)
            colnames = [desc[0] for desc in self.cursorObj.description]
            results = self.cursorObj.fetchall()
            rows = []
            for result in results:
                rows.append(list(result))
            return colnames, rows
        except Error as e:
            return e

    def insert_gui(self, table, data):
        # data in the form of tuple
        try:
            self.cursorObj.execute(f"INSERT INTO {table} VALUES {data}")
            self.db.commit()
            return self.cursorObj.execute(f"SELECT * FROM {table}")
        except Error as e:
            return e

    def delete_row(self, table, conditions):
        # delete_row('household', [{'household_id': [1, 2]}]
        try:
            for condition in conditions:
                for key, value in condition.items:
                    command = f"DELETE FROM {table} WHERE {key} LIKE '{value}'"
                    self.cursorObj.execute(command)
                    self.db.commit()
        except Error as e:
            return e

    def get_col_type(self, table):
        try:
            query = "pragma table_info({})".format(table)
            results = self.cursorObj.execute(query).fetchall()
            rows = []
            for result in results:
                rows.append(result[2])
            return rows
        except Error as e:
            return e

    def get_col(self, table):
        try:
            self.cursorObj.execute('SELECT * FROM {}'.format(table))
            names = list(map(lambda x: x[0], self.cursorObj.description))
            return names
        except Error as e:
            return e

    def get_all_col_record_in_table(self, table, col):
        try:
            self.cursorObj.execute(f'SELECT * from {table}')
            records = self.cursorObj.fetchall()
            results = []
            for record in records:
                results.append(record[col])
            return results
        except Error as e:
            return e

    def update_value(self, table, changes, condition):
        # change and condition in the form of a list
        # ex : change: [ {emp_id: 1}, {hel: 2}], condition: [area_id, 21]
        try:
            for change in changes:
                for key, value in change.items():
                    self.cursorObj.execute(f'UPDATE {table} SET {key} = {value} where {condition[0]} = {condition[1]}')
                    self.db.commit()
        except Error as e:
            return e

    def join_two_tables(self, table1, table2, attributes):
        try:
            sql = f'''SELECT * from {table1} JOIN {table2} ON '''
            print(len(attributes))
            if len(attributes) > 1:
                for i in range(len(attributes) - 1):
                    sql += f'''{table1}.{attributes[i]} = {table2}.{attributes[i]} AND '''

            sql += f'''{table1}.{attributes[len(attributes) - 1]} = {table2}.{attributes[len(attributes) - 1]}'''
            self.cursorObj.execute(sql)
            self.cursorObj.fetchall()
        except Error as e:
            return e

    def list_tables(self):
        try:
            sql_outputs = self.cursorObj.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            result = []
            for output in sql_outputs:
                for elem in output:
                    result.append(elem)
            return result
        except Error as e:
            return e

    def get_water_company_name(self, customer_id):
        self.cursorObj.execute("SELECT supplier_name from supplier,"
                               "household,billing WHERE household.household_id=billing.household_id "
                               "and billing.household_id='{}'".format(customer_id))

        result = self.cursorObj.fetchone()
        self.db.commit()
        return result

    # print bill

    def get_information_bill(self, household_id):
        try:
            self.cursorObj.execute(
                "SELECT * from billing WHERE household_id = '{}'".format(household_id))
            rows = self.cursorObj.fetchone()
            water_company_name = self.get_water_company_name(household_id)[0]
            customer_info = self.select_specific_customer(household_id)
            print(customer_info)
            customer_name = customer_info[1]
            no = rows[0]
            cust_id = rows[1]
            total_amount = rows[5]
            from_date = rows[3]
            to_date = rows[4]
            water_amount = rows[2]
            bill_name = 'bill_' + str(no) + '.txt'
            m = ""
            m += "============================================================\n"
            m += "\n"
            m += "                Water Bill" + "    " + "Bill number: %d\n\n" % no
            m += "              Customer Id: %d\n\n" % cust_id
            m += "------------------------------------------------------------\n"
            m += water_company_name + "\n"
            m += "Customer name:" + "      " + customer_name + "\n"
            m += "Customer address:" + "   " + customer_info[3] + "\n"
            m += "Customer phone:" + "     " + customer_info[4] + "\n"
            m += "Time use water:" + "   " + from_date + " " + "to" + " " + to_date + "\n"
            m += "Amount of water used:" + "   " + str(water_amount) + "m3" + "\n"
            m += "Total money:" + "   " + str(total_amount) + "VND" + "\n"
            m += "\n"
            m += "                                       " + str(datetime.date.today()) + "\n"
            m += "                                       " + "Signature" + "\n"
            m += "                                     " + water_company_name + "\n"
            m += "============================================================\n"
            bill = open(bill_name, 'w')
            bill.write(m)
            bill.close()
        except Error as e:
            return e

    def value_consumed_by_household(self, type="water_consumption", year="", month=""):
        try:
            result = []
            command = f"""SELECT household_id, SUM({type}) FROM billing """

            condition = ""
            if year:
                condition = f" WHERE to_date LIKE \'%{year}"

                if month:
                    condition += f"-{month}%\'"
                else:
                    condition += f"%\'"

            command += condition + " GROUP BY household_id"

            for row in self.cursorObj.execute(command):
                result.append(row)

            return result
        except Error as e:
            return e

    def num_of_value(self, table, conditions):
        # num_of-value(area, [{'supplier_id': [1, 2]}])
        try:
            result = []
            for condition in conditions:
                for key, values in condition.items():
                    for value in values:
                        command = f"SELECT SUM(CASE WHEN {key} = \'{value}\' THEN 1 ELSE 0 END) FROM {table}"
                        for row in self.cursorObj.execute(command):
                            result.append(row[0])
            return result
        except Error as e:
            return e

    def values_consumed_by_suppliers_or_areas(self, ids, type="water_consumption", year="", month=""):
        # db.value_consumed_by_suppliers_or_areas([{'supplier_id': [1, 2]}], "total_money")
        try:
            result = []
            for id in ids:
                for key, values in id.items():
                    for value in values:
                        command = f"""SELECT area.{key}, sum({type})
                                    FROM billing 
                                    INNER JOIN household 
                                    ON household.household_id = billing.household_id 
                                    INNER JOIN address
                                    ON address.address_id = household.address_id
                                    INNER JOIN area
                                    ON area.area_id = address.area_id 
                                    """
                        condition = f"WHERE area.{key} = '{value}'"

                        if year:
                            condition += f" AND to_date LIKE \'%{year}"

                            if month:
                                condition += f"-{month}%\'"
                            else:
                                condition += "%\'"

                        command += condition + f" GROUP BY area.{key}"

                        for item in self.cursorObj.execute(command):
                            result.append(item)
            return result
        except Error as e:
            return e

    def table_total_value(self, table):
        try:
            self.cursorObj.execute(f"SELECT COUNT(*) FROM {table}")
            result = self.cursorObj.fetchone()
            return result[0]
        except Error as e:
            return e

    def column_unique(self, table, column):
        try:
            result = []
            command = f"""SELECT DISTINCT({column}) FROM {table}"""
            for value in self.cursorObj.execute(command):
                result.append(value[0])
            return result
        except Error as e:
            return e


def main():
    db = Database(filename='water_database.db')
    # db.get_information_bill(1)
    # db.total_amount_of_water_by_area()
    # err = db.search("household", "hello", "10")
    # print(err)
    # db.update_value('supplier', ['supplier_name', 'CompFive'], ['supplier_id', '5'])
    # db.delete_row('supplier', 'supplier_id', [13, 12])
    # print(db.get_col_type('billing'))
    # print(db.value_consumed_by_suppliers_or_areas([{'area_id': [1, 2, 3]}], "water_consumption"))
    # print(db.value_consumed_by_household(year='2021', month='1'))
    # print(db.value_consumed_by_household(year='2020'))
    # print(db.value_consumed_by_household())
    # print(db.water_consumed_by_area([1, 2, 3, 4]))
    # print(db.value_consumed_by_suppliers_or_areas([{"supplier_id": [1, 2]}]))
    # print(db.browse_table('household'))

    # print(db.num_emp_gender('F'))
    # print(db.num_emp_role('director'))
    # print(db.num_households_in_area([1, 2, 3, 15]))
    # print(db.num_area_of_suppliers([1, 2, 3]))
    # print(db.num_of_value('area', [{'supplier_id': [1, 2]}]))
    db.column_unique("employee", "sex")



if __name__ == '__main__':
    main()
