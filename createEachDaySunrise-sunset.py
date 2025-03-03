#! /usr/bin/python3
# from a list where rows == day of month, create a dictionary where key = month, 
# value = list of sunrise sunset pairs
import datetime
import getpass


# get csv of sunset and sunrise times
user = getpass.getuser()
if user == "pi":
    ss = open(f"/home/{user}/SPC/sunrise_sunset.csv")
else:
    ss = open("/home/aps_desktop/Documents/SERC_Pollinator/Sunrise_sunset/sunrise_sunset.csv")
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



# calculates diferrence of each days sunset - sunrise
# each item in list is a timeDelta object.
deltalist = []
for date in range(len(datelist)):
    if date % 2 == 0:
        deltalist.append(datelist[date + 1] - datelist[date])

#write # of hours/minutes between sunrise and sunset to schedulingHours.txt with format: 
# hours, minutes, sunrise date (isoformat), sunset date (isoformat)
if user == "pi":
    toScheduling = open(f"/home/{user}/SPC/SchedulingHours.txt", "w")
else:
    toScheduling = open(f"/home/{user}/Documents/SERC_Pollinator/Sunrise_sunset/SchedulingHours.txt", "w")

for d in range(len(deltalist)):
    deltaSplit = str(deltalist[d]).split(":")
    print(deltaSplit[0] + "," + deltaSplit[1] + "," + datelist[d*2].isoformat() + "," + datelist[d*2 + 1].isoformat() + "\n")
    toScheduling.write(deltaSplit[0] + "," + deltaSplit[1] + "," + datelist[d*2].isoformat() + "," + datelist[d*2 + 1].isoformat() + "\n")

toScheduling.close()