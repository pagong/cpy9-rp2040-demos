import board
import rainbowio
import random
import time

from bounce.matrix32 import MatrixSetup

NEO_PIN = board.IO1

matrix = MatrixSetup(NEO_PIN, "vstripes", 0.1)

######

WIDTH = matrix._width
HEIGHT = matrix._height

X = WIDTH  // 2
Y = HEIGHT // 2

COL = 0
LEN = 10

def draw():
    global X, Y, COL, LEN

    nextX = X + (random.randint(0, LEN) - LEN//2)
    if nextX<0: nextX = 0
    if nextX >= WIDTH: nextX = WIDTH-1
  
    nextY = Y + (random.randint(0, LEN) - LEN//2)
    if nextY<0: nextY = 0
    if nextY >= HEIGHT: nextY = HEIGHT-1
    
    color = rainbowio.colorwheel(COL)
    matrix.line(X, Y, nextX, nextY, color)

    COL = (COL + random.randint(0, 10)) & 255

    X = nextX
    Y = nextY


def loop():
    CNT = 246

    matrix.fill(0)
    for i in range(CNT):
        draw()
        matrix.display()


while True:
    loop()
    time.sleep(1)