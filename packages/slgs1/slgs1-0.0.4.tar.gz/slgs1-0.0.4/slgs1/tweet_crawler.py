import time
import datetime
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import os

driver = webdriver.Chrome('chromedriver')
driver.implicitly_wait(10)

def connent_url(UrlPath):
    Data_List = []
    print(os.getcwd())
    df = pd.read_csv(UrlPath)

    i = 1
    for url in df:
        driver.get(url=url)
        js = 'window.scrollBy(0, 1000)'
        js1 = 'return document.body.scrollHeight'
        try:
            page = 0
            for y in range(20):
                driver.execute_script(js)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                divs = soup.find_all(
                    'div', {'class': "css-1dbjc4n r-1igl3o0 r-qklmqi r-1adg3ll r-1ny4l3l"})
                page += 1
                print('------------------Fetching data on page {}！！---------------------'.format(page))
                for i, div in enumerate(divs):
                    data_list = []
                    name = div.find(
                        'div', {'class': 'css-901oao r-1awozwy r-1nao33i r-6koalj r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-bcqeeo r-1udh08x r-3s2u2q r-qvutc0'})
                    if name:
                        print('第' + str(i) + '个name: ' + name.get_text())
                        data_list.append(name.get_text())
                    else:
                        break
                    user_name = div.find(
                        'div', {'class': 'css-901oao css-1hf3ou5 r-1bwzh9t r-18u37iz r-37j5jr r-1wvb978 r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0'})
                    if user_name:
                        print('第' + str(i) + '个username: ' + user_name.get_text())
                        data_list.append(user_name.get_text())
                    else:
                        break
                    date = div.find('time')
                    if date:
                        print('第' + str(i) + '个time: ' + str(date).split("\"")[1])
                        data_list.append(str(date).split("\"")[1])
                    else:
                        break
                    content1 = div.text[div.text.rfind('日') + 1:]
                    content2 = div.text[div.text.rfind('小时') + 1:]
                    if content1:
                        data_list.append(str(content1).strip().replace('\n', ''))
                        print('第' + str(i) + '个content: ' + content1)
                    else:
                        data_list.append(str(content2).strip().replace('\n', ''))
                        print('第' + str(i) + '个content: ' + content2)
                    article = div.find('article')
                    a = article.findAll('a')[2]['href']
                    print('a:', a)
                    tweetID = a.split('/')[-1]
                    print('tweetID:', tweetID)
                    tweetURL = 'https://twitter.com' + a
                    interactions = article.find('div', {'class':'css-1dbjc4n r-1ta3fxp r-18u37iz r-1wtj0ep r-1s2bzr4 r-1mdbhws'})['aria-label']
                    data_list.append(tweetID)
                    data_list.append(tweetURL)
                    data_list.append(interactions)
                    Data_List.append(data_list)
                time.sleep(1)
        except Exception as e:
            print(e)
        print('第 {} 个URL信息已获取完毕。'.format(i))
        i = i + 1

    driver.close()

    Data_List_New = []
    for data in Data_List:
        if data not in Data_List_New:
            Data_List_New.append(data)
    return Data_List_New


def Save_Data(UrlPath):
    """
    获取数据并保存数据
    """
    Data_List_New = connent_url(UrlPath=UrlPath)
    print('共爬取了 {} 条数据。'.format(len(Data_List_New)))
    df_Sheet = pd.DataFrame(Data_List_New, columns=[
                            'name', 'user_name', 'date', 'content','tweetID', 'tweetURL', 'interactions'])
    print('Get data successfully!!!')

    TIMEFORMAT = '%Y-%m-%d %H:%M:%S'
    now = datetime.datetime.now().strftime(TIMEFORMAT)
    # ----------------------- csv name -----------------------
    csv_path = '电子科大 top.csv'
    df_Sheet.to_csv(csv_path)
    print('Save - successfully!!!')

def Run():
    Save_Data(UrlPath='C:/Users/99573/Desktop/tweet_1/script/twitter_url.txt')

# if __name__ == '__main__':
#     Run()
