from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

PATH = "chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('headless') #do not open the browser
driver = webdriver.Chrome(service= Service(PATH), options=options)
driver.maximize_window()
driver.get("https://vnexpress.net")

def crawl_post(url_topic, limit,output_dict):
    driver.get(url_topic)

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

        user_name = driver.find_elements(By.XPATH, "//span[@class = 'txt-name']")
        user_cmt_short = driver.find_elements(By.XPATH, "//p[@class = 'full_content']")
        user_cmt_long = driver.find_elements(By.XPATH, "//p[@class = 'content_more']")

        cmt_dict = {}
        if len(user_name) == 0:
            output_dict[title_posts[i]] = "this post has 0 comment"

        else:
            for usr in user_name:
                for cmt_short in user_cmt_short:
                    if cmt_short.text.find(usr.text, 0, len(usr.text)) != -1:
                        cmt_dict[usr.text] = cmt_short.text[len(usr.text):]
                        break
                for cmt_long in user_cmt_long:
                    if cmt_long.text.find(usr.text, 0, len(usr.text)) != -1:
                        cmt_dict[usr.text] = cmt_long.text[len(usr.text):]
                        break
            output_dict[title_posts[i]] = cmt_dict

    return limit

def TopicList():
    all_topic = driver.find_elements(By.XPATH, "//ul[contains(@class,'cat-menu')]")
    topic_dict = {}
    for topic in all_topic:
        li = topic.find_elements(By.XPATH, "li")
        a = li[0].find_element(By.TAG_NAME, "a")

        topic_title = a.get_attribute('title')
        topic_href = a.get_attribute('href')

        if topic_title not in ['Video', 'Podcasts']:
            topic_dict[topic_title] = topic_href
    
    return topic_dict
    # return topic_dict[topic]


def CrawlNewsWebsite(topic,limit):
    output_dict = {}
    topic_dict = TopicList()
    url_topic = topic_dict[topic]
    while limit > 1:
        limit = crawl_post(url_topic, limit, output_dict)
        if limit > 1:
            try:
                url_next_page = driver.find_element(By.XPATH, "//a[@class = 'btn-page active']/following-sibling::a").get_attribute('href')
            except:
                return output_dict
            else:
                url_topic = url_next_page
    return output_dict



