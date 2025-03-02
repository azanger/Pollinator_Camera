#! /usr/bin/python3

import datetime
import os.path
import subprocess
import getpass


today = datetime.datetime.now()
user = getpass.getuser()

fromSH = open(f"/home/{user}/SPC/SchedulingHours.txt", "r")
if not os.path.exists("/home/pi/wittypi/schedule.wpi"):
    subprocess.run(["touch", f"/home/{user}/wittypi/schedule.wpi"])
schWPI = open("/home/pi/wittypi/schedule.wpi", "w")


fromSHL = fromSH.readlines()
fromSH.close()


hoursMinutesList = []
for line in fromSHL:
    strip = line.strip("\n")
    split = strip.split(",")
    hoursMinutesList.append(split)


dayOfYear = today.date() - datetime.date(today.year, 1, 1)

#Create Datetime Object of Current days sunrise/sunset time
todaySunrise = datetime.datetime.fromisoformat(hoursMinutesList[dayOfYear.days][2])
todaySunset = datetime.datetime.fromisoformat(hoursMinutesList[dayOfYear.days][3])
try:
    onHour = int(hoursMinutesList[dayOfYear.days][0])
    onMinute = int(hoursMinutesList[dayOfYear.days][1])
    offHour = 24 - int(hoursMinutesList[dayOfYear.days + 1][0])
    offMinute = 60 - int(hoursMinutesList[dayOfYear.days + 1][1])
except IndexError:
    onHour = int(hoursMinutesList[dayOfYear.days][0])
    onMinute = int(hoursMinutesList[dayOfYear.days][1])
    offHour = 24 - int(hoursMinutesList[dayOfYear.days][0])
    offMinute = 60 - int(hoursMinutesList[dayOfYear.days][1])


#print(today, onHour, onMinute, offHour, offMinute)
#schedule.wpi has the format
#BEGIN YYYY-MM-DD HH:mm:SS
#END YYYY-MM-DD HH:mm:SS

#ON D(days) H(hours) M(minutes) S(seconds) -may omit unused
#OFF D(days) H(hours) M(minutes) S(seconds) -may omit unused

schWPI.write(f"BEGIN {today.year}-{fmonth}-{fday} {fhour}:{fmin}:00\nEND 2033-01-01 05:00:00\n\nON  H{onHour} M{onMinute}\nOFF  H{offHour} M{offMinute}")

