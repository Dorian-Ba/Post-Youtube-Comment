from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import sys

from random import randint, uniform
from credentials import email,email_password

def delay(n):
    time.sleep(randint(3, n))


def delay_mini(n):
    time.sleep(uniform(0.1, n))

def write_comment(nb_video):
    profile = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(firefox_profile=profile, executable_path=r'C:\Users\dorian\Desktop\geckodriver.exe')

    driver.get("https://www.youtube.com")
    print("enter " + driver.title)
    delay(5)

    # click SIGN IN button
    item = driver.find_element_by_css_selector("ytd-masthead div#buttons ytd-button-renderer a")
    item.click()
    delay(5)

    # login google account
    driver.find_element_by_id("identifierId").send_keys(email)
    driver.find_element_by_id("identifierNext").click()
    delay(5)

    password_locator = (By.CSS_SELECTOR, 'div#password input[name="password"]')
    WebDriverWait(driver, 10).until(
        expect.presence_of_element_located(password_locator)
    )
    password = driver.find_element(*password_locator)
    WebDriverWait(driver, 10).until(
        expect.element_to_be_clickable(password_locator)
    )
    password.send_keys(email_password)
    driver.find_element_by_id("passwordNext").click()
    delay(5)

    print("wait for login ...")
    WebDriverWait(driver, 300).until(
        expect.presence_of_element_located((By.CSS_SELECTOR, "ytd-masthead button#avatar-btn"))
    )
    print("login ok")

    file = open('video_pos.txt', 'r')
    pos_from=int(file.readline())
    file.close()

    file = open('video_pos.txt', 'w')
    pos_to = pos_from+nb_video
    file.write(str(pos_to))
    file.close()

    file_id = open('video_id.txt', 'r')
    error_log_file = open('error_logs.txt', 'w')
    log_file = open('logs.txt', 'w')


    for pos,idyoutube in enumerate(file_id):
        if pos<pos_from:
            continue
        if pos>=pos_to:
            break

        driver.get("https://www.youtube.com/watch?v="+idyoutube)
        delay(5)

        # scroll to the bottom in order to load the comments
        for i in range(10, 1000, 50):
            delay_mini(1)
            driver.execute_script("window.scrollTo(0, {});".format(i))
        try:
            print("wait for comments to load ...")
            WebDriverWait(driver, 10).until(
                expect.presence_of_element_located((By.CSS_SELECTOR, "ytd-comments ytd-comment-simplebox-renderer"))
            )

            box = WebDriverWait(driver, 10).until(expect.presence_of_element_located((By.ID, "simplebox-placeholder")))
            box.click()
            box = WebDriverWait(driver, 10).until(expect.presence_of_element_located((By.ID, "contenteditable-root")))
            box.send_keys("I have been using this trading robot and I have a very good profit\n")
            box.send_keys("Here is a demo: https://www.youtube.com/watch?v=GgX0ADjLxok&t\n")
            box.send_keys("I bought this EA in MQL market:https://www.mql5.com/en/market/product/24726 \n")
            box.send_keys(Keys.CONTROL, Keys.ENTER)
        except TimeoutException as inst:
            error_log_file.write('TimeoutException for the id {} \n'.format(idyoutube))
            log_file.write('{} is ko \n'.format(idyoutube))
            print('{} is ko \n'.format(idyoutube))
        except Exception as inst:
            message=str(inst)[:-1]
            error_log_file.write('{} for the id {} \n'.format(message,idyoutube))
            log_file.write('{} is ko \n'.format(idyoutube))
            print('{} is ko \n'.format(idyoutube))
        else:
            log_file.write('{} is ok \n'.format(idyoutube))
            print('{} is ok \n'.format(idyoutube))

    file_id.close()
    error_log_file.close()
    log_file.close()
write_comment(10)