''' 
This Python program runs on a Raspberry Pi 4 with three Vernier sensors connected to the USB ports of the Raspberry Pi. 
The program collects data from the sensor every 500ms and uploads the data to MongoDB.

Some issues faced tackling this program:
1. https://github.com/VernierST/godirect-examples/issues/30 ( Is it possible to record using more than 1 sensor at a time? )
2. https://github.com/VernierST/godirect-examples/issues/31 ( Can't get Vernier temperature bluetooth sensor to Raspberry Pi using GoDirect library. )

Libraries Needed:
1. Go Direct Libraries (gdx) from vernier. Installation here: https://vernierst.github.io/godirect-examples/python/.
2. PyMongo to connect Python to MongoDB. Type "pip3 install pymongo" on terminal.

The gdx functions are located in a gdx.py file inside a folder named "gdx". In order for 
the import to find the gdx folder, the folder needs to be in the same directory as this python program.

The gdx functions used in a typical program to collect data include:

gdx.open_usb() or gdx.open_ble()
gdx.select_sensors()
gdx.start()
gdx.read()
gdx.stop()
gdx.close() 

Below is a simple starter program that uses these functions to collect data from a Go Direct 
device (or devices) connected via USB. This example will provide you with prompts to select 
the sensors and the sampling period. Try a period of 1000 ms (1 sample/second). 

Tip: Skip the prompts to select the sensors and period by entering arguments in the functions.
Example 1, collect data from sensor 1 at a period of 1000ms using:
gdx.select_sensors([1]), gdx.start(1000)
Example 2, collect data from sensors 1, 2 and 3 at a period of 100ms using:
gdx.select_sensors([1,2,3]), gdx.start(100)
Is it possible to record using more than 1 sensor at a time?
'''
    
# 
# This code imports the gdx functions. 
from gdx import gdx
import time
import pymongo
from pymongo import MongoClient
#mongodb://user:uCqRhJWpgTSCOQiK@cluster0-shard-00-00.ewnsy.mongodb.net:27017,cluster0-shard-00-01.ewnsy.mongodb.net:27017,cluster0-shard-00-02.ewnsy.mongodb.net:27017/tapon?ssl=true&replicaSet=atlas-t6f42j-shard-0&authSource=admin&retryWrites=true&w=majority
client = MongoClient( "mongodb://user:uCqRhJWpgTSCOQiK@cluster0-shard-00-00.ewnsy.mongodb.net:27017,cluster0-shard-00-01.ewnsy.mongodb.net:27017,cluster0-shard-00-02.ewnsy.mongodb.net:27017/tapon?ssl=true&replicaSet=atlas-t6f42j-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client["tapon"]
collection = db ["datas"]

timer = 0

windSpeed = []
windDirection = []
windChill = []
temperature = []
heatIndex =[]
dewPoint = []
relativeHumidity = []
absoluteHumidity = []
stationPressure = []
barometricPressure = []
altitude = []

windSpeedAverage = 0
windDirectionAverage = 0
windChillAverage = 0
temperatureAverage = 0
heatIndexAverage = 0
dewPointAverage = 0
relativeHumidityAverage = 0
absoulteHumidityAverage = 0
stationPressureAverage = 0
barometricePressureAverage = 0
altitudeAverage = 0

gdx1 = gdx.gdx()
try: 
    gdx1.open_usb() # This code uses the gdx functions to collect data from your Go Direct sensors.
    gdx1.select_sensors()
    gdx1.start(500) #Record sensor data every 500ms.
except KeyError:
    print ( "Key Error FOOBAR" )

formattedString = ""

while True:
    for i in range(0,5): #Recording sensor data for 2500ms every 500ms. 5 readings every 2500ms.
        measurements = gdx1.read()
        
        #Store sensor data into array.
        windSpeed.append ( measurements [ 0 ] )
        windDirection.append ( measurements [ 1 ] ) 
        windChill.append ( measurements [ 2 ] ) 
        temperature.append ( measurements [ 3 ] )
        heatIndex.append ( measurements [ 4 ] )
        dewPoint.append ( measurements [ 5 ] )
        relativeHumidity.append ( measurements [ 6 ] )
        absoluteHumidity.append ( measurements [ 7 ] )
        stationPressure.append ( measurements [ 8 ] )
        barometricPressure.append ( measurements [ 9 ] )
        altitude.append ( measurements [ 10 ] )
        if measurements == None:
            break 
        print(measurements)

    #Get the sum of each sensor data array and divide them by 5 for the average of each array.
    windSpeedAverage = sum ( windSpeed ) / 5 
    windDirectionAverage = windDirection.pop()
    windChillAverage = sum ( windChill ) / 5
    temperatureAverage = sum ( temperature ) / 5
    heatIndexAverage = sum ( heatIndex ) / 5
    dewPointAverage = sum ( dewPoint ) / 5
    relativeHumidityAverage = sum ( relativeHumidity ) / 5
    absoluteHumidityAverage = sum ( absoluteHumidity ) / 5
    stationPressureAverage = sum ( stationPressure ) / 5
    barometricPressureAverage = sum ( barometricPressure ) / 5
    altitudeAverage = sum ( altitude ) / 5
    
    #Clear each array for further use when the while loop repeats itself.
    windSpeed.clear ()
    windDirection.clear ()
    windChill.clear ()
    temperature.clear ()
    heatIndex.clear ()
    dewPoint.clear ()
    dewPoint.clear ()
    relativeHumidity.clear ()
    absoluteHumidity.clear ()
    stationPressure.clear ()
    barometricPressure.clear()
    altitude.clear ()
    
    #Format string into comma seperated values for parsing on MongDB.
    formattedString =  str ( time.time() ) + ";" + ( str ( windSpeedAverage )  + "," + str ( windDirectionAverage ) + "," + str ( windChillAverage ) + "," + str(temperatureAverage) + "," + str ( heatIndexAverage ) + "," + str(dewPointAverage) + "," + str(relativeHumidityAverage) + "," + str(absoluteHumidityAverage) + "," + str(stationPressureAverage) + "," + str(barometricPressureAverage) + "," + str(altitudeAverage) )

    #Upload the formatted string to MongoDB database. It updates the same cell everytime it uploads on MongoDB.
    myquery = { "id": "0" }
    newvalues = { "$set": { "piString":formattedString } }
    collection.update_one(myquery, newvalues)
    
print ( "Stored Sensor Data:\n" )
print ( n03Sensor )
print ( doSensor )
print ( nh4Sensor )
print (formattedString)

gdx1.stop()
gdx1.close()
