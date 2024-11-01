# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-FileCopyrightText: Adapted from Phil B.'s 16bit_hello Arduino Code
# SPDX-FileCopyrightText: 2024 Pagong (slide show)
#
# SPDX-License-Identifier: MIT

import os
import gc
import random
import time
import displayio
import picodvi
import board
import framebufferio

displayio.release_displays()

# pin defs for DVI Sock
fb = picodvi.Framebuffer(320, 240,
	clk_dp=board.CKP, clk_dn=board.CKN,
	red_dp=board.GP26, red_dn=board.GP27,
	green_dp=board.GP24, green_dn=board.GP25,
	blue_dp=board.GP22, blue_dn=board.GP23,
	color_depth=8)

display = framebufferio.FramebufferDisplay(fb)

group = displayio.Group()
display.root_group = group


def clean_up(group_name):
    for _ in range(len(group_name)):
        group_name.pop()
    gc.collect()

def show_bitmap(filename, seconds):
    gc.collect()
    odb = displayio.OnDiskBitmap(filename)
    grid = displayio.TileGrid(odb, pixel_shader=odb.pixel_shader)
    #print(odb.width, odb.height)
    if odb.width < 320:
        grid.x = (320 - odb.width) // 2
    group.append(grid)

    time.sleep(seconds)

    clean_up(group)
    del grid
    del odb
    gc.collect()

# Return a duplicate of the input list in a random (shuffled) order.
def shuffled(seq):
    return sorted(seq, key=lambda _: random.random())


os.chdir("/sd")
files_bmp = sorted(os.listdir())
print(files_bmp)
LIST = list(range(len(files_bmp)))
#LIST = shuffled(LIST)
print(LIST)

WAIT = 10
while True:
    for i in LIST:
        show_bitmap(files_bmp[i], WAIT)

