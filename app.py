import numpy as np
import pickle
import streamlit as st
from PIL import Image
from CrawlerPaper import PaperCrawl 
from ImageCrawler import ImageCrawl
from paginator import paginator
import pandas as pd
from FacebookCrawler import crawlFB
from NewsCrawler import CrawlNewsWebsite

st.title('CS115 | CRAWLER MODULES')
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
                                    'Paper Crawler', "Image Crawler", "News Crawler", "Facebook Crawler"]
                                )

if app_mode == 'General information':
    st.markdown("**Support Vector Machine (SVM)** is one of the most popular Machine Learning Classifier. It falls under the category of Supervised learning algorithms and uses the concept of Margin to classify between classes.")

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
           Let's call this web **SVM IN PRACTISE**. There are a plenty of features that this web can operate.\n
            
            Here are our fantastic features:
            - Image Classification 
        
            Since this is just one sample, it would be better if we have more time to continue with our work. Promisingly, the next version would surely be well-structured and effective. \n
            We would implement more features in the next versions, feel free to contact and collaberate with us
            ''')
    
elif app_mode == 'Paper Crawler':

    st.sidebar.markdown('---')

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
    if crawl:
        paper_dataframe = PaperCrawl(author_name,int(number_paper))
        st.write(paper_dataframe)
        
elif app_mode == 'Image Crawler': #fix storing locally

    st.sidebar.markdown('---')

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
    if crawl:
        image_path = ImageCrawl(query,int(number_images))
        image_iterator = paginator("Select a sunset page", image_path)
        indices_on_page, images_on_page = map(list, zip(*image_iterator))
        st.image(images_on_page, width=100, caption=indices_on_page)

elif app_mode == 'News Crawler':

    st.sidebar.markdown('---')

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
                
    topic = st.text_input("Choose a topic: ")
    limit = st.text_input("Enter limit post: ")
    start_crawl = st.button("crawl")
    if topic and limit and start_crawl:
        result = CrawlNewsWebsite(topic,int(limit))
        print(result)
        for key, value in result.items():
            if isinstance(value, dict):
                df = pd.DataFrame(value.items(), columns=['user Name','user Comment'])
                st.text(f'Post title: {key}')
                st.write(df)
                
            else:
                st.text(f'Post title: {key}')
                st.text("This post has no comment")
               
                
elif app_mode == 'Facebook Crawler':

    st.sidebar.markdown('---')

    st.markdown(
    """
    # Facebook Crawler 
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

    limit_post = st.text_input("Enter the number of posts")
    start_crawl = st.button("crawl")
    if limit_post and start_crawl:
        result = crawlFB(int(limit_post))
        for key, value in result.items():
            st.text(f"The content post: {key}")
            if isinstance(value, dict):
                df = pd.DataFrame(value.items(), columns=['userName', 'userComment'])
                st.write(df)
            else:
                st.text('this post has 0 comment')
    
  

        