#! /usr/bin/bash

. /home/pi/wittypi/utilities.sh

lowV=$(/usr/sbin/i2cget -y 1 0x08 8)
lowV=$(hex2dec $lowV)
alarmShut=$(/usr/sbin/i2cget -y 1 0x08 10)
alarmShut=$(hex2dec $alarmShut)

#if [[ $alarmShut -eq 1 ]]; then
    #/usr/bin/echo "shutdown flag is 1 -raised-"
    #/usr/sbin/i2cset -y 1 0x08 22 0
    #/usr/bin/echo "Auto On If USB connected set of OFF"
#fi

#if [[ $alarmShut -eq 0 ]]; then
    #/usr/bin/echo "shutdown flag is 0 -down-"
    #/usr/sbin/i2cset -y 1 0x08 22 1
    #/usr/bin/echo "Auto On If USB connected set of ON"
#fi

if [[ $lowV -eq 1 ]]; then
    /usr/bin/echo "Shutting down due to low voltage"
    /usr/bin/python3 /home/pi/Pollinator_Camera/Low_Voltage_Shutdown.py
    /home/pi/wittypi/runscript.sh
fi
