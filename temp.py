import time
import smbus

# import board
# import busio
# import adafruit_mcp9808

import pyrebase

# Don't make this info public!!!
config = {
  "apiKey": "AIzaSyB1X48SrnZyb0IE4j8UDooTmqmX7-cdgXY",
  "authDomain": "smart-home-pwa.firebaseapp.com",
  "databaseURL": "https://smart-home-pwa.firebaseio.com",
  "storageBucket": "smart-home-pwa.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

def temp_reading():
    # Get i2c scl and sda address of sensor 
    # $ i2cdetect -y 1, useful to detect i2c sensors - 0x18 and 0x48      
    bus = smbus.SMBus(1)

    # MCP9808 address, 0x18(24)
    # Select configuration register, 0x01(1)
    #		0x0000(00)	Continuous conversion mode, Power-up default
    config = [0x00, 0x00]
    bus.write_i2c_block_data(0x18, 0x01, config)
    # MCP9808 address, 0x18(24)
    # Select resolution rgister, 0x08(8)
    #		0x03(03)	Resolution = +0.0625 / C
    bus.write_byte_data(0x18, 0x08, 0x03)

    
    time.sleep(0.5)

    # MCP9808 address, 0x18(24)
    # Read data back from 0x05(5), 2 bytes
    # Temp MSB, TEMP LSB
    data = bus.read_i2c_block_data(0x18, 0x05, 2)

    # Convert the data to 13-bits
    ctemp = ((data[0] & 0x1F) * 256) + data[1]
    if ctemp > 4095 :
        ctemp -= 8192
    ctemp = ctemp * 0.0625
    return ctemp

# adafruit way
# bus = busio.I2C(board.SCL, board.SDA) 
# mcp = adafruit_mcp9808.MCP9808(bus)


while True:
    # temp = mcp.temperature
    temp = temp_reading()
    tempC = round(temp,1) #round float to 1dp

    # print(tempC)

    #update temp value to rtd
    db.update({
        u'system1/temp': tempC
    })

    #automate temp 
    #get threshold value
    # TO DO - GET DOC OF A SPECIFIC USER
    threshold = db.child("system1/tempThreshold").get().val()

    # if lux is below threshold, turn on led2
    if tempC < threshold:
        db.update({
            u'system1/led4': True
        })
    else:
        db.update({
            u'system1/led4': False
        })
    # sleep for 1 second so that file isn't rinsing operations usage
    time.sleep(0.25)

