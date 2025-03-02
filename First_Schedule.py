#!/usr/bin/python3

from os import scandir
import datetime, getpass, subprocess, os.path

today = datetime.datetime.now()
user = getpass.getuser()

fromSH = open(f"/home/{user}/SPC/SchedulingHours.txt", "r")
if not os.path.exists("/home/pi/wittypi/schedule.wpi"):
    subprocess.run(["touch", f"/home/{user}/wittypi/schedule.wpi"])
schWPI = open("/home/pi/wittypi/schedule.wpi", "w")



fromSHL = fromSH.readlines()
fromSH.close()

#format today time for schWPI
fmonth = str(today.month)
fday = str(today.day)
fhour = str(today.hour)
fmin = str(today.minute)

if len(str(fmonth)) < 2:
    fmonth = "0" + fmonth

if len(str(fday)) < 2:
    fday = "0" + fday

if len(str(fhour)) < 2:
    fhour = "0" + fhour
if len(fmin) < 2:
    fmin = "0" + fmin    




hoursMinutesList = []
for line in fromSHL:
    strip = line.strip("\n")
    split = strip.split(",")
    hoursMinutesList.append(split)

dayOfYear = today.date() - datetime.date(today.year, 1, 1)
#print(dayOfYear.days + 1)
#print(hoursMinutesList[58])

#Create Datetime Object of Current days sunrise/sunset time
todaySunrise = datetime.datetime.fromisoformat(hoursMinutesList[dayOfYear.days][2])
todaySunset = datetime.datetime.fromisoformat(hoursMinutesList[dayOfYear.days][3])
try:
    onHour = int(hoursMinutesList[dayOfYear.days][0])
    onMinute = int(hoursMinutesList[dayOfYear.days][1])
    offHour = 24 - int(hoursMinutesList[dayOfYear.days + 1][0])
    offMinute = 60 - int(hoursMinutesList[dayOfYear.days + 1][1])
    #print(int(hoursMinutesList[dayOfYear.days + 1][0]))
except IndexError:
    #print("IndexError")
    onHour = int(hoursMinutesList[dayOfYear.days][0])
    onMinute = int(hoursMinutesList[dayOfYear.days][1])
    offHour = 24 - int(hoursMinutesList[dayOfYear.days][0])
    offMinute = 60 - int(hoursMinutesList[dayOfYear.days][1])

# if the current time is between sunrise and sunset
if today > todaySunrise and today < todaySunset:
    print("A")
    Delta = today - todaySunset
    onHour = int(Delta.total_seconds() * -1 // 3600)
    onMinute = int(round(((Delta.total_seconds() * -1 / 3600) - onHour) * 60, 0))
    schWPI.write(f"BEGIN {today.year}-{fmonth}-{fday} {fhour}:{fmin}:00\nEND 2033-01-01 05:00:00\n\nON  H{onHour} M{onMinute}\nOFF  H{offHour} M{offMinute}")


#If the Camera is being deployed after that days sunset or before the next days sunrise. 
#The Camera will stay on for 20 minutes to allow setup and the shutdown until it is scheduled to boot again
elif today < todaySunrise + datetime.timedelta(days=1) and today > todaySunset:
    print("B")
    Delta = today - (todaySunrise + datetime.timedelta(days=1))
    onHour = 0
    onMinute = 20
    offHour = int(abs(Delta.total_seconds() // 3600))
    offMinute = int((1 + (abs(Delta.total_seconds() / 3600) - offHour)) * 60)
    schWPI.write(f"BEGIN {today.year}-{fmonth}-{fday} {fhour}:{fmin}:00\nEND 2033-01-01 05:00:00\n\nON  H{onHour} M{onMinute}\nOFF  H{offHour} M{offMinute}")

schWPI.close()
#print("1:",Delta.total_seconds() // 3600, "2:", onHour, "3:", onMinute, "4:", offHour, "5:", offMinute)
#print(f"BEGIN 2025-01-01 05:00:00\nEND 2040-01-01 05:00:00\n\nON  H{onHour} M{onMinute}\nOFF  H{offHour} M{offMinute}")

