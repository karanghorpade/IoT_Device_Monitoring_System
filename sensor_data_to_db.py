import json
import sqlite3

# SQLite DB Name
DB_Name =  "Cloud281.db"

#===============================================================
# Database Manager Class

class DatabaseManager():
	def __init__(self):
		self.conn = sqlite3.connect(DB_Name)
		self.conn.execute('pragma foreign_keys = on')
		self.conn.commit()
		self.cur = self.conn.cursor()
		
	def add_del_update_db_record(self, sql_query, args=()):
		self.cur.execute(sql_query, args)
		self.conn.commit()
		return

	def __del__(self):
		self.cur.close()
		self.conn.close()

#===============================================================
# Functions to push Sensor Data into Database

# Function to save Temperature to DB Table
#def DHT22_Temp_Data_Handler(jsonData):
#	#Parse Data 
#	json_Dict = json.loads(jsonData)
#	SensorID = json_Dict['Sensor_ID']
#	Data_and_Time = json_Dict['Date']
#	Temperature = json_Dict['Temperature']
#	
#	#Push into DB Table
#	try12 = (SensorID, Date_n_Time, Temperature)
#	dbObj = DatabaseManager()
#	statm = """INSERT INTO DHT22_Temperature_Data (SensorID, Date_n_Time, Temperature) VALUES (?,?,?);"""
#	dbObj.add_del_update_db_record(statm,try12)
#	del dbObj
#	print("Inserted Temperature Data into Database.")
#	print("")

# Function to save Humidity to DB Table
def Humidity_Data_Handler(jsonData):
	#Parse Data 
	json_Dict = json.loads(jsonData)
	#SensorID = json_Dict['Sensor_ID']
	Data_and_Time = json_Dict['Time']
	Humidity = json_Dict['temprature']
	
	#Push into DB Table
	tt = (Data_and_Time, Humidity)
	dbObj = DatabaseManager()
	statme = """INSERT INTO Temperature_Data (Date_n_Time, Humidity) VALUES (?,?);"""
	dbObj.add_del_update_db_record(statme,tt)
	del dbObj
	print("Inserted Temperature Data into Database.")
	print("")


#===============================================================
# Master Function to Select DB Funtion based on MQTT Topic

def sensor_Data_Handler(Topic, jsonData):
	if Topic == "Home/BedRoom/DHT22/Temperature":
		DHT22_Temp_Data_Handler(jsonData)
	elif Topic == "ashish12/temprature_sensor":
		Humidity_Data_Handler(jsonData)	