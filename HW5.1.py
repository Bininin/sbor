# Написать программу, которая собирает товары «В тренде»
# с сайта техники mvideo и складывает данные в БД.
# Сайт можно выбрать и свой.
# Главный критерий выбора: динамически загружаемые товары

import time
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as DKE
from pprint import pprint
from selenium.webdriver.support.ui import WebDriverWait

client = MongoClient("localhost", 27017)
db = client["mvideo"]
mvideo_collection = db.mvideo_collection


s = Service('./chromedriver')
driver = webdriver.Chrome(service=s)
driver.maximize_window()

driver.get('https://www.mvideo.ru')


driver.execute_script("window.scrollTo(0, 1500);")
driver.implicitly_wait(15)
try:
    driver.find_element(By.XPATH,"//span[contains(text(), 'В тренде')]").click()

except exceptions.NoSuchElementException:
    print("Doesn't exist")

while True:
    try:
        button = driver.find_elements(By.XPATH, "//mvid-shelf-group/*//button[contains(@class,'btn forward')]/mvid-icon[@type = 'chevron_right']")
        button[1].click()
        time.sleep(2)
    except exceptions.ElementNotInteractableException:
        break

items = driver.find_elements(By.XPATH, "//mvid-shelf-group//mvid-product-cards-group//div[@class='title']")

items_list = []
for item in items:
    item_info = {}
    item_link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
    item_title = item.find_element(By.TAG_NAME, "a").text
    item_info['Title'] = item_title
    item_info['Link'] = item_link

    items_list.append(item_info)

    try:
        mvideo_collection.insert_one(item_info)
        mvideo_collection.create_index('Link', unique=True)
    except DKE:
        print(f'{item_title} is already exist')

pprint(items_list)
print(len(items_list))