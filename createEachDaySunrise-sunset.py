#! /usr/bin/python3

# This script script takes as input a table (csv)of a year of sunrise and sunsets.
#It transforms the input into a csv where each line's index is the day of the year(doy) - 1.
#The format of each line is: 
#(sunrise's YYYY:MM:DD HH:mm:SS), (sunset's YYYY:MM:DD HH:mm:SS)
import datetime
import getpass


# get csv of sunset and sunrise times
user = getpass.getuser()
if user == "pi":
    ss = open(f"/home/{user}/SPC/sunrise_sunset.csv")
else:
    ss = open("/home/aps_desktop/Pollinator_Camera/sunrise_sunset.csv")
sslines = ss.readlines()
ss.close()
#print(sslines)
ssll = [] #list of rows
for line in sslines:
    strip = line.strip("\n")
    split = strip.split(",")

    ssll.append(split)

# Dictionary key = month, value = list of [sunrise, sunset] pair for each day in month
ssdic ={1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}

# year to assign to each datetime object
year = datetime.date.today().year


# for each key, add each day of months [sunrise, sunset] pair.
## days of month are organized by column in csv
countE = 0
for key in ssdic.keys():
    
    countLine = 0
    
    while countLine < len(ssll):
        ssdic[key].append([ssll[countLine][countE], ssll[countLine][countE + 1]])
        #print(ssdic[key], len(ssdic[key]))
        countLine += 1
    countE += 2

# create a list of date objects, from ssdic
## currently if a day's sunrise and sunset pair has the same time as the previous it will use the index 
# of the first instance of that duplicate pair 
datelist = []
for key in ssdic.keys():
    for pair in range(len(ssdic[key])):
        try:
            day = ssdic[key].index(ssdic[key][pair])+ 1
            if ssdic[key].index(ssdic[key][pair])+ 1 == ssdic[key].index(ssdic[key][pair - 1])+ 1:
                day += 1
            sunrise = datetime.datetime(year=year, month=int(key), day=day, hour=int(ssdic[key][pair][0][:2]), minute=int(ssdic[key][pair][0][2:]))
            sunset = datetime.datetime(year=year, month=int(key), day=day, hour=int(ssdic[key][pair][1][:2]), minute=int(ssdic[key][pair][1][2:]))
            datelist.append(sunrise)
            datelist.append(sunset)
        except ValueError:
            break


# finds duplicate dates and increments them as necessary 
for date in range(len(datelist)-2): # for each date
    if datelist[date] == datelist[date + 2]: # if current date == two dates ahead
        # print("befre loop", datelist[date], datelist[date + 2])
        count = 2                                   # set count to 2
        while datelist[date + count].day == datelist[date].day: # while the current date is the same as the date + count dates ahead
            # print("loop -start", datelist[date].day, datelist[date + count].day, count)
            day = datelist[date].day + (count // 2)
            datelist[date + count] = datelist[date + count].replace(day=day)
            count += 1
            # print("loop -end", datelist[date].day, datelist[date + count].day, count, day)



# # calculates diferrence of each days sunset - sunrise
# # each item in list is a timeDelta object.
# deltalist = []
# for date in range(len(datelist)):
#     if date % 2 == 0:
#         deltalist.append(datelist[date + 1] - datelist[date])

#write 
#sunrise date (isoformat), sunset date (isoformat)
if user == "pi":
    toScheduling = open(f"/home/{user}/Pollinator_Camera/each_day_sunrise-sunset.txt", "w")
else:
    toScheduling = open(f"/home/{user}/Pollinator_Camera/each_day_sunrise-sunset.txt", "w")
for d in range(len(datelist) // 2):
    toScheduling.write(datelist[d*2].isoformat(" ") + "," + datelist[d*2 + 1].isoformat(" ") + "\n")

toScheduling.close()
