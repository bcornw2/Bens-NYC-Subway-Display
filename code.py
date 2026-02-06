import datetime
import microcontroller


from google.transit import gtfs_realtime_pb2
import requests
import time  # imports module for Epoch/GMT time conversion
from os import getenv
from protobuf_to_dict import protobuf_to_dict
import subprocess
import csv


import rundisplay
from easteregg import EasterEgg
from rundisplay import GraphicsTest
from digitalio import DigitalInOut
import board


from RGBMatrixEmulator import graphics
from rundisplay import GraphicsTest
import easteregg



def getdata():
    realtime_data1 = []
    # old_links=["https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace","https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm", "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"]
    feedurls = [
        "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace",  # ACE Sr
        "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm",  # BDFM Sf
        "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g",  # G
        "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz",  # JZ
        "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw",  # NQRW
        "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l",  # L
        "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"  # , #123 456 7 S
        # "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-si" #SIR
    ]

    for link in feedurls:
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(link)
        feed.ParseFromString(response.content)
        subway_feed = protobuf_to_dict(feed)  # subway_feed is a dictionary
        realtime_data = subway_feed['entity']  # train_data is a list
        for element in realtime_data:
            realtime_data1.append(element)
    return realtime_data1


def gettimes(data, station):
    arrivaldata = []
    trainletters = []
    ctimes = station_time_lookup(data, station)
    ctimes.sort(key=lambda row: (row[1], row[0]), reverse=False)
    return ctimes[:6]  # why is this trunc'd to only six?


def station_time_lookup(train_data, station):
    ctimes = []
    for trains in train_data:  # trains are dictionaries
        if trains.get('trip_update', False) != False:
            unique_train_schedule = trains['trip_update']  # train_schedule is a dictionary with trip
            try:
                unique_arrival_times = unique_train_schedule['stop_time_update']  # arrival_times is a list of arrivals
                for scheduled_arrivals in unique_arrival_times:  # arrivals are dictionaries with time data and stop_ids
                    if scheduled_arrivals.get('stop_id', False) == station:
                        s1 = unique_train_schedule
                        trainletter = s1['trip']['route_id']

                        test5 = unique_arrival_times[-1]
                        stop = test5['stop_id']

                        time_data = scheduled_arrivals['arrival']
                        unique_time = time_data['time']

                        if unique_time != None:
                            mintoarrival = int(((unique_time - int(time.time())) / 60))
                            # if mintoarrival > 2: #only displays trains 3 or more mins away
                            ctimes.append([trainletter, mintoarrival, stop])
            except:
                pass
    return ctimes


def totalstationtimes(stationlist):
    finaldata = []
    data = []
    try:
        print("   Fetching data...")
        data = getdata()
    except:
        print("datafail")
        time.sleep(30)
        # subprocess.Popen('sudo reboot -n', shell=True)
    print("datagot")
    for station in stationlist:
        stations = [(station + "N"), (station + "S")]
        newdata = []
        d = 0
        for station1 in stations:
            arrd = gettimes(data, station1)
            d += 1
            for element in arrd:
                newdata.append(element)
        newdata.sort(key=lambda row: (row[1], row[0]), reverse=False)
        finaldata.append(newdata)
    return finaldata


def getservicedata():
    realtime_data1 = []
    links = ["https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts"]
    for link in links:
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(link)
        feed.ParseFromString(response.content)
        subway_feed = protobuf_to_dict(feed)  # subway_feed is a dictionary
        realtime_data = subway_feed['entity']  # train_data is a list
        for element in realtime_data:
            realtime_data1.append(element)
    return realtime_data1


def procservicedata():
    problemtrains = []
    mainlist = getservicedata()[:10]
    mainlist2 = []
    for element in mainlist:
        if element["id"][4] == "a":  # seperates active alerts from planned service changes
            mainlist2.append(element["alert"]["informed_entity"])

    for element4 in mainlist2:
        for element5 in element4:
            try:
                if element5["route_id"] not in problemtrains:
                    if "S" not in element5["route_id"]:
                        problemtrains.append(element5["route_id"])
            except:
                pass
    if len(problemtrains) == 0:
        problemtrains = ["None"]
    problemtrains.sort()
    print(f"Problem trains: {problemtrains}")
    return problemtrains


def terminalformatter(packet, servicedata, stations):
    # get human-readable stops
    # color formatter

    stops = {}
    c = 0
    with open("stops.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            stops.update({row[0]: row[1]})
    bulletcolor = "white"
    for subpacket in packet:
        c += 1
        t_end = time.time() + 1 * 100
        b = 0
        for train in subpacket:
            bulletcolor = "white"
            if train[0] == "N" or train[0] == "R" or train[0] == "Q" or train[0] == "W": bulletcolor = "yellow"
            if train[0] == "4" or train[0] == "5" or train[0] == "6": bulletcolor = "green"
            if train[0] == "L": bulletcolor = "light_grey"
            if train[0] == "7": bulletcolor = "magenta"
            if train[0] == "1" or train[0] == "2" or train[0] == "3": bulletcolor = "red"
            if train[0] == "A" or train[0] == "C" or train[0] == "E": bulletcolor = "blue"
            if train[0] == "B" or train[0] == "D" or train[0] == "F" or train[0] == "M": bulletcolor = "light_red"
            if train[0] == "J" or train[0] == "Z": bulletcolor = "dark_grey"

            if train[2][3] == "N" or train[2][3] == "S":
                # if train[0] == "L":  b = 2 #somehow restrict output to only include sooner trips. L doesnt need that many because only 2 services (nobo & sobo), but 4/5/6 does need more
                if b < 6:
                    textstring = str(train[0])

                    line = colored(str(train[0]), bulletcolor, attrs=["bold"])
                    if train[1] <= 1:
                        mins = colored("...Now", "white", attrs=["bold"])
                    else:
                        mins = str(train[1]) + " mins"

                    dest = str(stops[train[2]])
                    width = 32

                    print(f"({line})  | {dest:<25}    {mins:>15}")
                    b += 1


def rgbformatter(packet, servicedata, stations):
    # get human-readable stops
    # color formatter

    stops = {}
    c = 0
    with open("stops.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            stops.update({row[0]: row[1]})
        # print("stops.: " + str(stops))
    print(f"Station:  {stops[stations[0]]}")
    bulletcolor = "white"
    for subpacket in packet:

        # print(f"packet: {packet}")
        print(f"subpacket: {subpacket}")
        c += 1
        t_end = time.time() + 1 * 100
        # while time.time() < t_end:
        b = 0
        for train in subpacket:
            # print(f"train[0]:   {train[0]} ... train[1]: {train[1]} ... train[2]: {train[2]} ... ")
            # print(f"train[0][1]:   {train[0][1]} ... train[0][2]: {train[0][2]} ") #... train[2]: {train[2]} ... ")
            bulletcolor = "white"
            if train[0] == "N" or train[0] == "R" or train[0] == "Q" or train[0] == "W": bulletcolor = "yellow"
            if train[0] == "4" or train[0] == "5" or train[0] == "6": bulletcolor = "green"
            if train[0] == "L": bulletcolor = "light_grey"
            if train[0] == "7": bulletcolor = "magenta"
            if train[0] == "1" or train[0] == "2" or train[0] == "3": bulletcolor = "red"
            if train[0] == "A" or train[0] == "C" or train[0] == "E": bulletcolor = "blue"
            if train[0] == "B" or train[0] == "D" or train[0] == "F" or train[0] == "M": bulletcolor = "light_red"
            if train[0] == "J" or train[0] == "Z": bulletcolor = "dark_grey"

            if train[2][3] == "N" or train[2][3] == "S":
                # if train[0] == "L":  b = 2 #somehow restrict output to only include sooner trips. L doesnt need that many because only 2 services (nobo & sobo), but 4/5/6 does need more
                if b < 6:
                    textstring = str(train[0])

                    line = colored(str(train[0]), bulletcolor, attrs=["bold"])
                    if train[1] <= 1:
                        mins = colored("...Now", "white", attrs=["bold"])
                    else:
                        mins = str(train[1]) + " mins"

                    dest = str(stops[train[2]])
                    width = 32

                    print(f"({line})  | {dest:<25}    {mins:>15}")
                    b += 1


## TEMPORARY::
while True:
    if __name__ == "__main__":
        now = datetime.datetime.now()
        print(f"now: {now.hour}:{now.minute}:{now.second}")
        stations = ["M12", "G31", "L13"] #["A32", "D20"] #W 4th St
                                # #for some reason, L12 and L13 don't work? No packet data?
                            #"R16", "127", "725", "901"] TIMES SQUARE
                        # #"M12", "G31", "L13"] SPENCER AND TIFFS HOUSE
                         #"718", "R09"] #QUEENSBORO PLAZA
        #                  #["635","R20","L03"] Union Square
        #                   #"these can be changed, use stops.csv in this dir to find your local.
        worked = 0
        while worked == 0:


            try:
                packet = totalstationtimes(stations)  # (14 st-Union Square N/S, -- "423", "A41", "232"]) <-- boroguh hall, Jay St Metrotech, borough hall again?
                servicedata = procservicedata()
                worked = 1
            except:
                print("CATASTROPHIC FAILURE")
            for timegroup in packet:
                for singletime in timegroup:
                    if singletime[1] < 2:
                        timegroup.remove(singletime)







            graphics_test = GraphicsTest(packet, servicedata, stations, procservicedata())
            print(f"Just finished.")
            if not graphics_test.process():
                print("is running")
                graphics_test.print_help()

            #easter egg schedule

            if now.hour == 00 and (1 <= now.minute <= 3 or 55 <now.minute <= 57):
                print(f"now.hour: {now.hour}, now.minute: {now.minute}")
                easter_egg = EasterEgg()
                if (not EasterEgg().process()):
                    easteregg.print_help()

    for timegroup in packet:
        for singletime in timegroup:
            if singletime[1] < 2:
                timegroup.remove(singletime)