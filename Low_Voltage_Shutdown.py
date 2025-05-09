#! /usr/bin/python3

#This Script is necissary to keep the camera from power cycling every 10 minutes when the v75 runs
#low, but is slowly being charged from solar. The shutdown from low voltage flag is triggered when
#the v75 is empty and the power switches to the 18650 battery. Assuming the low voltage threshold
#is set to ~4-4.2 Volts, the camera will soon shutdown. Originally the camera would wait for power
#from the v75, which begins sending power again once it has charged a little, and automatically
#turns on when it recieves over the 5v USB-C. 

# This appoach worked fine in good conditions, but in cloudy situations, either the v75 would begin sending power before it had enough charge to power the system, or the camera would be trying to boot on power from the solar panel, which was too low, and then causing a kernal panic (lines of @^@^@^@^@^@^@'s in log file ).

# The workaround is this script which shutsdown the camera when the low voltage flag is triggered for a given time and then reboots, at which point hopefully the v75 has recieved enough power to run the camera for a reasonable amount of time before it needs to shutdown again.

import subprocess, datetime
import os.path

#update these to change low voltage shutdown time
shutdownLengthHour = 1
shutdownLengthMin = 0

#gets time from pi, may be slightly off from RTC
today = datetime.datetime.now()

if not os.path.exists("/home/pi/wittypi/schedule.wpi"):
        subprocess.run(["touch", "/home/pi/wittypi/schedule.wpi"])
        subprocess.run("chmod 755 /home/pi/wittypi/schedule.wpi".split())

schWPI = open("/home/pi/wittypi/schedule.wpi", "r")
prevSched = schWPI.readlines()
schWPI.close()

# Get regular schedule shutdown time amount
prevShut = prevSched[4].split("H")
prevShut = prevShut[1].split("M")
prevH = int(prevShut[0].strip().strip("\n"))
prevM = int(prevShut[1].strip().strip("\n"))


# get current shutdown/wakeup time
def get_current_schedule_iso():
    shutdown = ""
    wake = ""
    lastScheWake = subprocess.run(["tail", "-n", "3", "/home/pi/wittypi/schedule.log"], capture_output=True, text=True).stdout
    lastScheWake = lastScheWake.split("\n")
    shutdown = lastScheWake[0].split(":", maxsplit=1)[1].strip()
    wake = lastScheWake[1].split(":", maxsplit=1)[1].strip()
    return (shutdown, wake)

schedule = get_current_schedule_iso()
shutdownDT = datetime.datetime.fromisoformat(schedule[0])
wakeDT = datetime.datetime.fromisoformat(schedule[1])


schWPI = open("/home/pi/wittypi/schedule.wpi", "w")

# if the time difference between current time and orginally scheduled shutdown time is less than the low voltage shutdown time, then just add the difference between now and the original shutdown time to the OFF section of schedule.wpi
Hour = 0
Minute = 0
trig = 0
if today + datetime.timedelta(seconds=(shutdownLengthHour * 3600)+(shutdownLengthMin*60)+120) >= shutdownDT:
    trig = 1
    DeltaH = today - shutdownDT
    Hour = abs(int(DeltaH.total_seconds() // 3600))
    print(Hour)
    Minute = abs(int(round(((DeltaH.total_seconds() / 3600) - DeltaH.total_seconds() // 3600) * 60, 0)))
    print(Minute)


schWPI = open("/home/pi/wittypi/schedule.wpi", "w")
if trig == 0:
    print("Putting Camera to Sleep for an hour to recharge (hopefully)")
    schWPI.write(f"BEGIN {today.isoformat(' ', timespec='minutes')}:00\nEND 2033-01-01 05:00:00\n\nON  H M1 \nOFF  H{shutdownLengthHour} M{shutdownLengthMin}")
else:
    print("Shutting down Camera Early due to low charge, will wake at next scheduled startup.")
    schWPI.write(f"BEGIN {today.isoformat(' ', timespec='minutes')}:00\nEND 2033-01-01 05:00:00\n\nON  H1 M1\nOFF  H{prevH + Hour} M{prevM + Minute}")

schWPI.close()