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
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #PIR
# Use inbuilt gpio pull-down resistor, PIR activated when pin pulled HIGH 
# Pin is pulled-down to LOW when not active to prevent floating value

#Pir right knob is delay, left knob is sensitivity

#PIR detects change in motion, not just presense of person/ifra-red

# Callback function to run in another thread when button pressed
# check if pin is high
# def motionSensor(channel):
#   if GPIO.input(21): # 1 = rising = motion came on
#     print("Motion detected")


# add event listener on pin 21, to listen and interrupt main loop when detector activates and deactivates
# GPIO.BOTH detects rising and falling
#GPIO.add_event_detect(21, GPIO.BOTH, callback=motionSensor, bouncetime=150) 

db.update({
  u'system1/motion': False
})

try:
  while True:
    #GPIO.wait_for_edge(21, GPIO.BOTH)
    #time.sleep(1)
    motion=GPIO.input(21)
    if motion==1: # 1 = rising = motion came on
      print("Motion detected")

      #record date and time
      date = datetime.datetime.now().strftime("%m/%d/%Y %H:%M")

      # update firebase motion LED
      db.update({
        u'system1/led3': True,
        u'system1/motion': True,
        u'system1/motionTime': date
      })
      # PIR takes roughly 3 seconds to reset
      # wait 3 seconds until listening for movement
      time.sleep(3)
      db.update({
        u'system1/motion': False
      })

except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  

