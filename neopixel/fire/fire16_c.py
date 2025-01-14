# SPDX-FileCopyrightText: 2024 Pagong
# SPDX-License-Identifier: MIT

import time
import board
import neopixel
import array
import random
import adafruit_pixel_framebuf

# for WS ESP32-S3-Zero with 16x16 NeoPixel-Matrix
NUM_COLS = 16
NUM_CELLS = 16

NUM_PIXELS = (NUM_COLS * NUM_CELLS)  # Update this to match the number of LEDs.
SPEED = 0.01       # Increase to slow down the fire. Decrease to speed it up.
BRIGHTNESS = 0.1   # A number between 0.0 and 1.0, where 0.0 is off, and 1.0 is max.
PIN = board.IO1    # This is the default pin on WS ESP32-S3-Zero with 16x16 NeoPixel matrix

pixels = neopixel.NeoPixel(PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=False)

HEAT = bytearray(NUM_PIXELS)

# create the PFB (using the pixel buffer)
pfb = adafruit_pixel_framebuf.PixelFramebuffer(
    pixels, NUM_COLS, NUM_CELLS, # reverse_y=True, rotation=2
)

####################### color mapping ###################

ACT_PALETTE = 0        # 0 = Heat, 1 = Rainbow, 2 = Water, 3 = Forest

HeatColors_palette = [
    0x000000,
    0x330000, 0x660000, 0x990000, 0xCC0000, 0xFF0000,
    0xFF3300, 0xFF6600, 0xFF9900, 0xFFCC00, 0xFFFF00,
    0xFFFF33, 0xFFFF66, 0xFFFF99, 0xFFFFCC, 0xFFFFFF
]

RainbowColors_palette = [
    0xFF0000, 0xD52A00, 0xAB5500, 0xAB7F00,
    0xABAB00, 0x56D500, 0x00FF00, 0x00D52A,
    0x00AB55, 0x0056AA, 0x0000FF, 0x2A00D5,
    0x5500AB, 0x7F0081, 0xAB0055, 0xD5002B
]

WaterColors_palette = [
    0x000000,
    0x000033, 0x000066, 0x000099, 0x0000CC, 0x0000FF,
    0x0033FF, 0x0066FF, 0x0099FF, 0x00CCFF, 0x00FFFF,
    0x33FFFF, 0x66FFFF, 0x99FFFF, 0xCCFFFF, 0xFFFFFF
]

ForestColors_palette = [
    0x000000,
    0x003300, 0x006600, 0x009900, 0x00CC00, 0x00FF00,
    0x33FF00, 0x66FF00, 0x66FF33, 0x66FF66, 0x99FF66,
    0x99FF99, 0xCCFF99, 0xCCFFCC, 0xCCFFFF, 0xFFFFFF
]

ALL_palettes = [
    HeatColors_palette,
    RainbowColors_palette,
    WaterColors_palette,
    ForestColors_palette
]

#####################

def interpolate(val1, val2, num, denom):
    value = val1 + ((val2-val1) * num) // denom
    return value

# map heat [0 .. 255] to color palette [0 .. length]
# and interpolate intermediate values
def map_heat_to_color(palette, heat):
    length = len(palette)
    if (length < 2):
        exit
    else:
        last = length-1

    k = (heat * last)
    i = k // 255
    j = k % 255

    color1 = palette[i]
    if (j == 0):
        color3 = color1
    else:
        color2 = palette[i+1]
        color3 = interpolate(color1, color2, j, 255)
    return color3

PALETTE = array.array("L", [0] * 256)
def create_lookup_table(palette):
    for heat in range(255):
        PALETTE[heat] = map_heat_to_color(palette, heat)

##################### fire simulation #######################

# Fire2012 by Mark Kriegsman, July 2012
# as part of "Five Elements" shown here: http://youtu.be/knWiGsmgycY
#
# This basic one-dimensional 'fire' simulation works roughly as follows:
# There's a underlying array of 'heat' cells, that model the temperature
# at each point along the line.  Every cycle through the simulation,
# four steps are performed:
#  1) All cells cool down a little bit, losing heat to the air
#  2) The heat from each cell drifts 'up' and diffuses a little
#  3) Sometimes randomly new 'sparks' of heat are added at the bottom
#  4) The heat from each cell is rendered as a color into the leds array
#     The heat-to-color mapping uses a palette approximating black-body radiation.
#
# Temperature is in arbitrary units from 0 (cold black) to 255 (white hot).
#
# This simulation scales it self a bit depending on NUM_LEDS; it should look
# "OK" on anywhere from 20 to 100 LEDs without too much tweaking.
#
# I recommend running this simulation at anywhere from 30-100 frames per second,
# meaning an interframe delay of about 10-35 milliseconds.
#
# Looks best on a high-density LED setup (60+ pixels/meter).
#
#
# There are two main parameters you can play with to control the look and
# feel of your fire: COOLING (used in step 1 above), and SPARKING (used
# in step 3 above).
#
# COOLING: How much does the air cool as it rises?
# Less cooling = taller flames.  More cooling = shorter flames.
# Default 50, suggested range 20-100
#define COOLING  80  // 60
COOLING = 60

# SPARKING: What chance (out of 255) is there that a new spark will be lit?
# Higher chance = more roaring fire.  Lower chance = more flickery fire.
# Default 120, suggested range 50-200.
#define SPARKING 80
SPARKING = 80

IGNITION = max(3, NUM_CELLS//10)    # ignition area: 10% of segment length or minimum 3 pixels
MaxCool = (((20 + COOLING//3) * 16) // NUM_CELLS)+2
CUSTOM = 0

def fire2012(column):
    col = column * NUM_CELLS
    heat = memoryview(HEAT)[col:col+NUM_CELLS]

    # Step 1.  Cool down every cell a little
    for row in range(NUM_CELLS):
        minTemp = (IGNITION-row)//4 + 16 if (row<IGNITION) else 0    # should not become black in ignition area
        cool = random.randint(0, MaxCool)
        temp = max(0, heat[row] - cool)
        heat[row] = minTemp if (temp<minTemp) else temp

    # Step 2.  Heat from each cell drifts 'up' and diffuses a little
    k = NUM_CELLS-1
    while (k >= 2):
        heat[k] = (heat[k-1] + 2*heat[k-2]) // 3
        k -= 1

    # Step 3.  Randomly ignite new 'sparks' of heat near the bottom
    if (random.randint(0, 255) < SPARKING):
        j = random.randint(0, IGNITION);
        boost = (17+CUSTOM) * (IGNITION - j//2) // IGNITION   # integer math!
        newheat = heat[j] + random.randint(96+2*boost, 207+boost)
        heat[j] = newheat if (newheat <= 255) else 255

    # Step 4.  Map from heat cells to LED colors
    for row in range(NUM_CELLS):
        color = PALETTE[heat[row]]
        pfb.pixel(column, row, color)


########## main loop #################

create_lookup_table(ALL_palettes[ACT_PALETTE])
Debug = True

while True:
    t1 = time.monotonic_ns()
    for column in range(NUM_COLS):
        fire2012(column)
    t2 = time.monotonic_ns()

    pfb.display()
    t3 = time.monotonic_ns()

    if Debug:
        d1 = (t2 - t1) / 1000000.0
        print(f"Compute {d1} ms", end=" +\t")
        d2 = (t3 - t2) / 1000000.0
        print(f"Display {d2} ms", end=" =\t")
        print(f"Total {d1+d2} ms")

    time.sleep(SPEED)

