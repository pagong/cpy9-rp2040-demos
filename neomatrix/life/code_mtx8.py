# SPDX-FileCopyrightText: 2024 Tim Cocks for Adafruit Industries
# SPDX-FileCopyrightText: 2024 Michael Doerr
#
# SPDX-License-Identifier: MIT
import board
import neopixel

from neomatrix import *

from life.mtx_life import ConwaysLifeAnimation

# Update to match the pin connected to your NeoPixels
pixel_pin = board.IO1
# Update to match the number of NeoPixels you have connected
pixel_num = 256

# initialize the neopixels. Change out for dotstars if needed.
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.05, auto_write=False)

initial_cells = [
    (2, 2),
    (3, 2),
    (4, 2),
    (5, 2),
    (6, 2),
]

matrixType = ( NEO_MATRIX_BOTTOM + NEO_MATRIX_LEFT + NEO_MATRIX_ROWS + NEO_MATRIX_ZIGZAG )

matrix = NeoMatrix(pixels, 8, 32, 1, 1, matrixType)

# initialize the animation
life = ConwaysLifeAnimation(matrix, 0.5, 0x00ffff, initial_cells)

while True:
    # call animation to show the next animation frame
    life.animate()

