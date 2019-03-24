import RPi.GPIO as GPIO
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

#GPIO set up led pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT) #led1
GPIO.setup(27, GPIO.OUT) #led2 - lux
GPIO.setup(22, GPIO.OUT) #led3 - motion
GPIO.setup(11, GPIO.OUT) #led4 - heating

# for doc in docs:
#     print(u'{} => {}'.format(doc.id, doc.to_dict()))
#     print(doc.to_dict())

# MAIN FUNCTION
try:
  while True:

    # query for document - adds doc if it doesn't exist
    # TO DO - GET DOC OF A SPECIFIC USER
    #get led values set the gpio values
    #manual light
    led1Val = db.child("system1/led1").get()
    GPIO.output(27, led1Val.val())
    #auto light
    led2Val = db.child("system1/led2").get()
    GPIO.output(17, led2Val.val())
    #motion light
    led3Val = db.child("system1/led3").get()
    GPIO.output(22, led3Val.val())
    #heating light
    led4Val = db.child("system1/led4").get()
    GPIO.output(11, led4Val.val())

    # sleep for 1 second so that file isn't rinsing operations usage
    time.sleep(0.1)

except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  
