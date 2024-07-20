import os
from typing import List
import requests
from bs4 import BeautifulSoup
from typings import Article, Image


# def scrape_article(url):
#     # Fetch the content of the article
#     response = requests.get(url)
#     response.raise_for_status() # Raise an error for bad responses
    
#     # Parse the content with BeautifulSoup
#     soup = BeautifulSoup(response.content, 'html.parser')
    
#     # Extract the main text of the article (modify these selectors based on the website structure)
#     inputTag = soup.findAll("p", {"class": "mol-para-with-font"})

#     text_content = ""
#     for para in inputTag:
#         text_content = text_content + str(para.get_text()) + "\n"
    
#     # remove invalid json characters
#     text_content.replace(r'\x0a', '\n')

#     # Extract the images with captions (modify these selectors based on the website structure)
#     imageTag = soup.findAll("div", {"class": "artSplitter mol-img-group"})
#     images_with_captions = []
#     for paragraphs in imageTag:

#         imgTag = paragraphs.find("div", {"class": "mol-img"}).find("div", {"class": "image-wrap"}).find("img")

#         image_url = imgTag.attrs["data-src"]
#         image_caption = imgTag.attrs["alt"]

#         print(image_url)
#         print(image_caption)

#         images_with_captions.append(Image(image_url, image_caption))
    
#     return Article(text_content, images_with_captions)

import requests
from bs4 import BeautifulSoup

def scrape_article(url):
    try:
        # Make a request to the article URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract article text content
        text_content = ""
        article_text_elements = soup.find_all('p')  # Adjust this based on HTML structure
        for element in article_text_elements:
            text_content += element.get_text() + "\n"

        # Extract images
        images = []
        image_elements = soup.find_all('img')  # Adjust this based on HTML structure
        for img in image_elements:
            image_src = img.get('src')
            images.append({'src': image_src})

        return {'textContent': text_content, 'images': images}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching article from {url}: {e}")
        return None
    except Exception as e:
        print(f"Error parsing article content: {e}")
        return None


def save_images_on_local_folder(images: List[Image]):
    for image in images:
        response = requests.get(image.imageUrl)
        response.raise_for_status() # Raise an error for bad response
        
        image_name = os.path.basename(image.imageUrl)

        with open('article/images/' + image_name, 'wb') as f:
            f.write(response.content)
