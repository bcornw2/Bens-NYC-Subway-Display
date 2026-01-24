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

from samplebase import SampleBase

from subprocess import check_output
import subprocess
import csv
import time
#import wifi
import os

##create a cron job that does "ntpd -qq" or any other ntp time sync for EST.



#easter egg # REMOVE BEFORE APPLYING TO OTHER PROJECTS
class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):

                    canvas.Clear()
                    roomate_list = ("spencer", "tiff", "paul", "ergo", "dolly", "buddy")
                    roomate = random.choice(roomate_list)
                    graphics.DrawText(canvas, font_big, 25, 14, white, "I LOVE YOU " + roomate)
                    canvas.Clear()

                    # Preprocess the gifs frames into canvases to improve playback performance
                    frames = []
                    gif = Image.open("pixel-heart.gif")
                    num_frames = gif.n_frames
                    #print("Preprocessing gif, this may take a moment depending on the size of the gif...")
                    for frame_index in range(0, num_frames):
                        gif.seek(frame_index)
                        # must copy the frame out of the gif, since thumbnail() modifies the image in-place
                        frame = gif.copy()
                        frame.thumbnail((32, 32), Image.Resampling.LANCZOS)
                        frames.append(frame.convert("RGB"))

                    # Close the gif file to save memory now that we have copied out all of the frames
                    gif.close()

                    #print("Completed Preprocessing, displaying gif")


                    # Infinitely loop through the gif
                    cur_frame = 0
                    #while (True):
                    #    canvas.SetImage(frames[cur_frame])
                    #    self.matrix.SwapOnVSync(canvas)  # , framerate_fraction=10)
                    #    if cur_frame == num_frames - 1:
                     #       cur_frame = 0
                    #    else:
                    #        cur_frame += 1
                     #   time.sleep(0.2)

