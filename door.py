import RPi.GPIO as GPIO
import time
import datetime

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

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# GPIO.setup(8, GPIO.IN)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Use inbuilt gpio pull-up resistor, sensor activated when pin pulled HIGH 
# Pin is pulled-up to HIGH when not active (door open) to prevent floating value


# check if pin is high
def doorSensor():
   if GPIO.input(8): # 1 = rising = door came on
      print("Door is open")
      #record date and time
      date = datetime.datetime.now().strftime("%m/%d/%Y %H:%M")
      # # update firebase door LED
      db.update({
         u'system1/led3': True,
         u'system1/door': True,
         u'system1/doorTime': date
      })
      # time.sleep(1)
      
   if GPIO.input(8) == False:
      print("Door is closed")
      # update firebase door LED
      db.update({
         u'system1/led3': False,
         u'system1/door': False
      })
      # time.sleep(1)

# Callback function to run in another thread when door sensor triggered
def inputChng(channel):
   doorSensor()

# add event listener on pin 8, to listen and interrupt main loop when detector activates and deactivates
# GPIO.BOTH detects rising and falling
GPIO.add_event_detect(8, GPIO.BOTH, callback=inputChng, bouncetime=30)

try:
   # check status when first executed
   doorSensor()

   while True:
      
      # infinitely do nothing
      time.sleep(1)


except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  

