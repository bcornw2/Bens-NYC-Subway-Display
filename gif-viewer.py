#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
#from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from PIL import Image
#image_file = "~/Downloads/odai8.gif"
#im = sys.stdin.readline()

#if len(sys.argv) < 2:
#    sys.exit("Require a gif argument")
#else:
image_file =  "gifs/grace.gif"  #sys.argv[1]

gif = Image.open(image_file)

try:
    num_frames = gif.n_frames
except Exception:
    sys.exit("provided image is not a gif")


# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 2
options.parallel = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

# Preprocess the gifs frames into canvases to improve playback performance
frames = []
canvas = matrix.CreateFrameCanvas()
print("Preprocessing gif, this may take a moment depending on the size of the gif...")
print(str(num_frames))
for frame_index in range(0, num_frames):
    gif.seek(frame_index)
    # must copy the frame out of the gif, since thumbnail() modifies the image in-place
    frame = gif.copy()
    frame.thumbnail((matrix.width, matrix.height), Image.Resampling.LANCZOS)
    frames.append(frame.convert("RGB"))


# Close the gif file to save memory now that we have copied out all of the frames
gif.close()

print("Completed Preprocessing, displaying gif")

try:
    #print("Press CTRL-C to stop.")

    # Infinitely loop through the gif
    cur_frame = 0
    while True:
#        canvas.SetImage(frames[3])
        # Print progress percentage on the same line
        print(f"\rcur_frame: {cur_frame}", end="", flush=True)
        time.sleep(0.01)
        canvas.SetImage(frames[cur_frame])
        matrix.SwapOnVSync(canvas)#, framerate_fraction=10)
        if cur_frame == num_frames - 1:
            cur_frame = 0
        else:
            cur_frame += 1
        time.sleep(0.01)
except KeyboardInterrupt:
    sys.exit(0)
