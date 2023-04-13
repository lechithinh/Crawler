import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PATH = "chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('headless') #do not open the browser
driver = webdriver.Chrome(service= Service(PATH), options=options)
driver.maximize_window()
driver.get("https://www.facebook.com/UIT.Fanpage")


POST_CONTAINER_PATH = "//div[@class = 'x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z']"
BUTTON_SHOWMORE_PATH = "//div[text() = 'See more']"
POST_PATH = "//div[@data-ad-preview='message']"
BUTTON_MOSTREL_PATH = "//span[text() = 'Most relevant']/ancestor::div[contains(@class,'x1i10hfl xjbqb8w')]"
BUTTON_SHOWALLCMT_PATH = "//span[text() = 'All comments']"
BUTTON_CMTVIEWMORE_PATH = "//span[contains(text(),'View')]/ancestor::div[contains(@class,'x1i10hfl xjbqb8w')]"
USER_NAME_PATH = "//span[@class = 'x3nfvp2']//span"
USER_CMT_PATH = "//div[@dir='auto']"


def crawl_post(idx, num_post,output_dict):
    for i in range(idx, num_post + 1):
        container_path = f"//div[@aria-posinset = '{i}']"
        try:
            button = driver.find_element(By.XPATH, "{}{}".format(container_path,BUTTON_SHOWMORE_PATH))
        except:
            pass
        else:
            driver.execute_script('arguments[0].click()', button)



        posts = driver.find_element(By.XPATH, "{}{}".format(container_path, POST_PATH))
        posts_text = posts.text

        most_rel = driver.find_elements(By.XPATH, "{}{}".format(container_path, BUTTON_MOSTREL_PATH))
        for btn in most_rel:
            driver.execute_script('arguments[0].click()', btn)
        show_all_cmt = driver.find_elements(By.XPATH, "{}{}".format(container_path, BUTTON_SHOWALLCMT_PATH))

        for btn in show_all_cmt:
            driver.execute_script('arguments[0].click()', btn)

        cmt_view_more = driver.find_elements(By.XPATH, "{}{}".format(container_path, BUTTON_CMTVIEWMORE_PATH))
        for cmt in cmt_view_more:
            driver.execute_script('arguments[0].click()', cmt)

        time.sleep(3)
        post_dict = {}

        try:
            cmt_user_name = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.XPATH, "{}{}".format(container_path, USER_NAME_PATH)))
                )
        except:
            output_dict[posts_text] = "no comment"
        else:
            for name in cmt_user_name:
                name_val = name.text

                try:
                    cmt_user_cmt = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,"{}//div[contains(@aria-label,'Comment by {}')]{}".format(container_path,name.text,USER_CMT_PATH))))
                except:
                    post_dict[name_val] = 'cmt khong phai dang text'
                else:
                    cmt_val = cmt_user_cmt.text
                    if cmt_val == ' ':
                        post_dict[name_val] = 'cmt khong phai dang text'
                    post_dict[name_val] = cmt_val

            output_dict[posts_text] = post_dict

def crawlFB(limit):
    output_dict = {}
    num_post = 0
    while limit:
        timeout = time.time() + 0.25
        while True:
            while True:
                driver.execute_script("window.scrollTo(0, window.scrollY + 20);")
                if time.time() > timeout:
                    break
            post_container = driver.find_elements(By.XPATH,"//div[@aria-posinset]")
            if len(post_container) >= (5 + num_post):
                break
        time.sleep(3)

        if limit > 5:
            idx = num_post + 1
            num_post = num_post + 5
            limit = limit - 5
        else:
            idx = num_post + 1
            num_post = num_post + limit
            limit = 0
        crawl_post(idx,num_post,output_dict)

    return output_dict






















