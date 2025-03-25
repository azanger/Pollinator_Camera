#! /usr/bin/python3

import datetime
import os.path
import subprocess
import getpass
from os import access


today = datetime.datetime.now()
user = getpass.getuser()
hostname = subprocess.run("hostname",capture_output=True, text=True).stdout

# load offset file
f = open("/home/pi/Pollinator_Camera/WakeupShutdownOffset.txt")
offsets = f.readlines()
f.close()

OnUserOffsetHour = int(offsets[0].strip())
OnUserOffsetMin = int(offsets[1].strip())
OffUserOffsetHour = int(offsets[2].strip())
OffUserOffsetMin = int(offsets[3].strip())


print("CreateScript.py is being run")
# Open each_day_sunrise-sunset.txt and schedule.wpi
fromSH = open(f"/home/pi/Pollinator_Camera/each_day_sunrise-sunset.csv", "r")
if user == "pi" or user == "root":
    if not os.path.exists("/home/pi/wittypi/schedule.wpi"):
        subprocess.run(["touch", "/home/pi/wittypi/schedule.wpi"])
        subprocess.run("chmod 755 /home/pi/wittypi/schedule.wpi".split())
    subprocess.run("chmod 755 /home/pi/wittypi/schedule.wpi".split())
    schWPI = open("/home/pi/wittypi/schedule.wpi", "w")
else:
    print(f"username is not pi, therefore assuming this isn't a raspberry pi, saving schedule.wpi to /home/{user}/Pollinator_Camera")
    if not os.path.exists("/home/{user}/Pollinator_Camera/schedule.wpi"):
        subprocess.run(["touch", f"/home/{user}/Pollinator_Camera/schedule.wpi"])
        subprocess.run(f"sudo chmod 755 /home/{user}/wittypi/schedule.wpi".split())
    schWPI = open(f"/home/{user}/Pollinator_Camera/schedule.wpi", "w")
fromSHL = fromSH.readlines()
fromSH.close()


SrSS_isoformat = []
for line in fromSHL:
    strip = line.strip("\n")
    split = strip.split(",")
    SrSS_isoformat.append(split)

#dayOfYear is actually one day before today, but the day is correct if indexing from 0
dayOfYear = today.date() - datetime.date(today.year, 1, 1)
#print(dayOfYear)
todaySunrise = datetime.datetime.fromisoformat(SrSS_isoformat[dayOfYear.days][0])
todaySunset = datetime.datetime.fromisoformat(SrSS_isoformat[dayOfYear.days][1])
try:
    tomorrowSunrise = datetime.datetime.fromisoformat(SrSS_isoformat[dayOfYear.days + 1][0])
    tomorrowSunset = datetime.datetime.fromisoformat(SrSS_isoformat[dayOfYear.days + 1][1])
except IndexError:
    tomorrowSunrise = datetime.datetime.fromisoformat(SrSS_isoformat[0][0])
    tomorrowSunset = datetime.datetime.fromisoformat(SrSS_isoformat[0][1])


# Calculate on time and off time for day camera
try:
    if "day" in hostname.lower():
        DeltaOn = todaySunset - today
        onHour = int(DeltaOn.total_seconds() // 3600)
        onMinute = int(round(((DeltaOn.total_seconds() / 3600) - onHour) * 60, 0))
        DeltaOff = tomorrowSunrise - todaySunset
        offHour = int(DeltaOff.total_seconds() // 3600)
        offMinute = int(((DeltaOff.total_seconds() / 3600) - offHour) * 60)


    elif "night" in hostname.lower():
        DeltaOn = tomorrowSunrise - today
        onHour = int(DeltaOn.total_seconds() // 3600)
        onMinute = int(round(((DeltaOn.total_seconds() / 3600) - onHour) * 60, 0))
        DeltaOff = tomorrowSunset - tomorrowSunrise
        offHour = int(DeltaOff.total_seconds() // 3600)
        offMinute = int(((DeltaOff.total_seconds() / 3600) - offHour) * 60)

    #print(f"BEGIN {todaySunrise.isoformat(' ')}\nEND 2033-01-01 05:00:00\n\nON  H{onHour} M{onMinute}\nOFF  H{offHour} M{offMinute}")
    schWPI.write(f"BEGIN {today.isoformat(' ', timespec='minutes')}:00\nEND 2033-01-01 05:00:00\n\nON  H{onHour + OnUserOffsetHour} M{onMinute + OnUserOffsetMin}\nOFF  H{offHour + OffUserOffsetHour} M{offMinute + OffUserOffsetMin}")


except NameError:
    print("---Hostname does not contain word day or night.\nIn order for the Camera to know how to create a schedule,\nThe hostname needs to have the word 'day' for a day camera or 'night' for night camera, not case sensitive.\nTo update the hostname:\nopen a terminal window (ctl+alt+t)\ntype 'sudo raspi-config' and press enter\npress enter again to select 'system options'\nSelect hostname\ntype a new hostname with the word night or day somewhere in it and then select 'ok'\n finally select 'yes' when asked to reboot.")


#print(today, onHour, onMinute, offHour, offMinute)
#schedule.wpi has the format
#BEGIN YYYY-MM-DD HH:mm:SS
#END YYYY-MM-DD HH:mm:SS

#ON D(days) H(hours) M(minutes) S(seconds) -may omit unused
#OFF D(days) H(hours) M(minutes) S(seconds) -may omit unused




