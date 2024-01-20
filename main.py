import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="LAF"
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE TABLE LOST (Lostid INT PRIMARY KEY, DeviceName INT, MainTag VARCHAR(255), Date DATE, Location VARCHAR(255))")
# mycursor.execute("CREATE TABLE FOUND (Foundid INT PRIMARY KEY, Photo BLOB, Location VARCHAR(255), Maintag VARCHAR(255))")

mycursor.execute("show tables")

for x in mycursor:
    print(x)

# insert_query = "INSERT INTO LOST (Lostid, DeviceName, MainTag, Date, Location) VALUES (%s, %s, %s, %s, %s)"
# data_to_insert = (4, 12348, 'laptop,hp,spectre', '2024-04-23', 'bakul')
# mycursor.execute(insert_query, data_to_insert)
# mydb.commit()



# mycursor.execute('select * from LOST')
# for x in mycursor:
#     print(x)

mycursor.execute('select * from LOST where Maintag = "laptop"')
for x in mycursor:
    print(x)

mycursor.execute('select MainTag,Lostid from LOST')
for x in mycursor:
    print(x)