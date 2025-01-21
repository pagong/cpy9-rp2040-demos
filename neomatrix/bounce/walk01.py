import board
import rainbowio
import random

from bounce.matrix32 import MatrixSetup

NEO_PIN = board.IO1

matrix = MatrixSetup(NEO_PIN, "vstripes", 0.1)

######

WIDTH = 32
HEIGHT = 32

X = WIDTH  // 2
Y = HEIGHT // 2

COL = 0
LEN = 10

def draw():
    global X, Y, COL, LEN

    nextX = X + random.randint(0, LEN) - LEN//2
    if nextX<0: nextX = 0
    if nextX >= WIDTH: nextX = WIDTH-1
  
    nextY = Y + random.randint(0, LEN) - LEN//2
    if nextY<0: nextY = 0
    if nextY >= HEIGHT: nextY = HEIGHT-1
    
    color = rainbowio.colorwheel(COL)
    matrix.line(X, Y, nextX, nextY, color)

    COL = (COL + random.randint(0, 10)) % 256

    X = nextX
    Y = nextY

matrix.fill(0)
while True:
    draw()
    matrix.display()
