import numpy as np
import pickle
import streamlit as st
from PIL import Image
from CrawlerPaper import PaperCrawl 
from ImageCrawler import ImageCrawl
from paginator import paginator
from NewsCrawler import crawl_post, Crawl
#news
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

# PATH = "chromedriver.exe"
# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(service= Service(PATH), options=options)
# driver.maximize_window()
# driver.get("https://vnexpress.net")

st.title('CS232 | CRAWLER MODULES')
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 350px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 350px;
        margin-left: -350px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.sidebar.title('Workspace - Options')
st.sidebar.subheader('Parameters')



app_mode = st.sidebar.selectbox('Choose the App mode',
                                ['General information',
                                    'Paper Crawler', "Image Crawler", "News Crawler"]
                                )

if app_mode == 'General information':
    background = Image.open('./assests/download.jpg')
    if background is not None:
        background = background.resize((700, 150))
        st.image(background)
    st.markdown("**A web crawler**, crawler or web spider, is a computer program that's used to search and automatically index website content and other information over the internet")

    st.markdown(
        """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    
    
    # image_profile = np.array(Image.open(AVATAR))
    # scale_percent = 200 # percent of original size
    # width_pro= int(image_profile.shape[1] * scale_percent / 100)
    # height_pro = int(image_profile.shape[0] * scale_percent / 100)
    # dim = (width_pro, height_pro)
    # resized_pro = cv2.resize(image_profile, dim, interpolation = cv2.INTER_AREA)
    # st.image(resized_pro)

    st.markdown('''
          # ABOUT US \n 
           Let's call this web **Crawler implementation**. There are a plenty of features that this web can operate.\n
            
            Here are our fantastic features:
            - Paper Crawler
            - Image Crawler
            - Facebook comment Crawler
            - Newspaper comment Crawler
        
            Since this is just one sample, it would be better if we have more time to continue with our work. Promisingly, the next version would surely be well-structured and effective. \n
            We would implement more features in the next versions, feel free to contact and collaberate with us
            ''')
    
elif app_mode == 'Paper Crawler':

    st.sidebar.markdown('---')

    background_paper = Image.open('./assests/crawlpaper.jpg')
    if background_paper is not None:
        background_paper = background_paper.resize((700, 150))
        st.image(background_paper)

    st.markdown(
    """
    # Crawl papers 
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

    
    author_name = st.text_input('Input the author name')
    number_paper = st.text_input("Input the number of page ")
    crawl = st.button('crawl')

    df = pd.DataFrame()
    if crawl:
        paper_dataframe = PaperCrawl(author_name,int(number_paper))
        st.write(paper_dataframe)
        df = paper_dataframe
    

    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(index=None).encode('utf-8')

    csv = convert_df(df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )
        
elif app_mode == 'Image Crawler':

    st.sidebar.markdown('---')

    background_search = Image.open('./assests/search_img.jpg')
    if background_search is not None:
        background_search = background_search.resize((700, 150))
        st.image(background_search)
    st.markdown(
    """
    # Image Crawler
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

    
    query = st.text_input('Input the image query')
    number_images = st.text_input("Input the number of images ")
    crawl = st.button('crawl')
    images = []
    if crawl:
        image_path = ImageCrawl(query,int(number_images))
        image_iterator = paginator("Select a sunset page", image_path)
        indices_on_page, images_on_page = map(list, zip(*image_iterator))
        st.image(images_on_page, width=100, caption=indices_on_page)

        images = images_on_page

    btn = st.download_button(
            label="Download image",
            data="",
            file_name="flower.png",
            mime="image/png"
          )
elif app_mode == 'News Crawler':

    st.sidebar.markdown('---')

    background_news = Image.open('./assests/news.jpg')
    if background_news is not None:
        background_news = background_news.resize((700, 150))
        st.image(background_news)
    st.markdown(
    """
    # News Crawler 
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


    topic_dict, output_list = Crawl()
    df_final = pd.DataFrame()
    if topic_dict: 
        topic = st.text_input("Choose a topic: ")
        limit = st.text_input("Enter limit post: ")
        crawl = st.button("crawl")
        if topic != "" and limit !="" and crawl: 
            topic = int(topic)
            limit = int(limit)
            url_topic = topic_dict[topic][1]
            print(url_topic)
            while limit > 1:
                limit, url_next_page = crawl_post(url_topic, limit, output_list)
                if limit > 1:
                    url_topic = url_next_page

            for key, value in output_list.items():
                df = pd.DataFrame(value.items(), columns=['user Name','user Comment'])
                st.text(f'Post title: {key}')
                st.write(df)
                df_final = df_final.append(df)

    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(index=None).encode('utf-8')

    csv = convert_df(df_final)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )
            

        