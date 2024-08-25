# SPDX-FileCopyrightText: 2022 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from rainbowio import colorwheel
import neopixel

# for Rp2040-Matrix

MAXPIX = 250
NUMPIXELS = 25     # Update this to match the number of LEDs.
SPEED = 0.2        # Increase to slow down the rainbow. Decrease to speed it up.
BRIGHTNESS = 0.2   # A number between 0.0 and 1.0, where 0.0 is off, and 1.0 is max.
PIN = board.GP16   # This is the default pin on the 5x5 NeoPixel WaveShare Matrix

pixels = neopixel.NeoPixel(PIN, NUMPIXELS, brightness=BRIGHTNESS, auto_write=False)


def rainbow_cycle(wait):
    for color in range(255):
        for pixel in range(MAXPIX):  # pylint: disable=consider-using-enumerate
            pixel_index = (pixel * 256 // MAXPIX) + color * 5
            if (pixel < NUMPIXELS): 
                pixels[pixel] = colorwheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


while True:
    rainbow_cycle(SPEED)
