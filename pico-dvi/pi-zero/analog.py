# SPDX-FileCopyrightText: 2024 Pagong
# SPDX-License-Identifier: MIT

import os
import time
import rtc

import board
import busio
import adafruit_ds3231

import displayio
import framebufferio
import picodvi

##############

displayio.release_displays()

# pin defs for RP2040-PiZero
fb = picodvi.Framebuffer(320, 240,
    clk_dp=board.CKP, clk_dn=board.CKN,
    red_dp=board.GP26, red_dn=board.GP27,
    green_dp=board.GP24, green_dn=board.GP25,
    blue_dp=board.GP22, blue_dn=board.GP23,
    color_depth=8)

display = framebufferio.FramebufferDisplay(fb, auto_refresh=False)

##############

UTC_OFFSET = os.getenv('UTC_OFFSET')
TZ = os.getenv('TZ')

try:
    i2c = busio.I2C(board.GP3, board.GP2)  # PiZero SCL=GP3 and SDA=GP2
    ds3231 = adafruit_ds3231.DS3231(i2c)
    dtm = ds3231.datetime
except:
    dtm = time.struct_time( (2024, 11, 4,    13, 45, 0,    0, 0, 0))

rtc.RTC().datetime = dtm

##############

from adafruit_turtle import Color, turtle

turtle = turtle(display)
#origin = turtle.position()
origin = (-1, 1)

turtle.mode("logo")
turtle.hideturtle()
turtle.speed(0)


def hand_h1():
    turtle.pensize(1)
    turtle.pendown()
    turtle.right(145)
    turtle.forward(9)
    turtle.left(160)
    turtle.forward(20)
    turtle.left(150)
    turtle.forward(20)
    turtle.left(160)
    turtle.forward(9)
    turtle.penup()

def hand_h2():
    l=5
    turtle.pensize(1)
    turtle.pendown()
    turtle.left(135)
    turtle.forward(l)
    turtle.back(l)
    turtle.left(90)
    turtle.forward(l)
    turtle.back(l)
    turtle.left(135)
    turtle.forward(3*l)
    turtle.penup()

def hand_h3():
    l=3
    turtle.pensize(1)
    turtle.pendown()
    turtle.left(90)
    turtle.forward(l)
    turtle.left(90)
    turtle.forward(2*l)
    turtle.left(90)
    turtle.forward(2*l)
    turtle.left(90)
    turtle.forward(2*l)
    turtle.left(90)
    turtle.forward(l)
    turtle.right(90)
    turtle.forward(4*l)
    turtle.penup()
    
def hand_h4():
    turtle.pensize(2)
    turtle.back(5)
    turtle.pendown()
    turtle.forward(20)
    turtle.penup()

def hand_h5():
    turtle.pensize(1)
    turtle.back(5)
    turtle.pendown()
    turtle.dot(2)
    turtle.forward(20)
    turtle.penup()
    
def hand_m():
    turtle.pensize(1)
    turtle.pendown()
    turtle.forward(24)
    turtle.penup()

def hand_s():
    turtle.pensize(1)
    turtle.forward(30)
    turtle.pendown()
    turtle.dot(1)
    turtle.penup()

##############

def Draw_center():
    turtle.pencolor(Color.RED)
    turtle.goto(origin)
    turtle.pensize(1)
    turtle.pendown()
    turtle.dot(1)
    turtle.penup()

def Draw_hour(h, m):
    turtle.pencolor(Color.BLUE)
    turtle.goto(origin)
    h = 30 * (h%12) + (m//2)
    turtle.setheading(h)
    hand_h1()

def Draw_minute(m):
    turtle.pencolor(Color.GREEN)
    turtle.goto(origin)
    turtle.setheading( (m%60) * 6)
    hand_m()

def Draw_second(s):
    turtle.pencolor(Color.RED)
    turtle.goto(origin)
    turtle.setheading( (s%60) * 6)
    hand_s()

# load clock face as background bitmap
FACE = "/Circle08.bmp"
turtle.bgpic(FACE)
Draw_center()
display.refresh()
last_sec = -1

# Main loop
while True:
    lt = time.localtime()

    hour   = lt.tm_hour
    minute = lt.tm_min
    second = lt.tm_sec

    if second != last_sec:
        last_sec = second
        turtle.clear()
        Draw_hour(hour, minute)
        Draw_minute(minute)
        Draw_second(second)
        if (second %2) == 0:
            Draw_center()     
        display.refresh()

    time.sleep(0.1)

