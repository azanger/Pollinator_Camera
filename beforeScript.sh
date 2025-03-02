#!bin/bash

. /home/pi/wittypi/utilities.sh

alarmStart=$(/usr/sbin/i2cget -y 1 0x08 9)
alarmStart=$(hex2dec $alarmStart)

alarmShut=$(/usr/sbin/i2cget -y 1 0x08 10)
alarmShut=$(hex2dec $alarmShut)

lowV=$(/usr/sbin/i2cget -y 1 0x08 8)
lowV=$(hex2dec $lowV)

if [[ $alarmStart -eq 1 ]]; then
    /usr/bin/echo "wakeup flag is 1 -raised-"
    /usr/sbin/i2cset -y 1 0x08 22 1
    /usr/bin/echo "Auto On If USB connected set of ON"
    /usr/bin/python3 /home/pi/SPC/Create_Schedule.py &
    /usr/bin/echo "Scheduale.wpi created"
    /home/pi/wittypi/runScript.sh
    /usr/bin/cat /home/pi/wittypi/schedule.wpi
    /usr/sbin/i2cset -y 1 0x08 22 1
    /usr/bin/echo "AutoOn set to ON"
fi

if [ $lowV -eq 0 ] && [ $alarmShut -eq 0 ] && [ $alarmStart -eq 0 ]; then
    /usr/bin/python3 
fi