#! /usr/bin/python3

# This program sets the onHourOffset, onMinuteOffset, offHourOffset, offMinuteOffset for 
# CreateSchedule.py

# The CreateSchedule.py script works by getting the current days sunset and tomorrow sunrise and 
# setting the camera wakeup and shutdown accordingly. This means the default wakeup and shutdown
# times are always exactly at sunrise or sunset. 

import subprocess, datetime

f = open("/home/pi/Pollinator_Camera/WakeupShutdownOffset.txt", 'w')

hostname = subprocess.run("hostname",capture_output=True, text=True).stdout

RTCTime = subprocess.run("/home/pi/Pollinator_Camera/GetRTCtime.sh", capture_output=True, text=True).stdout
PiTime = subprocess.run("date",capture_output=True, text=True).stdout

# Gets most recently logged scheduled shutdown and wakeup
lastScheWake = subprocess.run(["tail", "-n", "3", "/home/pi/wittypi/schedule.log"], capture_output=True, text=True).stdout
lastScheWake = lastScheWake.split("\n")



#Initial Display
print("-"*100)
print(f"This is Camera {hostname}\n")
print(f"It currently thinks it is {PiTime}while the Real Time Clock thinks it is {RTCTime}\n")
print("These Camera's, by default, base their wakeup/shutdown cycles based on the sunrise and sunset\ntimes in Washington, DC. (Eastern Daylight Time)\n")
print(f"The most recently scheduled shutdown was: {lastScheWake[0]}")
print(f"The most recently scheduled wakeup was: {lastScheWake[1]}")
print("The following prompts will allow you to offset the wakeup/shutdown cylce to account for\nchanging times zones, etc.")
print("\n")
print("-"*100)


onHour = 0
onMinute = 0
offHour = 0
offMinute = 0

onHour = input(f"How many hours to offset from sunrise?\n-- Integers only, use negative numbers to wake before sunrise --\nNumber of hours: ")
onMinute = input("And how many minutes?\n-- Integers only, 0-60 --\nMinutes: ")
offHour = input(f"How many hours to offset from sunset?\n(integers only, use negative numbers to wake before sunset)\nNumber of hours: ")
offMinute = input("And how many minutes?\n-- Integers only, 0-60 --\nMinutes: ")

f.write(f"{onHour}\n{onMinute}\n{offHour}\n{offMinute}")
f.close()

subprocess.run(["python3", "/home/pi/Pollinator_Camera/Create_Schedule.py"])

newSchd = subprocess.run(["tail", "-n", "3", "/home/pi/wittypi/schedule.log"], capture_output=True, text=True).stdout
newSchd = newSchd.split("\n")

print(f"The next scheduled wakeup/shutdown times will be:\n{newSchd[0]}\n{newSchd[1]}")