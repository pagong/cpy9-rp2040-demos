## CircuitPython_NeoMatrix

Port of Adafruit's `Arduino` [library](https://github.com/adafruit/Adafruit_NeoMatrix) `Adafruit_NeoMatrix` to CircuitPython.
See the [Adafruit NeoPixel Überguide](https://learn.adafruit.com/adafruit-neopixel-uberguide/neomatrix-library) for everything you need to know about NeoPixel-Grids.

- Features:
  - Single matrix: 16x16, 8x32, 32x8
  - Tiled matrices: multiple single matrices

### Single matrix
- Horizontal strips
  - 16w * 16h , 8w * 32h
  - zigzag and progressive rows
- Vertical strips
  - 16w * 16h, 32w * 8h
  - zigzag and progressive columns
- position of first Pixel
  - Bottom, Top, Left, Right

### Tiled matrices
- Assumption: only identical matrices are used
  - either Nx 16x16, or Nx 8x32, or Nx 32x8
- Tiles are laid out in a regular style
  - Nx tiles in X direction, Mx tiles in Y direction
  - tiles are wired either in progressive or zigzag mode
- Position of first Tile
  - Bottom, Top, Left, Right

