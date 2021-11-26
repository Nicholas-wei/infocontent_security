import os
import time
import json
import re

data_path = "D:\\data_analysis\Time\\11.24.json"
Hotd_path = "D:\\data_analysis\Time\\Hot_analysis.txt"

def cut_all_data(data_path):
    times = []
    f = open(data_path,'r')
    data = json.load(f)
    for d in data:
        times.append(d['update_time'])
    return times

def cal_the_hot(times):
    num = 0
    f = open(Hotd_path,'w',encoding='UTF-8')
    dates = []
    times.sort()
    for t in times[1:-1]:
        num += 1
        date = time.ctime(float(t))
        f.write((str(num) + '\t' + date + '\n'))
        date = re.split(r' +',date)
        dates.append(date)
    return dates


def cal_week(times):
    dict = {}
    f = open(Hotd_path,'r',encoding='UTF-8')
    dates = []
    times.sort()
    for t in times[1:-1]:
        date = time.ctime(float(t))
        date = re.split(r' +',date)
        dates.append(date)
    i = 0
    j = 1
    while(i < len(dates)):
        temp = 1
        while(j < len(dates)):
            if dates[i][0] == dates[j][0]:
                temp += 1
                i += 1
                j += 1
            else:
                break
        if dict.__contains__(dates[i][0]):
            dict[dates[i][0]] += temp
        else:
            dict[dates[i][0]] = temp
        i += 1
        j += 1
    print(dict)

def cal_month(times):
    dict = {}
    f = open(Hotd_path,'r',encoding='UTF-8')
    dates = []
    times.sort()
    for t in times[1:-1]:
        date = time.ctime(float(t))
        date = re.split(r' +',date)
        dates.append(date)
    i = 1
    j = 2
    while(i < len(dates)):
        temp = 0
        while(j < len(dates)):
            if dates[i][1] == dates[j][1]:
                temp += 1
                i += 1
                j += 1
            else:
                break
        dict[dates[i][1]] = temp
        i += 1
        j += 1
    print(dict)

def cal_day(times):
    dict = {}
    f = open(Hotd_path,'r',encoding='UTF-8')
    dates = []
    times.sort()
    for t in times[1:-1]:
        date = time.ctime(float(t))
        date = re.split(r' +',date)
        dates.append(date)
    i = 1
    j = 2
    while(i < len(dates)):
        temp = 0
        while(j < len(dates)):
            if dates[i][0] == dates[j][0] and dates[i][1] == dates[j][1] :
                temp += 1
                i += 1
                j += 1
            else:
                break
        day = dates[i][0] + " " + dates[i][1]
        dict[day] = temp
        i += 1
        j += 1
    print(dict)

cal_the_hot(cut_all_data(data_path))
cal_week(cut_all_data(data_path))
cal_month(cut_all_data(data_path))
cal_day(cut_all_data(data_path))
