import RPi.GPIO as GPIO
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#GPIO set up led pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

# Use the application default credentials
cred = credentials.Certificate('/home/pi/Documents/FYP/ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

# query for document - adds doc if it doesn't exist
# TO DO - GET DOC OF A SPECIFIC USER
doc_ref = db.collection(u'RPi').document(u'system1')

# MAIN FUNCTION
while True:
  # get document data
  doc = doc_ref.get()

  #get led values set the gpio values
  led1Val = doc.get("led1")
  GPIO.output(27, led1Val)
  led2Val = doc.get("led2")
  GPIO.output(17, led2Val)

  # sleep for 1 second so that file isn't rinsing operations usage
  time.sleep(1)

GPIO.cleanup()

# for doc in docs:
#     print(u'{} => {}'.format(doc.id, doc.to_dict()))
#     print(doc.to_dict())
