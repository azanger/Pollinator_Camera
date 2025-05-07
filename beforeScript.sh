#!/usr/bin/bash

. /home/pi/wittypi/utilities.sh

alarmStart=$(/usr/sbin/i2cget -y 1 0x08 9)
alarmStart=$(hex2dec $alarmStart)

alarmShut=$(/usr/sbin/i2cget -y 1 0x08 10)
alarmShut=$(hex2dec $alarmShut)

lastAction=$(/usr/sbin/i2cget -y 1 0x08 11)
lastAction=$(hex2dec $lastAction)

lowV=$(/usr/sbin/i2cget -y 1 0x08 8)
lowV=$(hex2dec $lowV)

#check wakeup flag, if on then:
if [[ $alarmStart -eq 1 ]]; then
    /usr/bin/echo "wakeup flag is 1 -raised-"
    /usr/bin/python3 /home/pi/Pollinator_Camera/Create_Schedule.py
    /usr/bin/echo "Scheduale.wpi created"
    /home/pi/wittypi/runScript.sh
    #/usr/bin/cat /home/pi/wittypi/schedule.wpi
fi

if [[ $lowV -eq 1 ]]; then
    /usr/bin/echo "wakeup after low voltage shutdown and subsequent recharge period"
    #/usr/bin/cat /home/pi/wittypi/schedule.wpi
    /usr/bin/python3 /home/pi/Pollinator_Camera/Create_Schedule.py
    #/usr/bin/cat /home/pi/wittypi/schedule.wpi
    /home/pi/wittypi/runScript.sh
    /usr/bin/tail -n 5 /home/pi/wittypi/schedule.log
fi
#if these flags are all down, then it probably means the camera was started manually
# this could be from the button or auto on by plugging in the usb
if [ $lastAction -eq 3 ]; then 
    /usr/bin/echo $'button clicked to start. \n runScript.sh should automatically revise time to next schedule to compnesate"'

    #/usr/bin/python3 /home/pi/Pollinator_Camera/Create_Schedule.py 
    #/home/pi/wittypi/runScript.sh
fi
