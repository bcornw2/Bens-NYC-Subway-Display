#!/usr/bin/env python
import RGBMatrixEmulator

#import rgbmatrix
from RGBMatrixEmulator import graphics
from samplebase import SampleBase
from subprocess import check_output
import subprocess
import csv
import time
import os
stops = {}
with open("stops.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        stops.update({row[0]: row[1]})

class GraphicsTest(SampleBase):
    def __init__(self, packet, servicedata, stations, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)
        self.packet=packet
        self.servicedata=servicedata
        self.stations=stations
        print(f"station: {stations}")
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
        atlantic=graphics.Color(165,155,155)
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
            bulletcolor = black
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




        font = graphics.Font()
        font.LoadFont("fonts/6x10.bdf") ##!! Change to 6x10.bdf,I think. Test this out - bcc
        font_small = graphics.Font()
        font_small.LoadFont("fonts/4x6.bdf")
        black= graphics.Color(0, 0, 0)
        white=graphics.Color(255, 255, 255)
        blue=graphics.Color(0, 0, 255)
        bulletcolor = white

        canvas.Clear()
        #initialize w station name
        graphics.DrawText(canvas, font, 1, 1, white, stops[self.stations[0]])
        time.sleep(2)
        canvas.Clear()
        d=0
        c=0 #what are you????
        for subpacket in self.packet:
            c+=1
            print(f"c count: {str(c)}")
            print(f"subpacket[c]:  {str(subpacket)}")
            print(f"Station:  {stops[self.stations[0]]}")

            #canvas.fillCircle(16, 16, 6, canvas.Color(0,0, 255))

            pos = 14
            posi2=14
            northhvalues=[[0, 30],[0,30]]
            southhvalues=[[0, 30],[0,30]]
            t_end = time.time() + 30  #last values controls display time per station in seconds
            #print(f"t_end: {str(t_end)}")
            #print(f"time.time(): {str(time.time())} ")
            while time.time() < t_end:
                canvas.Clear()
                traincharspacing=7
                b=0
                for train in subpacket:
                    line = str(train[0])
                    dest = str(stops[train[2]])
                    mins = str(train[1])
                    if train[2][3] == "N":
                        if b<2:
                            color=self.getcolor(line)
                            bulletcolor = white
                            if line=="N" or line=="R" or line=="Q" or line=="W": bulletcolor = black

                            len2=(len(str(dest))*5)
                            if len2>70:

                                northhvalues[b][0]=10-len2+42
                                posi2=northhvalues[b][1]
                                if northhvalues[b][1]<=northhvalues[b][0]-20:
                                    northhvalues[b][1]=30
                                    posi2=northhvalues[b][1]
                                if posi2<=northhvalues[b][0] and posi2>=northhvalues[b][0]-20:
                                    posi2=northhvalues[b][0]
                                if northhvalues[b][1]>=10:
                                    posi2=10
                            else:
                                posi2=10

                            #time.sleep(0.5)
                            graphics.DrawText(canvas, font, posi2, traincharspacing, color, str(stops[train[2]])) # train destination
                            time.sleep(0.05)


                            for i in range(9):graphics.DrawLine(canvas, i, traincharspacing-7, i, traincharspacing, graphics.Color(0, 0, 0)) #creates black bar beneath bullet/line num
                            for i in range(90,128): #black block beneath train arrival times
                                   graphics.DrawLine(canvas, i, traincharspacing-7, i, traincharspacing, graphics.Color(0, 0, 0))

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
                            # Draw line number on top of bullet
                            graphics.DrawText(canvas, font_small, 3, traincharspacing - 1, bulletcolor, line)  # train line on top of bullet

                            # if mins is single digit, it will add a blank space before the number to align it with two-digit ints.
                            if len(str(mins)) < 2:
                                mins = " " + mins + " mins"
                            else:
                                mins = mins + " mins"

                            # if the train is 0 minutes away, it will simply say "   Now" instead of " 0 mins"
                            if train[1] < 1: mins = "   Now"

                            # write out the minute counts
                            graphics.DrawText(canvas, font, 92, traincharspacing, color, mins)


                            # long cross line to separate Northbound trains and Southbound trains.
                            graphics.DrawLine(canvas, 0, 16, 128, 16, white )

                            traincharspacing+=8
                            northhvalues[b][1]-=1
                            b+=1
                            c+=1 #still not sure what "c" does.

                traincharspacing=23
                b=0
                #Southbound trains on bottom (why can't this be in the above loop? It's practically identical?)
                for train in subpacket:
                    line = str(train[0])
                    dest = str(stops[train[2]])
                    mins = str(train[1])
                    if train[2][3] == "S":
                        if b<2:
                            #fetch bullet/line color
                            color=self.getcolor(line)

                            #compressing/running the too-long dest names
                            len2=(len(str(dest))*5) #as 5 is the width if pixels per letter, this line shows how wide the destination is.
                            if len2>70:
                                southhvalues[b][0]=10-len2+42
                                posi2=southhvalues[b][1]
                                if southhvalues[b][1]<=southhvalues[b][0]-20:
                                    southhvalues[b][1]=30
                                    posi2=southhvalues[b][1]
                                if posi2<=southhvalues[b][0] and posi2>=southhvalues[b][0]-20:
                                    posi2=southhvalues[b][0]
                                    #print(f"posi2: {str(posi2)}")
                                if southhvalues[b][1]>=10:
                                    posi2=10
                            else:
                                posi2=10

                            #train destination
                            graphics.DrawText(canvas, font, posi2, traincharspacing, color, dest)

                            #black line below bullets
                            for i in range(9):
                                graphics.DrawLine(canvas, i, traincharspacing-7, i, traincharspacing, graphics.Color(0, 0, 0))
                            #black line below mins/arrival times
                            for i in range(90,128):
                                    graphics.DrawLine(canvas, i, traincharspacing-7, i, traincharspacing, graphics.Color(0, 0, 0))

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
                            graphics.DrawText(canvas, font_small, 3, traincharspacing - 1, bulletcolor, str(train[0]))  # train line

                            #if mins is single digit, it will add a blank space before the number to align it with two-digit ints.
                            if len(str(mins)) < 2: mins = " " + mins + " mins"
                            else: mins = mins +" mins"

                            #if the train is 0 minutes away, it will simply say "   Now" instead of " 0 mins"
                            if train[1] < 1: mins = "   Now"

                            #write out the minute counts
                            graphics.DrawText(canvas, font, 92, traincharspacing, color, mins)

                            #increment the counts (traincharspacing means that the next line is always 8 pixels lower than the current
                            traincharspacing+=8
                            southhvalues[b][1]-=1
                            b+=1

                time.sleep(0.05) #this makes the runnign text easier to read.
                canvas = self.matrix.SwapOnVSync(canvas)

            if c<3: #wtf is "c"??
                print("sleeping...")

                #THIS IS train disruption functionality that I don't care about.
#            elif c==3:
#                canvas.Clear()
#                graphics.DrawText(canvas, font, 0, 8, white, "Disruptions:")
#                print("servicedata showing")
#                charspace=0
#                vertspace=17
#                trainnum=1
#                for problemtrain in self.servicedata:
#                    color=self.getcolor(problemtrain)
#                    graphics.DrawText(canvas, font, charspace, vertspace, color, problemtrain)
#                    charspace +=7
#                    trainnum+=1
#                    if trainnum >= 10:
#                        vertspace+=8
#                        trainnum=1
#                        charspace=0
#                    #Add ip to disruptions screen
#                    ipaddr=str(check_output(['hostname', '-I']))[9:]
#
#                    ipaddr2="IP: " + ipaddr[:-3]
#                    graphics.DrawText(canvas, font, 0, 32, graphics.Color(10,169,172), ipaddr2)
 #               canvas = self.matrix.SwapOnVSync(canvas)
            else:
                print("fetching data")
