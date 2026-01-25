#!/usr/bin/env python
import random
from datetime import datetime

import RGBMatrixEmulator
from PIL import Image

#CLOCK
from pytz import timezone
import adafruit_ntp

#Adafruit
import adafruit_connection_manager

#import rgbmatrix
from RGBMatrixEmulator import graphics
from sympy.parsing.sympy_parser import null

import easteregg
from easteregg import EasterEgg
from samplebase import SampleBase

from subprocess import check_output
import subprocess
import csv
import time
#import wifi
import os

##create a cron job that does "ntpd -qq" or any other ntp time sync for EST.


#init
#wifi
wifi_ssid = os.getenv("cxxxx{|::::::::::::::::::::::::/")
wifi_password = os.getenv("thesword")
#radio = wifi.radio
#print(radio.enabled)
#wifi.radio.connect(wifi_ssid, wifi_password)

#pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
#ntp = adafruit_ntp.NTP(pool, tz_offset=0, cache_seconds=3600)
#now = ntp.datetime



stops = {}
with open("stops.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    i=0
    for row in csvreader:
        i+=1
        stops.update({row[0]: row[1]})

class GraphicsTest(SampleBase):
    def __init__(self, packet, servicedata, stations, problemtrains, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)
        self.packet=packet
        self.servicedata=servicedata
        self.stations=stations
        self.problemtrains=problemtrains
        self.station_names = []
        for station in stations:
            print(f"Stations: {stops[station]}  {str(station)[0]}")
            self.station_names.append(stops[station])

    def getcolor(self, trainline):
        white=graphics.Color(255, 255, 255)
        seventh = graphics.Color(255, 0, 0)
        lexington = graphics.Color(0, 146, 66)
        eigth = graphics.Color(0, 57, 163)
        sixth = graphics.Color(255, 99, 32)
        bway=graphics.Color(255,255,0)
        jamaica=graphics.Color(165,42,42)
        nassau=graphics.Color(107,187,78)
        flushing=graphics.Color(185,52,170)
        atlantic=graphics.Color(167,169,172)
        black = graphics.Color(0, 0, 0)
        white = graphics.Color(255, 255, 255)
        blue = graphics.Color(0, 0, 255)

        bulletcolor = white
        if trainline=="4" or trainline=="5" or trainline=="6":
            color=lexington

        elif trainline=="3" or trainline=="2" or trainline=="1":
            color=seventh
        elif trainline=="J" or trainline=="Z":
            color=jamaica
        elif trainline=="A" or trainline=="C" or trainline=="E" or trainline=="H":
            color=eigth
        elif trainline=="F" or trainline=="M" or trainline=="B" or trainline=="D":
            color=sixth
        elif trainline=="N" or trainline=="Q" or trainline=="R" or trainline=="W":
            color=bway
        elif trainline=="G":
            color=nassau
        elif trainline=="L":
            color=atlantic
        elif trainline=="7":
            color=flushing
        else:
            color=white
        return color
    def run(self):
        # new
        #options = RGBMatrixEmulator.RGBMatrixOptions()
        #options.rows = 32
        #options.chain_length = 2
        #options.parallel = 1
        #options.hardware_mapping = 'regular'


        canvas = self.matrix.CreateFrameCanvas()
        #canvas = self.matrix.SwapOnVSync(canvas)





        font = graphics.Font()
        font.LoadFont("fonts/6x10.bdf") ##!! Change to 6x10.bdf,I think. Test this out - bcc
        font_small = graphics.Font()
        font_small.LoadFont("fonts/4x6.bdf")
        font_big = graphics.Font()
        font_big.LoadFont("fonts/7x13B.bdf")
        black= graphics.Color(0, 0, 0)
        white=graphics.Color(255, 255, 255)
        blue=graphics.Color(0, 0, 255)
        red=graphics.Color(255, 0, 0)
        yellow=graphics.Color(255, 175, 0)
        bulletcolor = white
        problemtrains=self.problemtrains
        print(f"problem Trains (current): {problemtrains}")
        traincolors=[]








        #self.matrix.SwapOnVSync(canvas)
        #canvas.Clear()

        statnum = 0
        c=0 #what are you????


        for subpacket in self.packet:
            canvas.Clear()

            #EASTER EGG BLOCK
    #        now = datetime.now()
     #       print(f"____________Now.hour = {now.hour}, now.minute = {now.minute}, now.second = {now.second}")
#
 #           print(f"    -- calling: EasterEgg")
  #          print(f"easter egg! easter egg! easter egg! easter egg!")
   #         roomate_list = ("Spencer", "Tiff", "Paul", "Ergo", "Dolly", "Buddy")
    #        roomate = random.choice(roomate_list)
     #       print(f"I LOVE YOU {roomate}")
      #      t_end1 = time.time() + 4
       #     canvas.Fill(0, 255, 0)

            #hile time.time() < t_end1 and now.hour==20 and 55 <= now.minute <=57:
                # print(f"in here")
                # print(f" time.time() < time.time() + 10  |  {str(time.time())} < {str(time.time()+10)}")
            #    canvas.Clear()
            #    canvas.Fill(0, 255, 0)
            #    graphics.DrawText(canvas, font_big, 9, 6, white, "I LOVE YOU " + roomate)
                #                 str(self.station_names[0]) + " " + str(self.stations[0])[0] + " Train")

                # Why is this not printing anything on the matrix????????????????????

                # graphics.DrawText(canvas, font, 25, 14, white, "I LOVE YOU " + roomate)
                # time.sleep(5)
            #    canvas.Clear()

            print(f"Station Call: [{statnum}] {self.station_names[statnum]} ({str(self.stations[statnum])[0]} train)")
            c+=1



            northhvalues=[[0, 30],[0,30]]
            southhvalues=[[0, 30],[0,30]]
            t_end = time.time() + 4  #last value controls display time per station in seconds
            # ^ do it like: if there are three stations (statins[0,1,2], then make the interval variable much higher, so it only shows station name
            #at the end of each "cycle", instead of at the end of each line list. That way it goes like:
            # 456 times, nqrw times, L times, then "14 st-Union Sq", instead of the station name after each card.
            print(f"time.time(): {str(time.time())} | t_end: {str(t_end)}")



            canvas.Clear()
            line = ""

            while time.time() < t_end:
                canvas.Clear()
                graphics.DrawText(canvas, font_small, 9, 6, white, str(self.station_names[statnum]) + " " + str(self.stations[statnum])[0] + " Train")
                #utc = pytz.timezone('UTC')
                #now = utc.localize(datetime.utcnow())
                #nytz =pytz.timezone('America/New_York')
                #local_time = now.astimezone(nytz)
                now = datetime.now()
                formatted_time = now.strftime("%H:%M")
                graphics.DrawText(canvas, font_small, 107, 6, yellow, formatted_time)

                i = 0
                b = 0

                traincharspacing=7+8 # The Vertical spacing for characters.

                for train in subpacket:
                    line = str(train[0])
                    mins = str(train[1])
                    dest = str(stops[train[2]])

                    if train[2][3] == "N":
                        if b<2:
                            color=self.getcolor(line)
                            traincolors.append(color)
                            bulletcolor = white
                            if line=="N" or line=="R" or line=="Q" or line=="W": bulletcolor = black
                            posi2=17



                            len2=(len(str(dest))*5)
                            if len2>80: #length of free black space between the bullet/arrows and the times.

                                northhvalues[b][0]=10-len2+42
                                posi2=northhvalues[b][1]
                                if northhvalues[b][1]<=northhvalues[b][0]-20:
                                    northhvalues[b][1]=30
                                    posi2=northhvalues[b][1]
                                if posi2<=northhvalues[b][0] and posi2>=northhvalues[b][0]-20:
                                    posi2=northhvalues[b][0]
                                if northhvalues[b][1]>=15:
                                    posi2=15 #= x coords
                            else:
                                posi2=15

                                ## POSSIBLY: add "framerate_fraction=10" to the canvas once its running on metal? Its a utility not finihsed for emulator.


                            graphics.DrawText(canvas, font, posi2, traincharspacing, color, str(stops[train[2]])) # train destination scroll
                            time.sleep(0.02)

                            for i in range(14):graphics.DrawLine(canvas, i, traincharspacing-7, i, traincharspacing, graphics.Color(0, 0, 0)) #creates black bar beneath bullet/line num
                            for i in range(95,128): #black block beneath train arrival times
                                   graphics.DrawLine(canvas, i, traincharspacing-7, i, traincharspacing, graphics.Color(0, 0, 0))

                            #ARROW GRAPHICS (range(8,14)
                            graphics.DrawLine(canvas, 9, 9, 12, 12, graphics.Color(255, 255, 255))
                            canvas.SetPixel(10, 9, 255, 255, 255)
                            canvas.SetPixel(11, 9, 255, 255, 255)
                            #canvas.SetPixel(12, 9, 255, 255, 255)
                            canvas.SetPixel(9, 10, 255, 255, 255)
                            canvas.SetPixel(9, 11, 255, 255, 255)
                            #canvas.SetPixel(9, 12, 255, 255, 255)

                            graphics.DrawLine(canvas, 9, 9+8, 12, 13+7, graphics.Color(255, 255, 255))
                            canvas.SetPixel(10, 9+8, 255, 255, 255)
                            canvas.SetPixel(11, 9+8, 255, 255, 255)
                            #canvas.SetPixel(12, 9+8, 255, 255, 255)
                            canvas.SetPixel(9, 10+8, 255, 255, 255)
                            canvas.SetPixel(9, 11+8, 255, 255, 255)
                            #canvas.SetPixel(9, 12+8, 255, 255, 255)



                            #BULLETS
                            # Manual bullet icon creation
                            graphics.DrawCircle(canvas, 4, traincharspacing - 4, 3, color)  # bullet
                            graphics.DrawCircle(canvas, 4, traincharspacing - 4, 2, color)  # fill
                            graphics.DrawCircle(canvas, 4, traincharspacing - 4, 1, color)  # fill
                            canvas.SetPixel(3, traincharspacing - 5, color.red, color.green, color.blue)  # fill
                            canvas.SetPixel(3, traincharspacing - 3, color.red, color.green, color.blue)  # fill
                            canvas.SetPixel(5, traincharspacing - 5, color.red, color.green, color.blue)  # fill
                            canvas.SetPixel(5, traincharspacing - 3, color.red, color.green, color.blue)  # fill
                            canvas.SetPixel(4, traincharspacing - 4, color.red, color.green, color.blue)  # fill
                            canvas.SetPixel(4, traincharspacing - 4, color.red, color.green, color.blue)  # fill


                            # Draw line letter/number on top of bullet
                            if line in problemtrains:
                                bulletcolor = red #this makes the letter of the bullet RED if the line is facing delays or outages
                                if line=="1" or line=="2" or line=="3":
                                    bulletcolor=yellow #since the 1/2/3 lines are already red, this makes the bullet color yellow, instead of red (outage) or white (normal)
                            graphics.DrawText(canvas, font_small, 3, traincharspacing - 1, bulletcolor, line)  # train line on top of bullet

                            # if mins is single digit, it will add a blank space before the number to align it with two-digit ints.
                            if len(str(mins)) < 2:
                                mins = " " + mins

                            # if the train is 0 minutes away, it will simply say "   Now" instead of " 0 mins"
                            if train[1] < 1:
                                mins = "  Now"

                                # write out the minute counts
                                graphics.DrawText(canvas, font, 98, traincharspacing, white, mins)
                            else:
                                graphics.DrawText(canvas, font, 98, traincharspacing, white, mins)
                                graphics.DrawText(canvas, font_small, 111, traincharspacing, white, "mins")




                            # long cross line to separate Northbound trains and Southbound trains.
                            #graphics.DrawLine(canvas, 9, 16+7, 96, 16+7, white )

                            traincharspacing+=8
                            northhvalues[b][1]-=1
                            b+=1
                            c+=1 #still not sure what "c" does.

                traincharspacing=23+7+1
                b=0
                i+=1
                #Southbound trains on bottom (why can't this be in the above loop? It's practically identical?)
                for train in subpacket:
                    line = str(train[0])
                    dest = str(stops[train[2]])
                    mins = str(train[1])
                    if train[2][3] == "S":
                        if b<1:
                            #fetch bullet/line color
                            color=self.getcolor(line)
                            bulletcolor=white

                            #compressing/running the too-long dest names
                            len2=(len(str(dest))*5) #as 5 is the width if pixels per letter, this line shows how wide the destination is.
                            if len2>80: #length of white line
                                southhvalues[b][0]=10-len2+42
                                posi2=southhvalues[b][1]
                                if southhvalues[b][1]<=southhvalues[b][0]-20:
                                    southhvalues[b][1]=30
                                    posi2=southhvalues[b][1]
                                if posi2<=southhvalues[b][0] and posi2>=southhvalues[b][0]-20:
                                    posi2=southhvalues[b][0]
                                if southhvalues[b][1]>=15:
                                    posi2=15
                            else:
                                posi2=15

                            #train destination
                            graphics.DrawText(canvas, font, posi2, traincharspacing, color, dest)
                            time.sleep(0.02)

                            #black line below bullets
                            for i in range(14):
                                graphics.DrawLine(canvas, i, traincharspacing-7, i, traincharspacing, graphics.Color(0, 0, 0))
                            #black line below mins/arrival times
                            for i in range(95,128):
                                    graphics.DrawLine(canvas, i, traincharspacing-7, i, traincharspacing, graphics.Color(0, 0, 0))

                            #ARROW
                            graphics.DrawLine(canvas, 9, 9 + 8 + 8, 12, 13 + 8 + 7, graphics.Color(255, 255, 255))
                            canvas.SetPixel(10, 9 + 8 + 8+3, 255, 255, 255)
                            canvas.SetPixel(11, 9 + 8 + 8+3, 255, 255, 255)
                            #canvas.SetPixel(12, 9 + 8 + 8+3, 255, 255, 255)
                            canvas.SetPixel(9+3, 10 + 8 + 8, 255, 255, 255)
                            canvas.SetPixel(9+3, 11 + 8 + 8, 255, 255, 255)
                            #canvas.SetPixel(9+3, 12 + 8 + 8, 255, 255, 255)

                            #Manual bullet icon creation
                            graphics.DrawCircle(canvas, 4, traincharspacing - 4, 3, color) #bullet
                            graphics.DrawCircle(canvas, 4, traincharspacing - 4, 2, color) #fill
                            graphics.DrawCircle(canvas, 4, traincharspacing - 4, 1, color) #fill
                            canvas.SetPixel(3, traincharspacing - 5, color.red, color.green, color.blue)  #fill
                            canvas.SetPixel(3, traincharspacing - 3, color.red, color.green, color.blue)  #fill
                            canvas.SetPixel(5, traincharspacing - 5, color.red, color.green, color.blue)  #fill
                            canvas.SetPixel(5, traincharspacing - 3, color.red, color.green, color.blue)  #fill
                            canvas.SetPixel(4, traincharspacing - 4, color.red, color.green, color.blue)  # fill
                            canvas.SetPixel(4, traincharspacing - 4, color.red, color.green, color.blue)  # fill
                            # Draw line number on top of bullet
                            if line in problemtrains:
                                bulletcolor = red
                                if line=="1" or line=="2" or line=="3":
                                    bulletcolor=yellow
                            graphics.DrawText(canvas, font_small, 3, traincharspacing - 1, bulletcolor, str(train[0]))  # train line

                            # if mins is single digit, it will add a blank space before the number to align it with two-digit ints.
                            if len(str(mins)) < 2:
                                mins = " " + mins

                            # if the train is 0 minutes away, it will simply say "   Now" instead of " 0 mins"
                            if train[1] < 1:
                                mins = "  Now"

                                # write out the minute counts
                                graphics.DrawText(canvas, font, 98, traincharspacing, white, mins)
                            else:
                                graphics.DrawText(canvas, font, 98, traincharspacing, white, mins)
                                graphics.DrawText(canvas, font_small, 111, traincharspacing, white, "mins")

                            #increment the counts (traincharspacing means that the next line is always 8 pixels lower than the current
                            traincharspacing+=8
                            southhvalues[b][1]-=1
                            b+=1

                time.sleep(0.01) #this makes the running text easier to read.
                canvas = self.matrix.SwapOnVSync(canvas) #turning this off makes the whole thing black forever? Weird.
                i +=1
            if c<3: #wtf is "c"??
                print("sleeping...")
            elif c==3:
                canvas.Clear()
                graphics.DrawText(canvas, font, 0, 8, white, "Disruptions:")
                charspace=0
                vertspace=17
                trainnum=1
                for problemtrain in self.servicedata:
                    color=self.getcolor(problemtrain)
                    graphics.DrawText(canvas, font, charspace, vertspace, color, problemtrain)
                    charspace +=7
                    trainnum+=1
                    if trainnum >= 10:
                        vertspace+=8
                        trainnum=1
                        charspace=0
                    #Add ip to disruptions screen
                    ipaddr=str(check_output(['hostname', '-I']))[9:]

                    ipaddr2="IP: " + ipaddr[:-3]
                    graphics.DrawText(canvas, font, 0, 32, graphics.Color(10,169,172), ipaddr2)
                canvas = self.matrix.SwapOnVSync(canvas)
           # if 25 <= now.minute <= 31:
               # t_end1 = time.time()+20
                #while time.time() < t_end1:
                    #print("waking....")
                  #  print(f"now.minute: {now.minute}")
                    #canvas.Clear()
                   # canvas.Fill(100,100,100)
                 #   graphics.DrawText(canvas, font_big, 9, 6,blue, "I LOVE YOU!")

                  #  canvas.Clear()






            statnum+=1




    def print_help(self):
        pass

