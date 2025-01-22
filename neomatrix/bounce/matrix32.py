# SPDX-FileCopyrightText: 2024 Mike Doerr
# SPDX-License-Identifier: MIT

#######################################

# Map 32x32 NeoPixel matrix coordinates to sequential strand indices [0..1023].
# Works with four NeoMatrix tiles (either squares or stripes) wired as a 32x32 display.

import neopixel
from neomatrix import *

#######################################

# Use matrixMode to select matrix type for 4 common tile arrangements of a 32x32 matrix
#   matrixMode = "hsquares"      # 2x2 horizontally arranged 16x16 tiles
#   matrixMode = "vsquares"      # 2x2 vertically arranged 16x16 tiles
#   matrixMode = "vstripes"      # 4x1 vertically arranged 8x32 tiles
#   matrixMode = "hstripes"      # 1x4 horizontally arranged 32x8 tiles

def MatrixSetup(pixel_pin, matrixMode, brightness = 0.1):

    if (matrixMode == "hsquares"):       # horizontally arranged 16x16 tiles
        matrixType = (
            NEO_MATRIX_BOTTOM + NEO_MATRIX_LEFT + NEO_MATRIX_ROWS + NEO_MATRIX_ZIGZAG +
            NEO_TILE_BOTTOM + NEO_TILE_LEFT + NEO_TILE_ROWS + NEO_TILE_PROGRESSIVE
        )
        tileWidth = 16
        tileHeight = 16
        tilesX = 2
        tilesY = 2
        rotation = 0

    elif (matrixMode == "vsquares"):     # vertically arranged 16x16 tiles
        matrixType = (
            NEO_MATRIX_TOP + NEO_MATRIX_LEFT + NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG +
            NEO_TILE_TOP + NEO_TILE_LEFT + NEO_TILE_COLUMNS + NEO_TILE_PROGRESSIVE
        )
        tileWidth = 16
        tileHeight = 16
        tilesX = 2
        tilesY = 2
        rotation = 0

    elif (matrixMode == "vstripes"):     # vertically arranged 8x32 tiles
        matrixType = (
            NEO_MATRIX_BOTTOM + NEO_MATRIX_LEFT + NEO_MATRIX_ROWS + NEO_MATRIX_ZIGZAG +
            NEO_TILE_BOTTOM + NEO_TILE_LEFT + NEO_TILE_COLUMNS + NEO_TILE_ZIGZAG
        )
        tileWidth = 8
        tileHeight = 32
        tilesX = 4
        tilesY = 1
        rotation = 0

    elif (matrixMode == "hstripes"):     # horizontally arranged 32x8 tiles
        matrixType = (
            NEO_MATRIX_TOP + NEO_MATRIX_LEFT + NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG +
            NEO_TILE_TOP + NEO_TILE_LEFT + NEO_TILE_ROWS + NEO_TILE_ZIGZAG
        )
        tileWidth = 32
        tileHeight = 8
        tilesX = 1
        tilesY = 4
        rotation = 0

    else:
        print("Invalid mode = ", matrixMode)
        exit


    # Update to match the number of NeoPixels you have connected
    #pixel_num = 1024
    pixel_num = (tileWidth * tilesX) * (tileHeight * tilesY)

    # initialize the neopixels. Change out for dotstars if needed.
    pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=brightness, auto_write=False)

    return NeoMatrix(pixels,
                     tileWidth, tileHeight,
                     tilesX, tilesY,
                     matrixType, rotation)

#######################################

