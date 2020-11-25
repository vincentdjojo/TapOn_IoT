# Check devices on Raspberry Pi's ports: python -m serial.tools.miniterm
# Code for microbit: https://makecode.microbit.org/93193-13394-23340-40251
# Import Libraries
import serial
import time

# Set up the Serial connection to capture the Microbit communications
ser = serial.Serial()
ser.baudrate = 115200
ser.port = "/dev/ttyACM0"
ser.open()

# Loop forever
while True:
    
    # Read in a line from the Microbit, store it in variable 'microbitdata' as a string
    microbitdata = str(ser.readline())
    
    # Cleanup the data from the microbit and convert it to an integer
    temperature = microbitdata[2:]
    temperature = temperature.replace(" ","")
    temperature = temperature.replace("\\r\\n","")
    temperature = temperature.replace("'","")
    temperature = int(temperature)

    # Print the returned unique ID from Firebase on receipt of our data
    print("The temperature is ",temperature)
    
    # Pause for 5 seconds between loops
    time.sleep(5)

# Close the serial connection
ser.close()

