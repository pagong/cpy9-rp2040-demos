## CircuitPython_NeoMatrix

Port of Adafruit's `Adafruit_NeoMatrix` [library](https://github.com/adafruit/Adafruit_NeoMatrix) for the Arduino to CircuitPython.  
See the [Adafruit NeoPixel Überguide](https://learn.adafruit.com/adafruit-neopixel-uberguide/neomatrix-library) for everything you need to know about NeoPixel-Grids.

- Features:
  - Single matrix: 8x8, 16x16, 8x32, 32x8 NeoPixels
  - Tiled matrices: multiple single matrices

### Single matrix
- Horizontal strips (row major)
  - 8w * 8h, 16w * 16h , 8w * 32h
  - zigzag and progressive rows
- Vertical strips (column major)
  - 8w * 8h, 16w * 16h, 32w * 8h
  - zigzag and progressive columns
- position of first Pixel
  - Bottom, Top, Left, Right

### Tiled matrices
- Assumption: only identical matrices are used
  - tiles of size 8 * 8, or 16 * 16, or 8 * 32, or 32 * 8
- Tiles are laid out in a regular style
  - N * tiles in X direction, either Left --> Right, or reversed
  - M * tiles in Y direction, either Top --> Down, or reversed
  - tiles are wired either in progressive or zigzag mode
- Position of first Tile
  - Bottom, Top, Left, Right

