import mysql.connector
import time
import record_SQL_data
import csv

mydb=mysql.connector.connect(
  host="localhost",
  user="dmueller",
  passwd="mypwd",
  database="beerCode"
)
mycursor=mydb.cursor()

# Query the existing databases.
query=record_SQL_data.query_all_in_table(mydb,mycursor,"beerCode","brewList")
print(query)
query=record_SQL_data.query_all_in_table(mydb,mycursor,"beerCode","brewTemperatureHistory")
print(query)

# Read data from csv file.
fileName='./logs/temp_log_08_13_13_05_2019.csv'
brewID=2
with open(fileName) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
          print('Column names are '+", ".join(row))
          line_count += 1
        print(row["time"]+', '+row["temperature_air"]+', '+row["temperature_liquid"]+', '+row["op_hot"]+', '+row["op_cold"])
        line_count += 1
        record_SQL_data.add_to_temp_log(mydb,mycursor,brewID,row["time"],row["temperature_air"],row["temperature_liquid"],row["op_hot"],row["op_cold"])
    print('Processed '+str(line_count)+' lines.')

# Write functions
#record_SQL_data.add_to_brew_list(mydb,mycursor,"SighPA 1")
#record_SQL_data.add_to_temp_log(mydb,mycursor,1,time,10.5,11.3,0,1)

# Remove records
#record_SQL_data.remove_from_brew_list(mydb,mycursor,(2,3,4,5,6,7,8,9,10))
#record_SQL_data.remove_from_temp_log(mydb,mycursor,(2,3,4,5,6,7))

mydb.close()
