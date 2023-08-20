import requests
from bs4 import BeautifulSoup
import json

class Article:
    def __init__(self, textContent, images):
        self.textContent = textContent
        self.images = images

class Image:
    def __init__(self, imageUrl, caption):
        self.imageUrl = imageUrl
        self.caption = caption

class ArticleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Article):
            return {
                'textContent': obj.textContent,
                'images': [
                    {'imageUrl': image.imageUrl, 'caption': image.caption}
                    for image in obj.images
                ]
            }
        return super().default(obj)



def scrape_article(url):
    # Fetch the content of the article
    response = requests.get(url)
    response.raise_for_status() # Raise an error for bad responses
    
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the main text of the article (modify these selectors based on the website structure)
    inputTag = soup.findAll("p", {"class": "mol-para-with-font"})

    text_content = ""
    for para in inputTag:
        text_content = text_content + str(para.get_text()) + "\n"
    
    # remove invalid json characters
    text_content.replace(r'\x0a', '\n')

    # Extract the images with captions (modify these selectors based on the website structure)
    imageTag = soup.findAll("div", {"class": "artSplitter mol-img-group"})
    images_with_captions = []
    for paragraphs in imageTag:

        imgTag = paragraphs.find("div", {"class": "mol-img"}).find("div", {"class": "image-wrap"}).find("img")

        image_url = imgTag.attrs["data-src"]
        image_caption = imgTag.attrs["alt"]

        print(image_url)
        print(image_caption)

        images_with_captions.append(Image(image_url, image_caption))
    
    return Article(text_content, images_with_captions)