from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.remote.webelement import BaseWebElement
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd

PATH = "C:\seleniumdriver\chromedriver.exe"


def crawl_post(url_topic, limit, driver, output_list):
    driver.get(url_topic)
    try:
        url_next_page = driver.find_element(By.XPATH, "//a[@class = 'btn-page active']/following-sibling::a").get_attribute('href')
    except:
        url_next_page = ''

    post = driver.find_elements(By.XPATH,"//article[contains(@class, 'item-news')]/h3[@class = 'title-news']/a")
    link_post = []
    title_posts = []
    for pst in post:
        link_post.append(pst.get_attribute('href'))
        title_posts.append(pst.text)

    if limit > len(link_post):
        iteration = len(link_post)
        limit = limit - len(link_post)
    else:
        iteration = limit
        limit = 1

    for i in range(0, iteration):
        driver.get(link_post[i])
        user_cmt_more = driver.find_elements(By.XPATH, "//p[@class = 'content_more']")
        user_cmt_less = driver.find_elements(By.XPATH, "//p[@class = 'content_less']")
        user_cmt_hidden = driver.find_elements(By.XPATH, "//div[@style = 'display: none;']")

        for cmt in user_cmt_hidden:
            driver.execute_script("arguments[0].removeAttribute('style')", cmt)

        for cmt in user_cmt_more:
            driver.execute_script("arguments[0].style.display = 'block';", cmt)

        for cmt in user_cmt_less:
            driver.execute_script("arguments[0].style.display = 'none';", cmt)

        user_name = driver.find_elements(By.XPATH, "//b")
        user_cmt_short = driver.find_elements(By.XPATH, "//p[@class = 'full_content']")
        user_cmt_long = driver.find_elements(By.XPATH, "//p[@class = 'content_more']")

        arr = []
        for usr in user_name:
            if usr.text == '':
                continue
            for cmt_short in user_cmt_short:
                if cmt_short.text.find(usr.text, 0, len(usr.text)) != -1:
                    arr.append([usr.text, cmt_short.text[len(usr.text):]])
                    break
            for cmt_long in user_cmt_long:
                if cmt_long.text.find(usr.text, 0, len(usr.text)) != -1:
                    arr.append([usr.text, cmt_long.text[len(usr.text):]])
                    break

        dct = {}
        for a in arr:
            dct[a[0]] = a[1]
        output_list[title_posts[i]] = dct

    return limit, url_next_page


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('headless')
driver = webdriver.Chrome(service= Service(PATH), options=options)
driver.maximize_window()
driver.get("https://vnexpress.net")


output_list = {}
all_topic = driver.find_elements(By.XPATH, "//ul[contains(@class,'cat-menu')]")
topic_dict = {}
for idx,topic in enumerate(all_topic):
    li = topic.find_elements(By.XPATH, "li")
    a = li[0].find_element(By.TAG_NAME, "a")

    topic_title = a.get_attribute('title')
    topic_href = a.get_attribute('href')

    if topic_title not in ['Video', 'Podcasts']:
        topic_dict[idx] = [topic_title,topic_href]

# bo di topic video va podcast


for key, value in topic_dict.items():
    print(f"{key}: {value[0]}")

topic = int(input("choose a topic: "))
url_topic = topic_dict[topic][1]
print(url_topic)
limit = int(input("limit post: "))

while limit > 1:
    limit, url_next_page = crawl_post(url_topic, limit, driver, output_list)
    if limit > 1:
        url_topic = url_next_page

for key, value in output_list.items():
    print(f"Post title: {key}")
    # print("Post comments: ")
    # for k, v in value.items():
    #     print(f"User: {k}")
    #     print(f"Comment: {v}")
    # print(" ")

    df = pd.DataFrame(value.items(), columns=['userName','userComment'])
    print(df)