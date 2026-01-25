#!/usr/bin/env python
import random
import sys

from PIL import Image

from samplebase import SampleBase
import time
from RGBMatrixEmulator import graphics, RGBMatrixOptions, RGBMatrix

# Configuration for the matrix
#options = RGBMatrixOptions()
#options.rows = 32
##options.cols = 128
#options.chain_length = 1
#options.parallel = 1

#canvas = RGBMatrix()#options = options)

class EasterEgg(SampleBase):
    def __init__(self, *args, **kwargs):
        super(EasterEgg, self).__init__(*args, **kwargs)


    def run(self):
        canvas = self.matrix.CreateFrameCanvas()
        #canvas = self.matrix.CreateFrameCanvas()
        print(f"easter egg! easter egg! easter egg! easter egg!")
        font_big = graphics.Font()
        font_big.LoadFont("fonts/7x13B.bdf")
        white = graphics.Color(255, 255, 255)
        canvas.Clear()
        print("canvas cleared?")
        roomate_list = ("Spencer", "tiff", "paul", "ergo", "dolly", "buddy")
        roomate = random.choice(roomate_list)
        t_end = time.time() + 8
        while time.time() < t_end:
            canvas.Fill(0,0,0)
            graphics.DrawText(canvas, font_big, 12, 14, white, "I LOVE YOU " + roomate)
            print("once")
            time.sleep(1)







        # Preprocess the gifs frames into canvases to improve playback performance
        #frames = []
        #gif = Image.open("pixel-heart.gif")
        #num_frames = gif.n_frames
        #print(f"num_frames: {num_frames}")
        #print("Preprocessing gif, this may take a moment depending on the size of the gif...")
        #for frame_index in range(0, num_frames):
        #    gif.seek(frame_index)
        #    # must copy the frame out of the gif, since thumbnail() modifies the image in-place
        #    frame = gif.copy()
        #    frame.thumbnail((32, 32), Image.Resampling.LANCZOS)
        #    frames.append(frame.convert("RGB"))

            # Close the gif file to save memory now that we have copied out all of the frames
#            gif.close()

 #           print("Completed Preprocessing, displaying gif")


            # Infinitely loop through the gif
  #          cur_frame = 0
            #while (True):
            #    canvas.SetImage(frames[cur_frame])
            #    self.matrix.SwapOnVSync(canvas)  # , framerate_fraction=10)
            #    if cur_frame == num_frames - 1:
            #       cur_frame = 0
            #    else:
            #        cur_frame += 1
            #   time.sleep(0.2)

