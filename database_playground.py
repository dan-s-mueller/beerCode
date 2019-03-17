import mysql.connector
import time
import record_SQL_data
import csv

mydb=mysql.connector.connect(
  host="localhost",
  user="dmueller",
  passwd="Spartan1",
  database="beerCode"
)
mycursor=mydb.cursor()

# Query the existing databases.
query=record_SQL_data.query_all_in_table(mydb,mycursor,"beerCode","brewList")
print(query)
query=record_SQL_data.query_all_in_table(mydb,mycursor,"beerCode","brewTemperatureHistory")
print(query)

# Read data from csv file.
fileName='temp_log_22_50_10_03_2019.csv'
brewID=1
with open(fileName) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
          print('Column names are '+", ".join(row))
          line_count += 1
        print(row["time"]+', '+row["temperature_air"]+', '+row["temperature_liquid"])
        line_count += 1
        record_SQL_data.add_to_temp_log(mydb,mycursor,brewID,row["time"],row["temperature_air"],row["temperature_liquid"])
    print('Processed '+str(line_count)+' lines.')

# Write functions
# time=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#record_SQL_data.add_to_brew_list(mydb,mycursor,"We never made this!")
#record_SQL_data.add_to_temp_log(mydb,mycursor,1,time,10.5,11.3)

# Remove records
#record_SQL_data.remove_from_brew_list(mydb,mycursor,(2,3,4,5,6,7,8,9,10))
#record_SQL_data.remove_from_temp_log(mydb,mycursor,(2,3,4,5))

mydb.close()
