# SPDX-FileCopyrightText: 2023 Frederick M Meyer
#
# SPDX-License-Identifier: MIT

import random
import os
import time
import rtc
import board
import busio
import adafruit_ds3231
import displayio
import framebufferio
import rgbmatrix
#import digitalio
import terminalio
import adafruit_display_text as adt
import adafruit_display_text.label as adtl

UTC_OFFSET = os.getenv('UTC_OFFSET')
TZ = os.getenv('TZ')

QUARTER = "Quarter"
HALF = "Half"
PAST = "Past"
UNTIL = "Until"
OCLOCK = "O'clock"
NOON = "Noon"
MIDNIGHT = "Midnight"
MINUTE = "Minute"
SINGLE_DIGITS = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
TEN_PLUS = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
TENS = ["Twenty", "Thirty", "Fourty", "Fifty"]

###################

displayio.release_displays()

UTC_OFFSET = os.getenv('UTC_OFFSET')
TZ = os.getenv('TZ')

try:
    i2c = busio.I2C(board.GP7, board.GP6)  # PICO SCL=GP7 and SDA=GP6
    ds3231 = adafruit_ds3231.DS3231(i2c)
    dtm = ds3231.datetime
except:
    dtm = time.struct_time( (2024, 6, 24,    1, 55, 0,    0, 0, 0))

rtc.RTC().datetime = dtm

###################

def format_hour(hour_num):
    hour = hour_num % 24
    if hour == 0:
        o_hour = MIDNIGHT
    elif hour == 12:
        o_hour = NOON
    else:
        if hour > 12:
            hour -= 12
        elif hour == 0:
            hour = 12

        if hour < 10:
            o_hour = SINGLE_DIGITS[hour - 1]
        else:
            o_hour = TEN_PLUS[hour - 10]
    return hour, o_hour

COLOR_VALUES = [0, 128, 255]  # Brighter - Possible color values used for random 0..2 selection
#COLOR_VALUES = [0, 80, 160]   # Dimmer   - Possible color values used for random 0..2 selection
#COLOR_VALUES = [0, 64, 128]   # Dimmer   - Possible color values used for random 0..2 selection

def pick_random_color():
    # Pick a random color for each line and add it to the display
    r = COLOR_VALUES[random.randint(0, 2)]
    g = COLOR_VALUES[random.randint(0, 2)]
    b = COLOR_VALUES[random.randint(0, 2)]
    if not (r | g | b): r = g = b = COLOR_VALUES[2] # Set to white if black result
    return (r<<16|g<<8|b)

##############

RGB_TYPE = "SeenGreat"
#RGB_TYPE = "Pimoroni"

def seengreat_rgb():
    # Code for Pico rp2040 on SeenGreat RGB Matrix Adapter Board
    return rgbmatrix.RGBMatrix(
        width=64, height=64, bit_depth=2,
        rgb_pins=[board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
        addr_pins=[board.GP10, board.GP16, board.GP18, board.GP20, board.GP22],
        clock_pin=board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13)

def pimoroni_rgb():
    # Code for Pico rp2040 on D-I-Y Adapter (Pimoroni Interstate75 compatible)
    return rgbmatrix.RGBMatrix(
        width=64, height=64, bit_depth=2,
        rgb_pins=[board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5],
        addr_pins=[board.GP6, board.GP7, board.GP8, board.GP9, board.GP10],
        clock_pin=board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13)

if RGB_TYPE == "SeenGreat":     matrix = seengreat_rgb()
elif RGB_TYPE == "Pimoroni":    matrix = pimoroni_rgb()
else:                           raise NameError(RGB_TYPE)

##############

# These pins are for the Hub75-Pico adapter by SeenGreat
#matrix = rgbmatrix.RGBMatrix(
#    width=64, height=64, bit_depth=2,
#    rgb_pins=[board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
#    addr_pins=[board.GP10, board.GP16, board.GP18, board.GP20, board.GP22],
#    clock_pin=board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True, rotation = 0)

##############

last_minute_displayed = -1
while True:
    lt = time.localtime()

    hour = lt.tm_hour
    min = lt.tm_min

    #hour = 12  # For testing
    #min = 00   # For testing

    if last_minute_displayed != min:
        last_minute_displayed = min

        if min <= 30:
            o_min_half = PAST
            hour, o_hour = format_hour(hour)
        else:
            o_min_half = UNTIL
            min = 60 - min
            hour, o_hour = format_hour(hour + 1)

        if min == 15:
            o_min = QUARTER
        elif min == 30:
            o_min = HALF
        elif min == 0:
            o_min = ""
            o_min_half = ""
        elif min < 10:
            o_min = SINGLE_DIGITS[min - 1]
        elif min < 20:
            o_min = TEN_PLUS[min - 10]
        else:
            o_min = TENS[(min // 10) - 2]
            if min % 10:
                o_min += " " + SINGLE_DIGITS[(min % 10) - 1]

        if o_min not in [QUARTER, HALF, ""]:
            o_min += " " + MINUTE
            if min != 1: o_min += "s"

        if min > 0 or o_hour in [MIDNIGHT, NOON]:
            txt = (o_min + " " + o_min_half + " " + o_hour).strip()
        else:
            txt = (o_min + " " + o_min_half + " " + o_hour + " " + OCLOCK).strip()

        text_list = adt.wrap_text_to_pixels(txt, 60, font=terminalio.FONT)
        
        total_height = 0
        max_width = 0
        line_list = []
        for w in text_list:
            line = adtl.Label(
                terminalio.FONT,
                color=pick_random_color(),
                text=w,
                scale=1)
            line_list.append(line)
            zx, zy, zwidth, zheight = line.bounding_box
            total_height += zheight
            max_width = max(max_width, zwidth)
        xwork = ((60 - max_width) // 2) + 2
        ywork = ((60 - total_height) // 2) + 2 + 6

        current_y = ywork        
        g = displayio.Group()
        for l in line_list:
            l.x = xwork
            l.y = current_y
            zx, zy, zwidth, zheight = l.bounding_box
            current_y += zheight
            g.append(l)
        display.root_group=g

    time.sleep(1)

