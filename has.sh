#!/bin/bash

python3 led.py &
python3 lux.py &
python3 pir.py &
python3 temp.py

exit 0
