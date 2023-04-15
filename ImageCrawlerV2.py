import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import urllib.request

PATH = "C:\seleniumdriver\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('headless')
driver = webdriver.Chrome(service= Service(PATH), options=options)
driver.maximize_window()

URL_IMAGE = "https://www.google.com/search?tbm=isch&q="
IMAGE_PATH = "//img[@class = 'rg_i Q4LuWd']"

def ImageCrawl(query, num_images):    
    Image_Folder = query.replace(' ', '') + "Image"
    
    #Store Image
    if not os.path.exists(Image_Folder):
        os.mkdir(Image_Folder)
    return download_images(query,num_images,Image_Folder)


def download_images(query,num_images,Image_Folder):    
    query = query.replace(' ',"+")
    FULL_URL = URL_IMAGE + query
    driver.get(FULL_URL)

    while True:
        image = driver.find_elements(By.XPATH,IMAGE_PATH)
        if len(image) < num_images:
            driver.execute_script("window.scrollTo(0, window.scrollY + 50);")
        else:
            break
    
    image_path = []
    for idx,img in enumerate(image):
        if idx > num_images-1:
            break
        imagename = Image_Folder + '/' + f'img{idx+1}.png'

        image_path.append(imagename)
        urllib.request.urlretrieve(img.get_attribute('src'),imagename)
    return image_path

