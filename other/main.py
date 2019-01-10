# import pyautogui
# print(pyautogui.displayMousePosition())


from pytesseract import image_to_string
import pytesseract

import pyautogui



def get_score():
    SCALE_FACTOR = 2

    left_top = (395 * SCALE_FACTOR, 152 * SCALE_FACTOR)
    down_right = (482 * SCALE_FACTOR, 176 * SCALE_FACTOR)

    width = down_right[0] - left_top[0]
    height = down_right[1] - left_top[1]

    box = (left_top[0],left_top[1],width,height)
    im = pyautogui.screenshot(region=box)

    # im.show()

    text = pytesseract.image_to_string(im, lang="eng", config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789')
    score = [int(s) for s in text.split() if s.isdigit()]
    if len(score) == 0:
        return None
    score = score[0]
    return score

def get_best_score():
    SCALE_FACTOR = 2

    left_top = (493 * SCALE_FACTOR, 152 * SCALE_FACTOR)
    down_right = (581 * SCALE_FACTOR, 176 * SCALE_FACTOR)

    width = down_right[0] - left_top[0]
    height = down_right[1] - left_top[1]

    box = (left_top[0],left_top[1],width,height)
    im = pyautogui.screenshot(region=box)

    # im.show()

    text = pytesseract.image_to_string(im, lang="eng", config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789')
    score = [int(s) for s in text.split() if s.isdigit()]
    if len(score) == 0:
        return None
    score = score[0]
    return score

# print(get_best_score())

print(get_best_score())