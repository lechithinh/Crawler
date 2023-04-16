import numpy as np
import pickle
import streamlit as st
from PIL import Image
from CrawlerPaper import PaperCrawl 
from paginator import paginator
import pandas as pd
from FacebookCrawler import crawlFB
from NewsCrawler import CrawlNewsWebsite, TopicList
from ImageCrawler import ImageCrawl

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

def convert_df(df):
    return df.to_csv(index=None).encode('utf-8')

app_mode = st.sidebar.selectbox('Choose the App mode',
                                ['General information',
                                    'Paper Crawler', "Image Crawler", "News Crawler", "Facebook Crawler"]
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
        
    csv = convert_df(df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )

elif app_mode == 'Image Crawler': #fix storing locally

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
    Image_Folder = st.text_input('Input download path (optional)')
    crawl = st.button('crawl') 
    download = st.checkbox('download')
    if crawl:
        image_path, imagelinks, image_content = ImageCrawl(query,int(number_images),Image_Folder, download)
        image_iterator = paginator("Select a sunset page", imagelinks)
        indices_on_page, images_on_page = map(list, zip(*image_iterator))
        st.image(images_on_page, width=150, caption=indices_on_page)   
        if download:
            for i in range(len(image_path)):
                with open(image_path[i], 'wb') as file:
                    file.write(image_content[i])


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

    topic_lst = st.text("Topic list: ")
    topic_dict = TopicList()
    len_dict = len(topic_dict)
    topic_arr = []
    for idx,topic in topic_dict.items():
        topic_arr.append([topic[0]])
    df = pd.DataFrame(np.array(topic_arr),index=range(1,len_dict+1),columns=['Topic'])
    st.dataframe(df.T)        

    topic = st.number_input(f"Choose a topic (1 to {len_dict}): ",format="%i",min_value=1,max_value=len_dict,step=1)
    limit = st.text_input("Enter limit post: ")
    start_crawl = st.button("crawl")

    df_final = pd.DataFrame()
    if topic and limit and start_crawl:
        result = CrawlNewsWebsite(topic,int(limit))
        # print(result)
        for key, value in result.items():
            if isinstance(value, dict):
                df = pd.DataFrame(value.items(), columns=['user Name','user Comment'])
                st.text(f'Post title: {key}')
                st.write(df)
                df_final = df_final.append(df)
                
            else:
                st.text(f'Post title: {key}')
                st.text("This post has no comment")
                            
    csv = convert_df(df_final)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )
                
elif app_mode == 'Facebook Crawler':

    st.sidebar.markdown('---')

    background_facebook = Image.open('./assests/facebook_img.png')
    if background_facebook is not None:
        background_facebook = background_facebook.resize((700, 150))
        st.image(background_facebook)

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
    

    df_down = pd.DataFrame()
    url = st.text_input("Enter the url of a facebook page")
    if url:
        try:
            if url.startswith("https://www.facebook.com/groups"):
                st.write('Invalid URL')
            elif url.startswith("https://www.facebook.com/"):
                st.write('Valid URL')
            else:
                st.write('Invalid URL')
        except ValueError:
            st.write('Invalid URL')
    limit_post = st.text_input("Enter the number of posts")
    start_crawl = st.button("crawl")
    result = {}
    if limit_post and start_crawl:
        result = crawlFB(int(limit_post),url)
        for key, value in result.items():
            st.text(f"The content post: {key}") 
            if isinstance(value, dict):
                df = pd.DataFrame(value.items(), columns=['userName', 'userComment'])
                st.write(df) 
                df_down = df_down.append(df)
            else:
                st.text('this post has 0 comment') 
        result.clear()



    csv = convert_df(df_down)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )
  

        