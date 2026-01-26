#!/usr/bin/env python
import random
import sys
from random import randint

from PIL import Image

#from mtaapicall import eastereggfunc
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

def gifrunner(matrix, gif_file, t_end, position):
    # GIF Processing:
    # GIF of HEARTS
    # Preprocess the gifs frames into canvases to improve playback performance
    x= []
    if position == "":
        x=[0]
    if position == "rightalign":
        x = [104]
    if position == "leftalign":
        x = [-4]
    if position == "both":
        x = [-4, 102]
    frames = []
    if gif_file == "gifs/grace.gif":
        xg = matrix.width - 96
        yg = matrix.height #(matrix.width, matrix.height)
    else:
        xg = matrix.width
    gif = Image.open(gif_file)
    num_frames = gif.n_frames
    print(f"num_frames: {num_frames}")
    print("Preprocessing gif, this may take a moment depending on the size of the gif...")
    for frame_index in range(0, num_frames):
        gif.seek(frame_index)
        # must copy the frame out of the gif, since thumbnail() modifies the image in-place
        frame = gif.copy()
        frame.thumbnail((matrix.width, matrix.height), Image.Resampling.LANCZOS)
        frames.append(frame.convert("RGB"))
        # Close the gif file to save memory now that we have copied out all of the frames
    gif.close()
    # Infinitely loop through the gif
    cur_frame = 0
    while time.time() < t_end:

        if len(x) == 1:

            if gif_file == "gifs/grace.gif":
                matrix.SetImage(frames[cur_frame], 0, 0)
            else:
                matrix.SetImage(frames[cur_frame], 96, 0)
            time.sleep(0.15)#make the 98 a variable
        if len(x) == 2:
            for pos in x:
                matrix.SetImage(frames[cur_frame], pos, 0)
        # self.matrix.SwapOnVSync(self.matrix)  # , framerate_fraction=10)
        if cur_frame == num_frames - 1:
            cur_frame = 0
        else:
            cur_frame += 1
        # Print progress percentage on the same line
        print(f"\rcur_frame: {cur_frame}", end="", flush=True)
    if gif_file == "gifs/skull2.gif":
        matrix.SetImage(frames[0], 96, 0)
    time.sleep(0.15)

        #matrix.Clear()

class EasterEgg(SampleBase):
    def __init__(self, *args, **kwargs):
        super(EasterEgg, self).__init__(*args, **kwargs)


    def run(self):
        #t_end = time.time() +8
        #while time.time() < t_end :
        #    im = Image.open("pixel-heart.gif").convert("RGB")
        #    if im.size[0] > im.size[1]:
        #        size = (self.matrix.width + self.matrix.width), self.matrix.width
        #        im.thumbnail(size)
        #    else:
        #        size = self.matrix.height, (self.matrix.height + self.matrix.height)
        #        im.thumbnail(size)
         #   width, height = im.size
          #  left = (width - self.matrix.width) / 2
           # top = (height - self.matrix.height) / 2
         #   right = (width + self.matrix.width) / 2
          #  bottom = (height + self.matrix.height) / 2
           # image = im.crop((left, top, right, bottom))

         #   image.thumbnail((self.matrix.width, self.matrix.height), Image.LANCZOS)
          #  self.matrix.SetImage(image)


        #canvas = self.matrix.CreateFrameCanvas()
        #canvas = self.matrix.CreateFrameCanvas()
        print(f"easter egg! easter egg! easter egg! easter egg!")
        font = graphics.Font()
        font.LoadFont("fonts/5x8.bdf")
        font_small = graphics.Font()
        font_small.LoadFont("fonts/4x6.bdf")
        font_big = graphics.Font()
        font_big.LoadFont("fonts/7x13B.bdf")
        font_scientificaitalic = graphics.Font()
        font_scientificaitalic.LoadFont("fonts/scientificaItalic-11.bdf")
        white = graphics.Color(255, 255, 255)
        red = graphics.Color(255, 75, 75)
        #self.matrix.Clear()

        t_end = time.time() + 8
        while time.time() < t_end:
            #message selection
            surprise = random.randint(0, 5)
            if surprise == 0: #hearts
                #I LOVE YOU RM message

                roomate_list = ("Spencer", "tiff", "paul", "ergo", "dolly", "buddy")
                roomate = random.choice(roomate_list)


                graphics.DrawText(self.matrix, font_big, 29, 14, white, "I LOVE YOU ")
                graphics.DrawText(self.matrix, font_big, 44, 25, white, roomate.upper()+"!")
                gifrunner(self.matrix, "gifs/pixel-heart.gif", t_end, "both")
                break

            if surprise == 1: #memento mori
                align="rightalign"
                image = Image.open("gifs/gravestone.png")
                image.thumbnail((32, 32), Image.Resampling.LANCZOS)
                self.matrix.SetImage(image.convert('RGB'), -4, 0)
                gifrunner(self.matrix, "gifs/skull2.gif", t_end-3, align)
                graphics.DrawText(self.matrix, font_scientificaitalic, 30, 8, white, "~ Memento Mori ~")
                graphics.DrawText(self.matrix, font_scientificaitalic, 30, 18, red, "Remember that")
                graphics.DrawText(self.matrix, font_scientificaitalic, 30, 28, red, "you will die!")
                break

            if surprise == 2: #the fly toward grace
                t_end += 25
                align=""
                gifrunner(self.matrix, "gifs/grace.gif", t_end - 3, align)
                        #graphics.DrawText(self.matrix, font_big, 32, 20, white, message)
                break
                break

            if surprise == 3: #funny message
                r = randint(10, 255)
                g = randint(10, 255)
                b = randint(10, 255)
                messagebank = ["Brandon is Hot", "GO PISS GIRL", "GO BRIY GO", "I LOVE MY PALS", "LONG LIVE POOBA", "NOOP STRONG!!", "SMOKE BREAK!"]
                message = random.choice(messagebank)
                graphics.DrawText(self.matrix, font_big, 6, 14, graphics.Color(r, g, b), message)
                break

            if surprise == 4: #ben was here
                r = randint(10,255)
                g = randint(10,255)
                b = randint(10,255)
                message = "BEN WAS HERE"
                graphics.DrawText(self.matrix, font_big, 29, 14, graphics.Color(r, g, b), "BEN WAS HERE!")
                break

            if surprise == 5:
                message = "SUBSCRIBE to LonelyManLazarus"
                graphics.DrawText(self.matrix, font, 10, 14, white, "SUBSCRIBE to")
                graphics.DrawText(self.matrix, font, 10, 26, white, "@LonelyManLazarus")
                image = Image.open("gifs/LMLgrimm.png")
                image.thumbnail((32, 32), Image.Resampling.LANCZOS)
                self.matrix.SetImage(image.convert('RGB'), 98, 0)
                break



#if __name__ == "__main__":
#    easteregg = EasterEgg()
#    if (not EasterEgg().process()):
#        easteregg.print_help()
