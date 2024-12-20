# SPDX-FileCopyrightText: 2024 Michael Doerr
# SPDX-FileCopyrightText: Copyright (c) 2024 Michael Doerr
#
# SPDX-License-Identifier: MIT
"""
`circuitpython_neomatrix`
================================================================================

Port of the Arduino library `Adafruit_NeoMatrix` to CircuitPython

Idea: pre-compute the mapping from X & Y matrix coordinates to index numbers
      of a NeoPixel strand and store the result in an `adafruit_pixelmap`.

Inspired by `adafruit_pixel_framebuf.py` and `adafruit_led_animation/grid.py`.

* Author(s): Michael Doerr

Implementation Notes
--------------------

**Hardware:**

* `Adafruit NeoPixels <https://www.adafruit.com/category/168>`_
* `Adafruit DotStars <https://www.adafruit.com/category/885>`_
* `Flexible 8x32 NeoPixel RGB LED Matrix <https://www.adafruit.com/product/2294>`_
* `Flexible 16x16 NeoPixel RGB LED Matrix <https://www.adafruit.com/product/2547>`_
* `Flexible 8x8 NeoPixel RGB LED Matrix <https://www.adafruit.com/product/2612>`_
* `Adafruit NeoPixel 8x8 NeoMatrices <https://www.adafruit.com/product/3052>`_
* `Adafruit DotStar High Density 8x8 Grid <https://www.adafruit.com/product/3444>`_
* `Adafruit NeoPixel FeatherWing <https://www.adafruit.com/product/2945>`_
* `Adafruit DotStar FeatherWing <https://www.adafruit.com/product/3449>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's framebuf library: https://github.com/adafruit/Adafruit_CircuitPython_framebuf
* Adafruit's pixelmap library: https://github.com/adafruit/Adafruit_CircuitPython_pixelmap

"""

### ----------------------------------------


from micropython import const
from adafruit_pixelmap import PixelMap
from adafruit_framebuf import FrameBuffer, RGB888


### ----------------------------------------


# Matrix layout information is passed in the 'matrixType' parameter
# for the `NeoMatrix` and `NeoGrid` classes.

# These define the layout for a single 'unified' matrix (e.g. one made
# from NeoPixel strips, or a single NeoPixel shield), or for the pixels
# within each matrix of a tiled display (e.g. multiple NeoPixel shields).

NEO_MATRIX_TOP: int = const( 0x00 )       # Pixel 0 is at top of matrix
NEO_MATRIX_BOTTOM: int = const( 0x01 )    # Pixel 0 is at bottom of matrix
NEO_MATRIX_LEFT: int = const( 0x00 )      # Pixel 0 is at left of matrix
NEO_MATRIX_RIGHT: int = const( 0x02 )     # Pixel 0 is at right of matrix
MSK_MATRIX_CORNER: int = const( 0x03 )    # Bitmask for pixel 0 matrix corner

NEO_MATRIX_ROWS: int = const( 0x00 )       # Matrix is row major (horizontal)
NEO_MATRIX_COLUMNS: int = const( 0x04 )    # Matrix is column major (vertical)
MSK_MATRIX_AXIS: int = const( 0x04 )       # Bitmask for row/column layout

NEO_MATRIX_PROGRESSIVE: int = const( 0x00 ) # Same pixel order across each line
NEO_MATRIX_ZIGZAG: int = const( 0x08 )      # Pixel order reverses between lines
MSK_MATRIX_SEQUENCE: int = const( 0x08 )    # Bitmask for pixel line order


# These apply only to tiled displays (multiple matrices):

NEO_TILE_TOP: int = const( 0x00 )       # First tile is at top of matrix
NEO_TILE_BOTTOM: int = const( 0x10 )    # First tile is at bottom of matrix
NEO_TILE_LEFT: int = const( 0x00 )      # First tile is at left of matrix
NEO_TILE_RIGHT: int = const( 0x20 )     # First tile is at right of matrix
MSK_TILE_CORNER: int = const( 0x30 )    # Bitmask for first tile corner

NEO_TILE_ROWS: int = const( 0x00 )       # Tiles ordered in rows
NEO_TILE_COLUMNS: int = const( 0x40 )    # Tiles ordered in columns
MSK_TILE_AXIS: int = const( 0x40 )       # Bitmask for tile H/V orientation

NEO_TILE_PROGRESSIVE: int = const( 0x00 ) # Same tile order across each line
NEO_TILE_ZIGZAG: int = const( 0x80 )      # Tile order reverses between lines
MSK_TILE_SEQUENCE: int = const( 0x80 )    # Bitmask for tile line order


### ----------------------------------------


# `NeoGrid` is inspired by `adafruit_led_animation.grid.PixelGrid`
class NeoGrid:
    """
    NeoGrid lets you address a pixel strip with x and y coordinates.

    :param strip: An object that implements the Neopixel or Dotstar protocol.
    :param width: Tile width = number of pixels in a tile in X direction
    :param height: Tile height = number of pixels in a tile in Y direction
    :param tileX: Number of tiles in horizontal X direction
    :param tileY: Number of tiles in vertical Y direction
    :param MatrixType: see Adafruit_NeoMatrix for valid values (default 0)

    """
    # pylint: disable=too-many-arguments,too-many-locals
    def __init__(
        self,
        strip,
        width, height,
        tileX, tileY,
        matrixType,
    ):

        self.tileW = width
        self.tileH = height
        self.tileX = tileX
        self.tileY = tileY
        self.gridW = width * tileX
        self.gridH = height * tileY
        #print(self.tileW, self.tileH, self.tileX, self.tileY, self.gridW, self.gridH)

        self.matrixType = matrixType
        self._pixels = strip
        self._map = []

        for x in range(0, self.gridW):
            self._map.append(
                PixelMap(
                    strip,
                    [self.map1pix(x, y) for y in range(0, self.gridH)],
                    individual_pixels=True,
                )
            )
        self.n = len(self._map)


    def __repr__(self):
        return "[" + ", ".join([str(self[x]) for x in range(self.n)]) + "]"


    def __setitem__(self, index, val):
        if isinstance(index, slice):
            raise NotImplementedError("NeoGrid does not support slices")

        if isinstance(index, tuple):
            self._map[index[0]][index[1]] = val
        else:
            raise ValueError("NeoGrid assignment needs a sub-index or x,y coordinate")

        if self._pixels.auto_write:
            self.show()


    def __getitem__(self, index):
        if isinstance(index, slice):
            raise NotImplementedError("NeoGrid does not support slices")
        if index < 0:
            index += len(self)
        if index >= self.n or index < 0:
            raise IndexError("x is out of range")
        return self._map[index]


    def __len__(self):
        return self.n


    def fill(self, color):
        """
        Fill the NeoGrid with the specified color.

        :param color: Color to use.
        """
        for strip in self._map:
            strip.fill(color)


    def show(self):
        """
        Shows the pixels on the underlying strip.
        """
        self._pixels.show()


    @property
    def brightness(self):
        """
        brightness from the underlying strip.
        """
        return self._pixels.brightness

    @brightness.setter
    def brightness(self, brightness):
        # pylint: disable=attribute-defined-outside-init
        self._pixels.brightness = min(max(brightness, 0.0), 1.0)


    @property
    def auto_write(self):
        """
        auto_write from the underlying strip.
        """
        return self._pixels.auto_write

    @auto_write.setter
    def auto_write(self, value):
        self._pixels.auto_write = value

    ### ### ### ### ###


    def map1pix(self, x, y) -> int:
        """
        Return the strand index for the given X & Y coordinates.
        """

        # Standard single matrix or tiled matrices
        corner = self.matrixType & MSK_MATRIX_CORNER;

        tileOffset = 0
        if (self.tileX * self.tileY) > 1:
            # Tiled display, multiple matrices

            minor = x // self.tileW         # Tile # X/Y; presume row major to
            major = y // self.tileH         # start (will swap later if needed)
            x = x - (minor * self.tileW)    # Pixel X/Y within tile
            y = y - (major * self.tileH)    # (-* is less math than modulo)

            # Determine corner of entry, flip axes if needed
            if (self.matrixType & NEO_TILE_RIGHT):
                minor = self.tileX - 1 - minor
            if (self.matrixType & NEO_TILE_BOTTOM):
                major = self.tileY - 1 - major;

            # Determine actual major axis of tiling
            if ((self.matrixType & MSK_TILE_AXIS) == NEO_TILE_ROWS):
                majorScale = self.tileX
            else:
                major, minor = minor, major
                majorScale = self.tileY

            # Determine tile number
            if ((self.matrixType & MSK_TILE_SEQUENCE) == NEO_TILE_PROGRESSIVE):
                # All tiles in same order
                tile = major * majorScale + minor
            else:
                # Zigzag; alternate rows change direction.  On these rows,
                # this also flips the starting corner of the matrix for the
                # pixel math later.
                if (major & 1):
                    corner ^= MSK_MATRIX_CORNER
                    tile = (major + 1) * majorScale - 1 - minor
                else:
                    tile = major * majorScale + minor

            # Index of first pixel in tile
            tileOffset = tile * self.tileW * self.tileH

        # else no tiling (handle as single tile)
        pixelOffset = 0

        # Find pixel number within tile
        minor = x   # Presume row major to start
        major = y   # (will swap later if needed)

        # Determine corner of entry, flip axes if needed
        if (corner & NEO_MATRIX_RIGHT):
            minor = self.tileW - 1 - minor
        if (corner & NEO_MATRIX_BOTTOM):
            major = self.tileH - 1 - major

        # Determine actual major axis of matrix
        if ((self.matrixType & MSK_MATRIX_AXIS) == NEO_MATRIX_ROWS):
            majorScale = self.tileW
        else:
            major, minor = minor, major
            majorScale = self.tileH

        # Determine pixel number within tile/matrix
        if ((self.matrixType & MSK_MATRIX_SEQUENCE) == NEO_MATRIX_PROGRESSIVE):
            # All lines in same order
            pixelOffset = major * majorScale + minor
        else:
            # Zigzag; alternate rows change direction.
            if (major & 1):
                pixelOffset = (major + 1) * majorScale - 1 - minor
            else:
                pixelOffset = major * majorScale + minor;

        index = tileOffset + pixelOffset
        #print(x, y, index)
        return index


### ----------------------------------------

'''
  /**
   * @brief Construct a tiled matrix.
   * @param  matrixW     Individual sub-matrix (tile) width in pixels.
   * @param  matrixH     Individual sub-matrix (tile) height in pixels.
   * @param  tX          Number of tiles on the X (horizontal) axis.
   * @param  tY          Number of tiles on the Y (vertical) axis.
   * @param  pin         Arduino pin number for NeoPixel data out.
   * @param  matrixType  Tiled matrix layout - add together NEO_MATRIX_* and
   *                     NEO_TILE_* values to declare orientation, rotation,
   *                     etc.
   * @param  ledType     NeoPixel LED type, similar to Adafruit_NeoPixel
   *                     constructor (e.g. NEO_GRB).
   */
  Adafruit_NeoMatrix(uint8_t matrixW, uint8_t matrixH, uint8_t tX, uint8_t tY,
                     uint8_t pin = 6,
                     uint8_t matrixType = NEO_MATRIX_TOP + NEO_MATRIX_LEFT +
                                          NEO_MATRIX_ROWS + NEO_TILE_TOP +
                                          NEO_TILE_LEFT + NEO_TILE_ROWS,
                     neoPixelType ledType = NEO_GRB + NEO_KHZ800);


// Constructor for tiled matrices:
Adafruit_NeoMatrix::Adafruit_NeoMatrix(uint8_t mW, uint8_t mH, uint8_t tX,
                                       uint8_t tY, uint8_t pin,
                                       uint8_t matrixType, neoPixelType ledType)
    : Adafruit_GFX(mW * tX, mH * tY),
      Adafruit_NeoPixel(mW * mH * tX * tY, pin, ledType),
      type(matrixType),
      matrixWidth(mW), matrixHeight(mH),
      tilesX(tX), tilesY(tY),
      remapFn(NULL) {}
'''


BPP: int = const(3)       # 3 bytes per pixel

# `NeoMmatrix` is inspired by `adafruit_pixel_framebuf.PixelFramebuffer`
class NeoMatrix(FrameBuffer):
    """
    NeoPixel and Dotstar FrameBuffer for easy drawing of graphics
    and text on a grid of either kind of pixel

    :param strip: An object that implements the Neopixel or Dotstar protocol
    :param width: Tile width = number of pixels in X direction
    :param height: Tile height = number of pixels in Y direction
    :param tileX: Number of tiles in horizontal X direction (default 1)
    :param tileY: Number of tiles in vertical Y direction (default 1)
    :param int matrixType: see above (and Adafruit_NeoMatrix) for valid values (default 0)
    :param int rotation: A value of 0-3 representing the rotation of the framebuffer (default 0)

    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        strip,
        width: int,
        height: int,
        tileX: int = 1,
        tileY: int = 1,
        matrixType: int = 0,
        rotation: int = 0,
    ) -> None:

        #print(width, height, tileX, tileY)
        self._tileX = tileX if (tileX > 1) else 1
        self._width = width * self._tileX

        self._tileY = tileY if (tileY > 1) else 1
        self._height = height * self._tileY
        #print(self._tileX, self._width, self._tileY, self._height)

        # NeoGrid is responsible for the X+Y coord -> strand mapping
        self._grid = NeoGrid(
            strip,
            width, height,
            self._tileX, self._tileY,
            matrixType,
        )

        buffer_size = self._width * self._height * BPP
        self._buffer = bytearray(buffer_size)
        self._double_buffer = bytearray(buffer_size)

        # initialize the superclass `FrameBuffer`
        super().__init__(
            self._buffer, self._width, self._height, buf_format=RGB888
        )
        # rotation is handled on the FrameBuffer level
        self.rotation = int(rotation) % 4


    def display(self) -> None:
        """Copy the raw buffer changes to the grid and show"""
        for _y in range(self._height):
            for _x in range(self._width):
                index = (_y * self.stride + _x) * BPP
                if (
                    self._buffer[index : index + BPP] != self._double_buffer[index : index + BPP]
                ):
                    self._grid[(_x, _y)] = tuple(self._buffer[index : index + BPP])
                    self._double_buffer[index : index + BPP] = self._buffer[ index : index + BPP ]
        self._grid.show()



### ----------------------------------------

### ----------------------------------------

### ----------------------------------------

