#! /usr/bin/python3

# This program sets the onHourOffset, onMinuteOffset, offHourOffset, offMinuteOffset for 
# CreateSchedule.py

# The CreateSchedule.py script works by getting the current days sunset and tomorrow sunrise and 
# setting the camera wakeup and shutdown accordingly. This means the default wakeup and shutdown
# times are always exactly at sunrise or sunset. 

from re import sub
import subprocess, datetime, time

f = open("/home/pi/Pollinator_Camera/WakeupShutdownOffset.txt", 'w')

hostname = subprocess.run("hostname",capture_output=True, text=True).stdout

RTCTime = subprocess.run("/home/pi/Pollinator_Camera/GetRTCtime.sh", capture_output=True, text=True).stdout
PiTime = subprocess.run("date",capture_output=True, text=True).stdout

# Gets most recently logged scheduled shutdown and wakeup
lastScheWake = subprocess.run(["tail", "-n", "3", "/home/pi/wittypi/schedule.log"], capture_output=True, text=True).stdout
lastScheWake = lastScheWake.split("\n")



#Set Time if wrong
print("-"*100)
print("**Currently this script does not check for errors when running, if you enter an incorrect time or date, press 'Ctrl+c' and run PreDeploy again**")
#print("**There is also a bug, where entering the hour offset for sunrise, it adds an extra hour,")
print(f"This is Camera: {hostname}\n")
print(f"The Camera currently thinks it is {PiTime}while the Real Time Clock thinks it is {RTCTime}\n")


answer = input("If the time that the camera thinks it is is wrong, type y to update, otherwise type n:  ")

if answer.lower() == "y":
    man_date_time = input("Enter a date and time that has this format -> YYYY-MM-DD HH:mm :")
    man_date_time = man_date_time + ":00"
    subprocess.run(["sudo", "date", "-s", man_date_time])
    set_date_time = subprocess.run("date", capture_output=True, text=True).stdout
    subprocess.run("/home/pi/Pollinator_Camera/System_to_rtc.sh")
    print(f"The Camera's date and time was set to {set_date_time}")
else:
    print(f"The Camera's date and time will remain {PiTime}")

time.sleep(.2)
print(".")
time.sleep(.2)
print(".")
time.sleep(.2)
print(".\n")

# set offset from sunrise/sunset
print("These Camera's, by default, base their wakeup/shutdown cycles based on the sunrise and sunset\ntimes in Washington, DC. (Eastern Daylight Time)\n")
print(f"The most recently scheduled shutdown was: {lastScheWake[0]}")
print(f"The most recently scheduled wakeup was: {lastScheWake[1]}")
print("The following prompts will allow you to offset the wakeup/shutdown cylce to account for\nchanging times zones, etc.")
print("\n")
print("-"*100)
print("\n")


onHour = 0
onMinute = 0
offHour = 0
offMinute = 0

onHour = input(f"How many hours to offset from sunrise?\n-- Integers only, use negative numbers to wake (day camera) or shutdown (night camera) before sunrise --\nNumber of hours: ")
onMinute = input("And how many minutes?\n-- Integers only, 0-60 --\nMinutes: ")
offHour = input(f"How many hours to wake from sunset?\n(integers only, use negative numbers to wake (day camera) or shutdown (night camera) before sunset)\nNumber of hours: ")
offMinute = input("And how many minutes?\n-- Integers only, 0-60 --\nMinutes: ")

f.write(f"{onHour}\n{onMinute}\n{offHour}\n{offMinute}")
f.close()

time.sleep(.2)
print(".")
time.sleep(.2)
print(".")
time.sleep(.2)
print(".\n")

subprocess.run(["python3", "/home/pi/Pollinator_Camera/Create_Schedule.py"])
print("The following is the schedule.wpi script that was created and the resulting shutdown and startup times")
subprocess.run("/home/pi/wittypi/runScript.sh")

newSchd = subprocess.run(["tail", "-n", "4", "/home/pi/wittypi/schedule.wpi"], capture_output=True, text=True).stdout
newSchd = newSchd.split("\n")

print(f"The next scheduled shutdown will be in:\n{newSchd[2][2:]}")
print(f"It will then wake up after: \n{newSchd[3][2:]}")

