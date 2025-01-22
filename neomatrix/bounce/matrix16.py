# SPDX-FileCopyrightText: 2024 Mike Doerr
# SPDX-License-Identifier: MIT

#######################################

# Map 16x16 NeoPixel matrix coordinates to sequential strand indices [0..255].
# Works with one square NeoMatrix tile wired as a 16x16 display.

import neopixel
from neomatrix import *

#######################################

# Use matrixMode to select matrix type for 2 tile arrangements of a 16x16 matrix
#   matrixMode = "hsquare"      # 1x1 horizontally arranged 16x16 tile
#   matrixMode = "vsquare"      # 1x1 vertically arranged 16x16 tile

def MatrixSetup(pixel_pin, matrixMode, brightness = 0.1):

    if (matrixMode == "hsquare"):       # horizontally arranged 16x16 tiles
        matrixType = (
            NEO_MATRIX_BOTTOM + NEO_MATRIX_LEFT + NEO_MATRIX_ROWS + NEO_MATRIX_ZIGZAG
        )
        tileWidth = 16
        tileHeight = 16
        tilesX = 1
        tilesY = 1
        rotation = 0

    elif (matrixMode == "vsquare"):     # vertically arranged 16x16 tiles
        matrixType = (
            NEO_MATRIX_TOP + NEO_MATRIX_LEFT + NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG
        )
        tileWidth = 16
        tileHeight = 16
        tilesX = 1
        tilesY = 1
        rotation = 0

    else:
        raise ValueError(matrixMode)


    # Update to match the number of NeoPixels you have connected
    #pixel_num = 256
    pixel_num = (tileWidth * tilesX) * (tileHeight * tilesY)

    # initialize the neopixels. Change out for dotstars if needed.
    pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=brightness, auto_write=False)

    return NeoMatrix(pixels,
                     tileWidth, tileHeight,
                     tilesX, tilesY,
                     matrixType, rotation)

#######################################

