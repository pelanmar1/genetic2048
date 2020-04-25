from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary



driver = webdriver.Chrome("/Users/pelanmar1/Coding/Python/Selenium/chromedriver")

# driver = webdriver.Firefox(executable_path=r"/Users/pelanmar1/Coding/Python/Selenium/geckodriver")
driver.get("http://2048game.com/")
wait = WebDriverWait(driver, 10)

# Load scripts
r = driver.execute_script(open("/Users/pelanmar1/Coding/Python/Genetic2048/genetic_2048/sel/funcs.js").read())
print(r)
print('SPLIT SCREEN WITH GAME ON THE LEFT AND PRESS ENTER TO BEGIN')
pause = input('') #This will wait until you press enter before it continues with the program
print('STARTING TRAINING')


def get_grid():
    grid = driver.execute_script("return getGrid();")
    return grid

def get_score():
    score = driver.execute_script("return getScore();")
    return score

def get_best_score():
    best_score = driver.execute_script("return getBestScore();")
    return best_score

#driver.close()