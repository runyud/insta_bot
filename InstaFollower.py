import os
import random
import time

from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

SIMILAR_ACCOUNT = "leomessi"
USERNAME = os.getenv("INSTA_USER")
PASSWORD = os.getenv("INSTA_PASSWORD")


class InstaFollower:

    def __init__(self):
        chrome_driver_path = ChromeDriverManager().install()  # Install the chromedriver executable local to your project

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)  # Keeps the browser open when the script finishes

        service = ChromeService(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def login(self):
        insta_login_url = "https://www.instagram.com/accounts/login/"
        self.driver.get(insta_login_url)
        # user_name = self.driver.find_element(By.NAME, "username")
        time.sleep(5)
        user_name = self.driver.find_element(By.CSS_SELECTOR, '#loginForm > div > div:nth-child(1) > div > label > '
                                                              'input')
        user_name.click()
        user_name.send_keys(USERNAME)
        # password = self.driver.find_element(By.NAME, "password")
        time.sleep(2)
        password = self.driver.find_element(By.CSS_SELECTOR,
                                            '#loginForm > div > div:nth-child(2) > div > label > input')
        password.click()
        password.send_keys(PASSWORD)
        password.send_keys(Keys.ENTER)

    def find_follower(self):
        time.sleep(10)
        target_url = f"https://www.instagram.com/{SIMILAR_ACCOUNT}/"
        self.driver.get(target_url)
        time.sleep(10)
        followers_url = f"https://www.instagram.com/{SIMILAR_ACCOUNT}/followers/"
        self.driver.get(followers_url)
        time.sleep(10)

        # To access the followers pop-up.
        f_body = self.driver.find_element(By.XPATH, "//div[@class='_aano']")

        # To scroll down thrice in the followers pop-up.
        for i in range(3):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", f_body)
            time.sleep(10)

    def follow(self):
        while True:
            try:
                list_of_people = self.driver.find_elements(By.CSS_SELECTOR, 'button')
                print(len(list_of_people))
                for person in list_of_people:
                    print(person.text)
                    if person.text == "Follow":
                        time.sleep(random.randint(5, 10))
                        self.driver.execute_script("arguments[0].click();", person)
                        time.sleep(random.randint(5, 10))
                    print(len(list_of_people))
                print('Scrolling...')

                fBody = self.driver.find_element(By.XPATH, "//div[@class='_aano']")
                scroll = 0
                while scroll < 5:  # scroll 5 times, feel free to change this
                    self.driver.execute_script(
                        'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
                    time.sleep(2)
                    scroll += 1

            except ElementClickInterceptedException as e:
                cancel_button = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[3]/button[2]')
                cancel_button.click()

        print("Bot Successful !")
