import mysql.connector
import time
import record_SQL_data

mydb=mysql.connector.connect(
  host="localhost",
  user="dmueller",
  passwd="mypwd",
  database="beerCode"
)
mycursor=mydb.cursor()

record_SQL_data.add_to_brew_list(mydb,mycursor,"Second Crack Coffee Porter 1")

mydb.close()
