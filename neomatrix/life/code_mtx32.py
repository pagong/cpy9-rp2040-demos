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
pixel_num = 1024

# initialize the neopixels. Change out for dotstars if needed.
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.02, auto_write=False)

####

# Use mode to select matrix type for 4 common tile arrangements of a 32x32 matrix
mode = "hsquares"       # horizontally arranged 16x16 tiles
#mode = "vsquares"      # vertically arranged 16x16 tiles
#mode = "hstripes"      # horizontally arranged 32x8 tiles
#mode = "vstripes"      # vertically arranged 8x32 tiles

if (mode == "hsquares"):
    matrixType = (
        NEO_MATRIX_BOTTOM + NEO_MATRIX_LEFT + NEO_MATRIX_ROWS + NEO_MATRIX_ZIGZAG +
        NEO_TILE_BOTTOM + NEO_TILE_LEFT + NEO_TILE_ROWS + NEO_TILE_PROGRESSIVE
    )
    tileWidth = 16
    tileHeight = 16
    tilesX = 2
    tilesY = 2
    color = 0x0000ff

elif (mode == "vsquares"):
    matrixType = (
        NEO_MATRIX_TOP + NEO_MATRIX_LEFT + NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG +
        NEO_TILE_TOP + NEO_TILE_LEFT + NEO_TILE_COLUMNS + NEO_TILE_PROGRESSIVE
    )
    tileWidth = 16
    tileHeight = 16
    tilesX = 2
    tilesY = 2
    color = 0xff0000

elif (mode == "vstripes"):
    matrixType = (
        NEO_MATRIX_BOTTOM + NEO_MATRIX_LEFT + NEO_MATRIX_ROWS + NEO_MATRIX_ZIGZAG +
        NEO_TILE_BOTTOM + NEO_TILE_LEFT + NEO_TILE_COLUMNS + NEO_TILE_ZIGZAG
    )
    tileWidth = 8
    tileHeight = 32
    tilesX = 4
    tilesY = 1
    color = 0x00ffff

elif (mode == "hstripes"):
    matrixType = (
        NEO_MATRIX_TOP + NEO_MATRIX_LEFT + NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG +
        NEO_TILE_TOP + NEO_TILE_LEFT + NEO_TILE_ROWS + NEO_TILE_ZIGZAG
    )
    tileWidth = 32
    tileHeight = 8
    tilesX = 1
    tilesY = 4
    color = 0xffff00

else:
    print("Invalid mode = ", mode)
    exit

####

matrix = NeoMatrix(pixels, tileWidth, tileHeight, tilesX, tilesY, matrixType)

initial_cells = [
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (6, 1),
]

# initialize the animation
life = ConwaysLifeAnimation(matrix, 0.2, 0xff00ff, initial_cells)

while True:
    # call animation to show the next animation frame
    life.animate()

