import psycopg2
from typing import List

# This is a function for creating a table in a PostgreSQL database

# fields gets a list with the table fields

# primaryKey gets the name of the column which has the primary key.

# Autoincrement gets a list of boolean indicators for each column in the table. 

# default gets a list with the default values or None if there is no default value.

# foreignKeys gets a list of bools indicating if each field is a foreign key

# parentTables gets a list of the parent tables for the foreign keys in the same order

def createTable(name : str,fields : List[str],
                types : List[str], primaryKey : str,
                autoIncrements: List[bool],defaults : List = [],
                foreignKeys: List[bool] = [], parentTables : List[str] = []) -> None:
    
    # Primary key and autoincrement management
    columns = ""
    isDef = 1 if len(defaults) > 0 else 0
    default = ''

    for i in range(len(fields)):

        prim = 'PRIMARY KEY' if fields[i] == primaryKey else ''
        typeOrautoInc = 'SERIAL' if autoIncrements[i] == True else types[i]

        if isDef == 1:
            default = f'DEFAULT {defaults[i]}' if defaults[i] != None else ''

        columns += f"{fields[i]} {typeOrautoInc} {prim} {default},\n"

    columns = columns[:-2]

    # Foreign keys management
    foreigns = ''
    ind = False

    # Checking if there is at least 1 foreign key
    for fk in foreignKeys:
        ind = True if fk != None else False

    if ind:
        foreigns = ',\n'
        for i in range(len(foreignKeys)):

            if foreignKeys[i] == True:

                foreigns += f"""FOREIGN KEY ({fields[i]}) REFERENCES {parentTables[i]}({fields[i]})
                                ON UPDATE CASCADE
                                ON DELETE RESTRICT,"""

        foreigns = foreigns[:-1]
      

    # Full query
    query = f"""
            CREATE TABLE {name} (
        """ + columns + foreigns + ");"
    
    print(query)
    
    try:
        cur.execute(query)
        print(f"Table {name} created")
    except Exception as e:
        print(e)


conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="153608"
)

conn.autocommit = True

cur = conn.cursor()

# Creating database if it doesn't exist
try:
    cur.execute("CREATE DATABASE Northwind;")
except:
    print("Database already exists")

cur.close()
conn.close()

f = open('pass.txt','r')
pwd = f.read()
f.close()

conn = psycopg2.connect(
        host="localhost",
        database="northwind",
        user="postgres",
        password=pwd
)

conn.autocommit = True

cur = conn.cursor()




createTable(name = 'Categories', fields = ['CategoryID','CategoryName','Description'],
                                types =['INTEGER', 'TEXT', 'TEXT'], primaryKey='CategoryID',
                                autoIncrements=[True,False,False])

createTable(name = 'Costumers', fields = ['CostumerID','CostumerName','ContactName','Adress','City','PostalCode','Country'],
                                types =['INTEGER', 'TEXT', 'TEXT','TEXT', 'TEXT','TEXT', 'TEXT'], primaryKey='CostumerID',
                                autoIncrements=[True,False,False,False,False,False,False])

createTable(name = 'Employees', fields =  ['EmployeeID','LastName','FirstName','BirthDate','Photo','Notes'],
                                types =['INTEGER', 'TEXT', 'TEXT','DATE', 'TEXT','TEXT'], primaryKey='EmployeeID',
                                autoIncrements=[True,False,False,False,False,False])

createTable(name = 'Shippers', fields =['ShipperID','ShipperName','Phone'],
                                types =['INTEGER', 'TEXT','TEXT'], primaryKey='ShipperID',
                                autoIncrements=[True,False,False])

createTable(name = 'Orders', fields =['OrderID','CostumerID','EmployeeID','OrderDate','ShipperID'],
                                types =['INTEGER', 'INTEGER', 'INTEGER','DATE','INTEGER'], primaryKey='OrderID',
                                autoIncrements=[True,False,False,False,False], foreignKeys=[False,True,True,False,True],
                                parentTables=[None, 'Costumers', 'Employees', None, 'Shippers'])

createTable(name = 'Products', fields =['ProductID','ProductName','SupplierID','CategoryID','Unit','Price'],defaults = [None,None,None,None,None,0],
                                types =['INTEGER', 'TEXT','INTEGER','INTEGER','TEXT','NUMERIC'], primaryKey='ProductID',
                                autoIncrements=[True,False,False,False,False,False], foreignKeys=[False,False,True,True,False,False],
                                parentTables=[None,None, 'Suppliers', 'Categories', None,None])

createTable(name = 'OrderDetails', fields =['OrderDetailID','OrderID','ProductID','Quantity'],
                                types =['INTEGER', 'INTEGER', 'INTEGER','INTEGER'], primaryKey='OrderDetailID',
                                autoIncrements=[True,False,False,False], foreignKeys=[False,True,True,False],
                                parentTables=[None, 'Orders', 'Products', None])

createTable(name = 'Suppliers', fields =['SupplierID','SupplierName','ContactName','Address','City','PostalCode','Country','Phone'],
                                types =['INTEGER', 'TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT'], primaryKey='SupplierID',
                                autoIncrements=[True,False,False,False,False,False,False,False])



cur.close()
conn.close()




