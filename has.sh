#!/bin/bash

python led.py &
python lux.py &
python pir.py &
python temp.py &
python door.py

exit 0
