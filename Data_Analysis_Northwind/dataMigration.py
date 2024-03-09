import psycopg2
from typing import List
import pandas as pd
import sqlite3



def insertData(tableName : str, columns: List[str], cur, data) -> None:

    cols = len(columns)

    colRow = "(" + ",".join(columns) + ")"

    print(colRow)

    for row in data:
        dataRow = "('" + "','".join([str(i).replace("'","''") for i in row]) + "')"
        query = f"INSERT INTO {tableName} {colRow} VALUES {dataRow};"

        
        print(query)
        cur.execute(query)
        #for i in range(cols):


def migrate(tableName : str, curOrigin, curDestiny) -> None:

    curOrigin.execute(f"SELECT * FROM {tableName};")
    data = curOrigin.fetchall()
    columns = [curOrigin.description[i][0] for i in range(len(data[0]))]
    print(columns)

    insertData(tableName, columns, curDestiny, data)
    



f = open('pass.txt','r')
pwd = f.read()
f.close()

connPg = psycopg2.connect(
        host="localhost",
        database="northwind",
        user="postgres",
        password=pwd
)

connPg.autocommit = True

curPg = connPg.cursor()


conSqL = sqlite3.connect("Northwind.db",isolation_level=None)
curSqL = conSqL.cursor()



migrate("Categories", curSqL, curPg)
migrate("Customers", curSqL, curPg)
migrate("Employees", curSqL, curPg)
migrate("Shippers", curSqL, curPg)
migrate("Orders", curSqL, curPg)
migrate("Suppliers", curSqL, curPg)
migrate("Products", curSqL, curPg)
migrate("OrderDetails", curSqL, curPg)






curPg.close()
connPg.close()
