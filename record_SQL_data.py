import mysql.connector
import time
import datetime

def query_all_in_table(mydb,mycursor,database,tableName):
	"""
	Queries tableName and returns the value of the entire query.
	database = name of database
	tableName = name of table in database.table
	"""
	sql = "SELECT * FROM "+database+"."+tableName
	
	try:
		mycursor.execute(sql)
		query=mycursor.fetchall()
		return query
	except:
		mydb.rollback()
		print("Issue occurred when trying to query table.")
		return -1

def add_to_brew_list(mydb,mycursor,brewName):
	"""
	Adds a record to beerCode.brewList.
	brewName = String describing the name of the beer.
	"""
	ts = time.time()
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	
	sql = "INSERT INTO beerCode.brewList (brewName, brewDate) VALUES (%s, %s)"
	val = (brewName, timestamp)

	try:
		mycursor.execute(sql, val)
		mydb.commit()
		print(mycursor.rowcount, "Record inserted.")
	except:
		mydb.rollback()
		print("Issue occurred when trying to write record.")
		
def remove_from_brew_list(mydb,mycursor,brewIDs):
	"""
	Removes list of brewIDs from beerCode.brewList
	brewIDs = array of IDs to remove from table.
	"""
	try:
		for brewID in brewIDs:
			sql = "DELETE FROM beerCode.brewList WHERE brewID = "+str(brewID)
			mycursor.execute(sql)
			mydb.commit()
			print(mycursor.rowcount, "record(s) deleted")
	except:
		mydb.rollback()
		print("Issue ocurred when trying to delete record(s).")

def add_to_temp_log(mydb,mycursor,brewID,tempAir,tempLiquid):
	"""
	Adds a record to beerCode.brewList.
	brewID = Integer mapping to brewList
	tempAir = Double value of tempAir sensor
	tempLiquid = Double value of tempLiquid sensor
	"""
	ts = time.time()
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	
	sql = "INSERT INTO beerCode.brewTemperatureHistory (brewID,timeMeasurement,tempAir,tempLiquid) VALUES (%s,%s,%s,%s)"
	print(sql)
	val = (brewID,timestamp,tempAir,tempLiquid)

	try:
		mycursor.execute(sql, val)
		mydb.commit()
		print(mycursor.rowcount, "Record inserted.")
	except:
		mydb.rollback()
		print("Issue occurred when trying to write record.")

def remove_from_temp_log(mydb,mycursor,tempIDs):
	"""
	Removes list of tempIDs from beerCode.brewTemperatureHistory
	tempIDs = array of IDs to remove from table.
	"""
	try:
		for tempID in tempIDs:
			sql = "DELETE FROM beerCode.brewTemperatureHistory WHERE tempID = "+str(tempID)
			mycursor.execute(sql)
			mydb.commit()
			print(mycursor.rowcount, "record(s) deleted")
	except:
		mydb.rollback()
		print("Issue ocurred when trying to delete record(s).")
