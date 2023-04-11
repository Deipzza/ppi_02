import time
import requests

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions

db = 'allunbot.db'

def auth(payload):
    """ """

    # create session
    session = requests.Session()
    url = 'https://sia.unal.edu.co/ServiciosApp'    

    # get log in page
    auth_page = session.get(url)
    soup = BeautifulSoup(auth_page.content, 'html.parser')

    # get form
    form = soup.find('form')
    post_url = form['action']

    # auth
    session.post(post_url, data=payload)

    # parse content
    content_url = 'https://sia.unal.edu.co/ServiciosApp'
    page = session.get(content_url)
    page_soup = BeautifulSoup(page.content, 'html5lib')
    print(page_soup)

    try:
        user_loggen = page_soup.find('a', {'class': 'af_menu_bar-item-text'}).text
        return (user_loggen == payload["username"], session)
    except:
        return (False, None)

def login(payload) -> webdriver.Chrome:
    """Authenticates the student with its credentials.
    """
    options = ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://sia.unal.edu.co/ServiciosApp")

    user_input = driver.find_element(by=By.XPATH, value="//input[@id='username']")
    password_input = driver.find_element(by=By.XPATH, value="//input[@id='password']")
    login_button = driver.find_element(by=By.XPATH, value="//input[@name='submit']")

    user_input.send_keys(payload["username"])
    password_input.send_keys(payload["password"])

    login_button.click()

    del user_input
    del password_input
    del login_button

    driver.implicitly_wait(5)

    return driver
