''' 
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

n03Sensor = []
doSensor = []
nh4Sensor = []

n03Average = 0
doAverage = 0
nh4Average = 0

gdx1 = gdx.gdx()
try: 
    gdx1.open_usb() # This code uses the gdx functions to collect data from your Go Direct sensors.
    gdx1.select_sensors()
    gdx1.start(500) #Record sensor data every 500ms.
except KeyError:
    print ( "Key Error FOOBAR" )

formattedString = ""

while True:
    for i in range(0,5): #Recording sensor data for 5 minutes. 5 minutes has 600 units of 500ms.
        measurements = gdx1.read()
        n03Sensor.append ( measurements [ 0 ] )
        doSensor.append ( measurements [ 1 ] )
        nh4Sensor.append ( measurements [ 2 ] )
        if measurements == None:
            break 
        print(measurements)

    n03Average = sum(n03Sensor) / 5
    doAverage = sum(doSensor) / 5
    nh4Average = sum(nh4Sensor) / 5

    n03Sensor.clear()
    doSensor.clear()
    nh4Sensor.clear()

    #print (n03Average, doAverage, nh4Average )
    formattedString =  str ( time.time() ) + ";" + (str ( n03Average )  + "," + str ( doAverage ) + "," + str ( nh4Average ) )


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