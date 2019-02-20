from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys



driver = webdriver.Chrome("/Users/pelanmar1/Coding/Python/Genetic2048/genetic_2048/sel/chromedriver")
driver.get("http://2048game.com/")
wait = WebDriverWait(driver, 5)

# Load scripts
driver.execute_script(open("/Users/pelanmar1/Coding/Python/Genetic2048/genetic_2048/sel/funcs.js").read())

print('SPLIT SCREEN WITH GAME ON THE LEFT AND PRESS ENTER TO BEGIN')
pause = input('') #This will wait until you press enter before it continues with the program
print('STARTING TRAINING')


def get_grid():
    grid = driver.execute_script("return getGrid();")
    return grid

def get_score():
    score = driver.execute_script("return getScore();")
    return score
    

#driver.close()