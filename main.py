from classes import *
from functions import *
import time
import os

from scenes import *

WIDTH = 120
HEIGHT = 30

FPS = 60

def main():
    global screen, copyScreen
    init()

    curScene = RunningScene(screen)

    while True:
        deltaTime = delay()

        curScene.update(deltaTime)
        curScene.inputKey(deltaTime)
        curScene.render()

        fixConsoleSize()
        updateDisplay()

        curScene = curScene.nextScene

def init():
    global screen, copyScreen, previousTime, delayTime
    hideCursor()
    setQuickEditMode(False)
    os.system(f"mode {WIDTH}, {HEIGHT}")

    screen = Surface(WIDTH, HEIGHT)
    copyScreen = Surface(WIDTH, HEIGHT)
    
    previousTime = time.time()
    delayTime = 1/FPS

def fixConsoleSize():
    global copyScreen
    terminal_size = os.get_terminal_size()

    if (terminal_size.lines != HEIGHT or terminal_size.columns != WIDTH):
        os.system(f"mode {WIDTH}, {HEIGHT}")
        hideCursor()
        
        copyScreen = Surface(WIDTH, HEIGHT)
        updateDisplay()

def updateDisplay():
    global screen, copyScreen
    a = False
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if (screen.image[i][j] == copyScreen.image[i][j]):
                if (screen.image[i][j].start and j + 1 < WIDTH and screen.image[i][j + 1] != copyScreen.image[i][j + 1]):
                    pass
                else:
                    continue
            
            char = screen.image[i][j]

            if (char.start):
                if (j + 1 < WIDTH and screen.image[i][j+1].end):
                    gotoxy(j, i)
                    printf("  ")
                    gotoxy(j, i)
                    printf(char.byte)
                    printf(screen.image[i][j+1].byte)
                else:
                    gotoxy(j, i)
                    printf(" ")
            elif (char.end):
                if (j - 1 >= 0 and screen.image[i][j-1].start):
                    pass
                else:
                    gotoxy(j, i)
                    printf(" ")
            else:
                if (copyScreen.image[i][j].start):
                    gotoxy(j, i)
                    printf(" ")
                
                gotoxy(j, i)
                printf(char.byte)

            copyScreen.image[i][j] = screen.image[i][j]

def delay() -> float:
    global previousTime, delayTime

    curTime = time.time()

    curDelayTime = curTime - previousTime
    
    if (delayTime > curDelayTime):
        time.sleep(delayTime - curDelayTime)

    curTime = time.time()

    deltaTime = curTime - previousTime

    previousTime = curTime

    return deltaTime

if (__name__ == "__main__"):
    main()