import smbus
import time

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

# Get lux sensor values
def lux_reading():
  # Get i2c scl and sda address of sensor 
  # $ i2cdetect -y 1, useful to detect i2c sensors - 0x39
  bus = smbus.SMBus(1)

  # TSL2561 address, 0x39(57)
  # Select control register, 0x00(00) with command register, 0x80(128)
  #		0x03(03)	Power ON mode
  bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
  # TSL2561 address, 0x39(57)
  # Select timing register, 0x01(01) with command register, 0x80(128)
  #		0x02(02)	Nominal integration time = 402ms
  bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)

  time.sleep(0.5)

  # Read data back from 0x0C(12) with command register, 0x80(128), 2 bytes
  # ch0 LSB, ch0 MSB
  data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
  
  # Read data back from 0x0E(14) with command register, 0x80(128), 2 bytes
  # ch1 LSB, ch1 MSB
  data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)

  # Convert the data
  ch0 = data[1] * 256 + data[0]
  ch1 = data1[1] * 256 + data1[0]
  # only conserned with visible light, not infrared
  visible_lux = ch0 - ch1
  return visible_lux



# query for document - adds doc if it doesn't exist
# TO DO - GET DOC OF A SPECIFIC USER

while True:
  # get lux value
  lux = lux_reading()
  # set lux value in firestore
  db.update({
    u'system1/lux': lux
  })

  #automate led 
  #get threshold value  
  # TO DO - GET DOC OF A SPECIFIC USER
  threshold = db.child("system1/luxThreshold").get().val()

  # if lux is below threshold, turn on led2
  if lux < threshold:
    db.update({
      u'system1/led2': True
    })
  else:
    db.update({
      u'system1/led2': False
    })
  # sleep for 1 second so that file isn't rinsing operations usage
  time.sleep(0.25)

# Lux value guide table

# Lighting condition	From (lux)	To (lux)	Mean value (lux)	Lighting step
# Pitch Black	          0	          10	        5	              1
# Very Dark	            11	        50	        30	            2
# Dark Indoors	        51	        200	        125	            3
# Dim Indoors	          201	        400	        300	            4
# Normal Indoors	      401	        1000	      700	            5
# Bright Indoors	      1001	      5000	      3000	          6
# Dim Outdoors	        5001	      10,000	    7500	          7
# Cloudy Outdoors	      10,001	    30,000	    20,000	        8
# Direct Sunlight	      30,001	    100,000	    65,000	        9
