#!/usr/bin/python
# -*- coding:utf-8 -*-
import smbus
import time

#ADC i2c is at address 0x48
channel=1
address = 0x48
A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43
bus = smbus.SMBus(channel)
while True:
    bus.write_byte(address,A0)
    value = bus.read_byte(address)
    value *= 5
    print("AOUT:%1.3f  " %(value)) #*3.3/255
    time.sleep(0.1)

# avg pulse is 130 units, 5V is 255 units, 3.3V is 162 units
# threshold is 525 units
# so lowest multiple to make 130 above threshold is x 5
# so times adc value x 5
