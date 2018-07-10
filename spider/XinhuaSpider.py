#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# yogurt_lei@foxmail.com
# 2018-07-03 14:57
# 新华网新闻爬虫

import re
import json
import time
import requests
from bs4 import BeautifulSoup

REQ_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}
XINHUA_BASE_URL = "http://www.xinhuanet.com/politics/"
TODAY_REGEX = XINHUA_BASE_URL + time.strftime("%Y-%m") + '/' + time.strftime("%d") + '/'
XINHUA_SAVE_ACTION = 'xxx/kbase-core/action/spider/xinhua!save.htm'
CATE_DIR = "新闻测试"


def extract_news_list():
    """
        提取今日时政新闻列表url list
    """
    html = str(requests.get(XINHUA_BASE_URL, headers=REQ_HEADERS).content, 'utf-8')
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all('a', href=re.compile(r'' + TODAY_REGEX + 'c.*\.htm'))


def extract_news_data(url_list):
    """
    提取新闻内容
    """
    handled_list = []
    news_data = []
    for tag in url_list:
        _title = tag.text if tag.text else tag.find('img')['alt']
        _url = tag['href']
        if _url in handled_list:
            continue
        handled_list.append(_url)
        page_list, _content = extract_page_news(True, _url)
        for page_url in page_list:
            _content += extract_page_news(False, page_url)
        news_data.append({
            'id': _url[_url.rfind('c_') + 2:_url.rfind('.')],
            'url': _url,
            'title': _title,
            'content': _content.replace(u'\xa0', u' ').replace(u'\u3000', u'  ')
        })

    return news_data


def extract_page_news(is_first_page, url):
    """
    分页提取内容
    """
    soup = BeautifulSoup(str(requests.get(url, headers=REQ_HEADERS).content, 'utf-8'), "html.parser")
    page_list = []
    if is_first_page:
        for page in soup.find_all('div', id=re.compile(r'^div_page_roll')):
            for a in page.find_all('a', href=re.compile(r'http://.*')):
                if a['href'] not in page_list:
                    page_list.append(a['href'])
    main_content = soup.find(class_='article')  # 纯图分页
    if main_content is None:
        main_content = soup.find(class_="content")  # 图片+描述 分页
        if main_content is None:
            main_content = soup.find(id="p-detail")  # 图文混排
    content = ''
    for p in main_content.find_all('p'):
        for img in p.find_all('img'):
            if not img['src'].startswith(('http://', 'https://')):
                img['src'] = TODAY_REGEX + img['src']
        # 含有分页块 跳过该p
        if p.find('div', id=re.compile(r'^div_page_roll')) is not None:
            continue
        content += str(p)

    return (page_list, content) if is_first_page else content


def save_2_core(news_data):
    """
    调用kbase-core接口入库
    """
    try:
        params = {'newsData': json.dumps(news_data), 'categoryName': CATE_DIR}
        respJson = requests.post(XINHUA_SAVE_ACTION, params, headers=REQ_HEADERS, timeout=20).json()
        print(respJson)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    save_2_core(extract_news_data(extract_news_list()))
