import mysql.connector
import time
import record_SQL_data

mydb=mysql.connector.connect(
  host="localhost",
  user="dmueller",
  passwd="Spartan1",
  database="beerCode"
)
mycursor=mydb.cursor()

query=record_SQL_data.query_all_in_table(mydb,mycursor,"beerCode","brewList")
print(query)
query=record_SQL_data.query_all_in_table(mydb,mycursor,"beerCode","brewTemperatureHistory")
print(query)

#record_SQL_data.add_to_brew_list(mydb,mycursor,"We never made this!")
#record_SQL_data.add_to_temp_log(mydb,mycursor,1,10.5,11.3)

query=record_SQL_data.query_all_in_table(mydb,mycursor,"beerCode","brewList")
print(query)
query=record_SQL_data.query_all_in_table(mydb,mycursor,"beerCode","brewTemperatureHistory")
print(query)

#record_SQL_data.remove_from_brew_list(mydb,mycursor,(2,3,4,5,6,7,8,9,10))
#record_SQL_data.remove_from_temp_log(mydb,mycursor,(2,3,4,5))

mydb.close()
