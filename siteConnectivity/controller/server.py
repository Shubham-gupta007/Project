import mysql.connector
def  mysqlConnection(database):
    db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Admin@1234",
    database = database
    )
    print(db_connection)
    return(db_connection)


def createTable():
    conn = mysqlConnection()
    print("conn",conn)
    myscursor = conn.cursor()
    myscursor.execute("Create table sites_collection(id int NOT NULL AUTO_INCREMENT, dns_name varchar(128), status varchar(20), state varchar(20), created_date DATE, updated_date DATE, error_code int, error_message varchar(200), ipaddress varchar(200), PRIMARY KEY(id))")

def showTable():
    conn = mysqlConnection()
    mycursor = conn.cursor()
    mycursor.execute("Show tables")
    for tb in  mycursor:
        print(tb)

def editTable():
    conn = mysqlConnection()
    mycursor = conn.cursor()
    sqlForm = "Insert into employee(name,sal) value(%s,%s)"
    employess = [("shubham",10000),("amit",30000),("Ankit",20000)]
    mycursor.executemany(sqlForm,employess)
    conn.commit()

def readSingleTable():
    conn = mysqlConnection()
    mycursor = conn.cursor()
    mycursor.execute("Select * from employee")
    myresult = mycursor.fetchone()
    for row in myresult:
        print(row)

def readTable():
    conn = mysqlConnection()
    mycursor = conn.cursor()
    mycursor.execute("Select * from employee")
    myresult = mycursor.fetchall()
    for row in myresult:
        print(row)


def updatTable():
    conn = mysqlConnection()
    mycursor = conn.cursor()
    sqlUpdate = "UPDATE employee SET sal = 70000 WHERE name ='shubham'"
    mycursor.execute(sqlUpdate)
    conn.commit()


def deleteTable():
    conn = mysqlConnection()
    mycursor = conn.cursor()
    sqlQuery = "Delete FROM employee WHERE name= 'amit'"
    mycursor.execute(sqlQuery)
    conn.commit()
# createTable()
# showTable()
# editTable()
# readSingleTable()

# updatTable()
# readTable()
# deleteTable()
