from PIL import ImageGrab, ImageOps, Image, ImageDraw, ImageEnhance, ImageFilter

import pyautogui
import time 
from pytesseract import image_to_string
import pytesseract
import random

currentGrid = [[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]

UP = 100
LEFT = 101
DOWN = 102
RIGHT = 103
SCALE_FACTOR = 2
SPEED = 6

SPEED_LIST = list(reversed([0.005,0.01,0.05,0.1,0.5,1,2]))
WAIT = SPEED_LIST[SPEED]


def moves_map(move_id):
        moves_map = {0:UP,1:DOWN,2:LEFT,3:RIGHT}
        return moves_map[move_id]


class Cords:
    def scale_cords(cordArray):
        for index,cord in enumerate(cordArray):
            cordArray[index] = (cord[0]*SCALE_FACTOR, cord[1]*SCALE_FACTOR)
        return cordArray

    cord11 = (195, 285)
    cord12 = (305, 285)
    cord13 = (418, 285)
    cord14 = (523, 285)

    cord21 = (195, 390)
    cord22 = (305, 390)
    cord23 = (418, 390)
    cord24 = (523, 390)

    cord31 = (195, 505)
    cord32 = (305, 505)
    cord33 = (418, 505)
    cord34 = (523, 505)

    cord41 = (195, 615)
    cord42 = (305, 615)
    cord43 = (418, 615)
    cord44 = (523, 615)

    cordArray = [cord11, cord12, cord13, cord14,
                 cord21, cord22, cord23, cord24,
                 cord31, cord32, cord33, cord34,
                 cord41, cord42, cord43, cord44]
    
    cordArray = scale_cords(cordArray)
    
class Values:

# Profile: sRGB IEC61966-2.1
    color_map = {
    # Empty
    "195":0,
    "194":0,
    # 2
    "229":1,
    # 4
    "225":2,
    # 8
    "190":3,
    # 16
    "172":4,
    # 32
    "157":5,
    # 64
    "135":6,
    # 128
    "205":7,
    # 256
    "201":8,
    # 512
    "197":9,
    # 1024
    "193":10,
    # 2048
    "189":11
    }

def getGrid():
    image = ImageGrab.grab()
    grayImage = ImageOps.grayscale(image)
    grayImage.save("last_image.png")
    for index, cord in enumerate(Cords.cordArray):
        pixel = grayImage.getpixel(cord)
        try:
            pos = Values.color_map[str(pixel)]
        except:
            # restart_game()
            time.sleep(1)
            pos = Values.color_map[str(pixel)]
        i = index//4
        j = index % 4
        if pos == 0:
            currentGrid[i][j] = 0
        else:
            currentGrid[i][j] = pow(2, pos)
    return currentGrid
    
def printGrid(grid):
    for t in range(len(grid)):
        print(grid[t])

def performMove(move):
    pyautogui.click(x=65,y=266)
    if move == UP:
        pyautogui.keyDown('up')
        time.sleep(0.05)
        pyautogui.keyUp('up')
    elif move == DOWN:
        pyautogui.keyDown('down')
        time.sleep(0.05)
        pyautogui.keyUp('down')
    elif move == LEFT:
        pyautogui.keyDown('left')
        time.sleep(0.05)
        pyautogui.keyUp('left')
    else:
        pyautogui.keyDown('right')
        time.sleep(0.05)
        pyautogui.keyUp('right')
    # pyautogui.click(x=1200*2,y=850*2)
    pyautogui.PAUSE = 0.01
    time.sleep(0.3)
    
def restart_game():
    time.sleep(1)
    pyautogui.moveTo(x=524,y=205)
    pyautogui.click(x=524,y=205)
    pyautogui.click(x=524,y=205)
    time.sleep(1)
    pyautogui.click(x=1120,y=500)

# def get_score():
#     SCALE_FACTOR = 2

#     left_top = (395 * SCALE_FACTOR, 152 * SCALE_FACTOR)
#     down_right = (482 * SCALE_FACTOR, 176 * SCALE_FACTOR)

#     width = down_right[0] - left_top[0]
#     height = down_right[1] - left_top[1]

#     box = (left_top[0],left_top[1],width,height)
#     im = pyautogui.screenshot(region=box)

#     # im.show()

#     text = pytesseract.image_to_string(im, lang="eng", config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789')
#     score = [int(s) for s in text.split() if s.isdigit()]
#     if len(score) == 0:
#         return None
#     score = score[0]
#     return score


# def get_best_score():
#     SCALE_FACTOR = 2

#     left_top = (493 * SCALE_FACTOR, 152 * SCALE_FACTOR)
#     down_right = (581 * SCALE_FACTOR, 176 * SCALE_FACTOR)

#     width = down_right[0] - left_top[0]
#     height = down_right[1] - left_top[1]

#     box = (left_top[0],left_top[1],width,height)
#     im = pyautogui.screenshot(region=box)
#     im = im.filter(ImageFilter.MedianFilter())
#     enhancer = ImageEnhance.Contrast(im)
#     im = enhancer.enhance(2)
#     im = im.convert('1')
#     im.show()

#     text = pytesseract.image_to_string(im, '--psm 10 --oem 3 --print-parameters -c tessedit_char_whitelist=0123456789')
#     print(text)
#     score = [int(s) for s in text.split() if s.isdigit()]
#     if len(score) == 0:
#         return None
#     score = score[0]
#     return score    

# if __name__ == "__main__":
#     while(True):
#         x = moves_map(random.randint(0,3))
#         print(x)
#         performMove(x)

# def getpixels():
#     image = Image.open("last_image.png")
#     image.show()
    # image = ImageGrab.grab()
    # grayImage = ImageOps.grayscale(image)
    # for index, cord in enumerate(Cords.cordArray):
    #     print(image.getpixel(cord))

# if __name__ == "__main__":
#     getGrid()
#     printGrid(currentGrid)
    # getpixels()
    