import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

# CONVERT THE DATA INTO JSON
def dataToJson(title, img_url, news_link):
    return {
        "title" : title,
        "img_url" : img_url,
        "news_link" : news_link,
    }

def getAryData(item):
    title = item.find(class_="entry-title").text
    img_url = item.find(class_="entry-thumb").get('data-img-url')
    news_link = item.find(class_="entry-title").find("a").get('href')
    return dataToJson(title, img_url, news_link)

def getBolData(item):
    title = item.find(class_="title").text
    img_url = item.find("img").get("src")
    news_link = item.find("a").get("href")
    return dataToJson(title, img_url, news_link)
    
def getSammaData(item):
    title = item.find(class_="story__link").text
    img_url = item.find('img').get("src")
    news_link = item.find(class_="story__link").get("href")
    return dataToJson(title, img_url, news_link)

def getDunyaData(item):
    title = item.find(class_="card-title").text
    img_url = item.find('img').get("src")
    news_link = item.find('a').get("href")
    return dataToJson(title, img_url, news_link)

CHANNELS = {
    "ary" : {
        "url" : "https://arynews.tv/",
        "class" : "td-module-container",
        "func" : getAryData
    },
    "bol" : {
        "url" : "https://www.bolnews.com/",
        "class" : "post-box",
        "func" : getBolData
    },
    "samma" : {
        "url" : "https://www.samaa.tv/",
        "class" : "story",
        "func" : getSammaData
    },
    "dunya" : {
        "url" : "https://dunya.com.pk/index.php",
        "class" : "card",
        "func" : getDunyaData
    },
}

def getNewsData(channel_name):
    channel = CHANNELS[channel_name]
    response = requests.get(channel["url"], headers=HEADERS)
    soup =  BeautifulSoup(response.text, 'html.parser')
    all_news = []
    news_items_list = soup.find_all(class_= channel["class"])
    for item in news_items_list:
        try:
            all_news.append(channel["func"](item))
        except :
            print("error")

    return all_news

def getAllChannelsNews():
    allNews = {}
    for channel in CHANNELS.keys():
        allNews[channel] = getNewsData(channel)
    
    return allNews
    
if __name__ == "__main__":
    getAllChannelsNews()