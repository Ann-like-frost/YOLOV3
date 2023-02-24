
import matplotlib.pyplot as plt
import os
import re
import threading
import queue
import traceback
from bs4 import BeautifulSoup
import requests
import pandas as pd

#爬取当当网书籍排名
"""
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78'}

data_info = {'图书排名': [],
             '图书名称': [],
             '图书作者': [],
             '图书出版时间': [],
             '图书出版社': [],
             '图书价格': [],
             '折后价格': []}

def parse_html(soup):
    li_list = soup.select('.bang_list li')
    for li in li_list:
        data_info['图书排名'].append(li.select('.list_num')[0].text.replace('.',''))
        data_info['图书名称'].append(li.select('.name a')[0].text.split(' ')[0])
        data_info['图书作者'].append(li.select('.publisher_info')[0].select('a')[0].text)
        data_info['图书出版时间'].append(li.select('.publisher_info span')[0].text)
        data_info['图书出版社'].append(li.select('.publisher_info ')[1].select('a')[0].text)
        data_info['图书价格'].append(float(li.select('.price .price_r')[0].text.replace('¥','')))
        data_info['折后价格'].append(float(li.select('.price .price_n')[0].text.replace('¥','')))

for i in range(1,26):
    url = f'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent30-0-0-1-{i}'

    response = requests.get(url=url, headers=headers, timeout=10)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')
    parse_html(soup)
book_info = pd.DataFrame(data_info)
book_info.to_csv('1.csv', encoding='utf_8_sig', index=False)
"""

#多线程 + 队列：爬取图片
'''
queue = queue.Queue()
result_urls = []
image_num = 0
image_dir = 'D:/SunFlower/Deep_Learning/YOLOV3/TensorFlow-2.x-YOLOv3-master/1'

def download_image(url, image_dir, image_num):
    try:
        r = requests.get(url, timeout=10)
        image_ext = url.split('.')[-1]
        image_name = str(image_num) + '.' + image_ext
        image_path = os.path.join(image_dir, image_name)
        with open(image_path, 'wb') as f:
            f.write(r.content)
    except:
        traceback.print_exc()

def get_image_url(url):
    try:
        home_page = re.match(r"http[s]?://\w+\.com", url).group()
        r = requests.get(url, timeout=10)
        r.encoding = 'gbk'
        soup = BeautifulSoup(r.text, 'html.parser')
        image_a = soup.find_all('a', arrts={"id": "img"})
        if image_a:
            image_relative_url = re.search(r'src="(.+?)"', str(image_a[0])).group(1)
            image_abs_url = home_page + image_relative_url
            return image_abs_url

    except:
        traceback.print_exc()

def get_page_url(url):
    try:
        home_page = re.match(r"http[s]?://\w+\.com", url).group()
        r = requests.get(url, timeout=10)
        r.encoding = 'gbk'
        soup = BeautifulSoup(r.text, 'html.parser')
        image_pase_urls = []
        image_a_lists = soup.find_all('a')
        for image_a in image_a_lists:
            relative_url = image_a['href']
            if relative_url.startswith('/tupian') and relative_url.endswith('.html') or "/index_" in relative_url:
                image_or_index_abs_url = home_page + relative_url
                image_pase_urls.append(image_or_index_abs_url)
        return image_pase_urls

    except:
        traceback.print_exc()


def task(queue):
    global result_urls
    global image_dir
    global image_num
    while not queue.empty():
        url = queue.get()
        try:
            image_download_url = get_image_url(url)
            if image_download_url and image_download_url not in result_urls:
                image_num += 1
                 download_image(image_download_url, image_dir, image_num)
                result_urls.append(image_download_url)
        except:
        traceback.print_exc()

        try:
            image_page_urls = get_page_url(url)
            while image_page_urls:
                image_page_urls = image_page_urls.copy()
                if image_page_urls not in result_urls:
                    queue.put(image_page_urls)
                    result_urls.append(image_page_urls)
        except:
            traceback.print_exc()

if __name__ == "__main__":
    image_resource_url = 'http:'
    queue.put(image_resource_url)
    t_list = []
    for i in range(100):
        t = threading.Thread(target=task, args=(queue,))
        t_list.append(t)
        t.start()
    for t in t_list:
        t.join()

'''









