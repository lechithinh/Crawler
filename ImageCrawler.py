import os
import requests 
from bs4 import BeautifulSoup 
import numpy as np
from PIL import Image
import base64
import io

Google_Image = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7',
    'Connection': 'keep-alive',
} 



def ImageCrawl(query, num_images):    
    Image_Folder = query.replace(' ', '') + "Image"
    
    #Store Image
    if not os.path.exists(Image_Folder):
        os.mkdir(Image_Folder)
    return download_images(query,num_images,Image_Folder)
    

def download_images(query,num_images,Image_Folder):    
    search_url = Google_Image + 'q=' + query 
    response = requests.get(search_url, headers=headers)
    html = response.text 
    b_soup = BeautifulSoup(html, 'html.parser') 
    results = b_soup.findAll('img', {'class': 'rg_i Q4LuWd'})

    count = 0
    imagelinks= []
    for res in results:
        try:
            link = res['data-src']
            imagelinks.append(link)
            count = count + 1
            if (count >= num_images):
                break
            
        except KeyError:
            continue
            

    image_path = []
    for i, imagelink in enumerate(imagelinks):
        # open each image link and save the file
        response = requests.get(imagelink)
        imagename = Image_Folder + '/' + query.replace(' ', '') + str(i+1) + '.jpg'
        image_path.append(imagename)
        with open(imagename, 'wb') as file:
            file.write(response.content)
    print('Download Completed!')
    return image_path
    
