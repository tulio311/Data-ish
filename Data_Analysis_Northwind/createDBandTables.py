import psycopg2
from typing import List

# primaryKey gets the name of the column which has the primary key.
# Autoincrement gets a string of boolean indicators for each column
# in the table. foreignKeys has a list of strings or None values
def createTable(name : str,fields : List[str],
                types : List[str], primaryKey : str,
                autoIncrements: List[bool], foreignKeys: List[bool] = [],
                parentTable : str = '') -> None:
    
    queryFragment = ""
    for i in range(len(fields)):
        prim = 'PRIMARY KEY' if fields[i] == primaryKey else ''
        typeOrautoInc = 'SERIAL' if autoIncrements[i] == True else types[i]

        queryFragment += f"{fields[i]} {typeOrautoInc} {prim},"

    queryFragment = queryFragment[:-1]

    foreigns = ''
    ind = False
    for fk in foreignKeys:
        ind = True if fk != None else False

    if ind:
        queryFragmentfk = '('
        #queryFragmentfk2 = f'REFERENCES {parentTable}('
        for i in range(len(foreignKeys)):
            fkCol = f"{fields[i]}, " if foreignKeys[i] == True else ''
            queryFragmentfk += fkCol

        queryFragmentfk = queryFragmentfk[:-2] + ")"
        foreigns = f""",
                        CONSTRAINT fk_{name}
                       FOREIGN KEY {queryFragmentfk}
                        REFERENCES {parentTable} {queryFragmentfk}
                        ON UPDATE CASCADE
                        ON DELETE RESTRICT
                    """


    query = f"""
            CREATE TABLE {name} (
        """ + queryFragment + foreigns + ");"

    print(query)
    
    try:
        cur.execute(query)
        print(f"Table {name} created")
    except Exception as e:
        print(e)
        #print(f"Table {name} already exists")

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


conn = psycopg2.connect(
        host="localhost",
        database="northwind",
        user="postgres",
        password="153608"
)

conn.autocommit = True

cur = conn.cursor()




createTable(name = 'Categories', fields =  ['CategoryID','CategoryName','Description'],
                                types =['INTEGER', 'TEXT', 'TEXT'], primaryKey='CategoryID',
                                autoIncrements=[True,False,False])

createTable(name = 'Costumers', fields =  ['CostumerID','CostumerName','ContactName','Adress','City','PostalCode','Country'],
                                types =['INTEGER', 'TEXT', 'TEXT','TEXT', 'TEXT','TEXT', 'TEXT'], primaryKey='CostumerID',
                                autoIncrements=[True,False,False,False,False,False,False])

createTable(name = 'Employees', fields =  ['EmployeeID','LastName','FirstName','BirthDate','Photo','Notes'],
                                types =['INTEGER', 'TEXT', 'TEXT','DATE', 'TEXT','TEXT'], primaryKey='EmployeeID',
                                autoIncrements=[True,False,False,False,False,False])

createTable(name = 'OrderDetails', fields =  ['OrderDetailID','OrderID','ProductID','Quantity'],
                                types =['INTEGER', 'INTEGER', 'INTEGER','INTEGER'], primaryKey='OrderDetailID',
                                autoIncrements=[True,False,False,False], foreignKeys=[False,True,True,False],
                                parentTable='Products')


cur.close()
conn.close()




