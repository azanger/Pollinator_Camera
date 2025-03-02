# 0 = day of month, 1 = Jan(Rise), 2 = Jan(Set), 3 = Feb(Rise), ...

import getpass
import datetime

year = int(datetime.datetime.now().year)

user = getpass.getuser()

sunrise_sunset_table = open(f"/home/{user}/Documents/SERC_Pollinator/sunrise-sunset_Table{year}.txt", "r")

sst_lines = sunrise_sunset_table.readlines()

dirty_sst_list = []
for line in sst_lines:
    strip = line.strip("\n")
    split = strip.split(" ")
    dirty_sst_list.append(split)

sst_list = []
# for i in range(len(dirty_sst_list)):
#     for j in range(len(dirty_sst_list[i])):
#         if dirty_sst_list[i][j] != " ":
#             sst_list.append(dirty_sst_list[i][j])
#         if dirty_sst_list[i][j] == " ":
ignore = 0
for line in dirty_sst_list:
    sst_sub_list = []
    if len(line) == 37:
        for i in range(1, len(line)):
            if i % 3 != 1:
                sst_sub_list.append(line[i])
        sst_list.append(sst_sub_list)
    else:
        for i in range(1, len(line)):
            #print(i, len(line[i]))
            if line[i] == "":
                if ignore == 0:
                    if line[i+1] == "":
                        ignore = 1
                        sst_sub_list.append("")
                        sst_sub_list.append("")
                    else:
                        ignore = 0
            if line[i] != "":
                ignore = 0
                sst_sub_list.append(line[i])
        sst_list.append(sst_sub_list)
sunrise_sunset_table.close()    

sunrise_sunset = open("/home/aps_desktop/Documents/SERC_Pollinator/sunrise_sunset.csv", "w")
for i in range(len(sst_list)):
    sunrise_sunset.write(",".join(sst_list[i]))
    sunrise_sunset.write('\n')
sunrise_sunset.close()

