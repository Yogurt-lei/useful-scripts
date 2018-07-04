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
XINHUA_BASE_URL = "http://www.xinhuanet.com"
TODAY_REGEX = XINHUA_BASE_URL + '/politics/' + time.strftime("%Y-%m") + '/' + time.strftime("%d") + '/'
XINHUA_SAVE_ACTION = 'http://localhost:8081/kbase-core/action/spider/xinhua!save.htm'
CATE_DIR = "orz测试"


def extract_news_list():
    """
        提取今日时政新闻列表url list
    """
    html = str(requests.get(XINHUA_BASE_URL, headers=REQ_HEADERS).content, 'utf-8')
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all('a', href=re.compile(r'' + TODAY_REGEX + 'c.*\.htm'))


def extract_news_data(url_List):
    """
    提取新闻内容
    """
    news_data = []
    for tag in url_List:
        _title = tag.text
        _content = ''
        url = tag['href']
        soup = BeautifulSoup(str(requests.get(url, headers=REQ_HEADERS).content, 'utf-8'), "html.parser")
        # 特殊处理c_num为9位的元素 该种新闻为图片分页
        if len(url[url.rfind('c_') + 2:url.rfind('.htm')]) == 9:
            # 当前页图片
            article = soup.find(class_='article')
            p = article.find('p')
            img = p.find('img')
            img['src'] = TODAY_REGEX + img['src']
            _content += str(p)
            page_list = []
            for div in article.find_all('div', id=re.compile(r'^div_page_roll')):
                for a in div.find_all('a', href=re.compile(r'http://.*')):
                    page_list.append(a['href'])
            _page_list = list(set(page_list))
            _page_list.sort(key=page_list.index)

            # 处理每个分页的图片
            for _url in _page_list:
                soup = BeautifulSoup(str(requests.get(_url, headers=REQ_HEADERS).content, 'utf-8'), "html.parser")
                article = soup.find(class_='article')
                p = article.find('p')
                img = p.find('img')
                img['src'] = TODAY_REGEX + img['src']
                _content += str(p)
        else:
            # 正常新闻
            p_detail = soup.find(id="p-detail").find_all('p')
            for p in p_detail:
                for img in p.find_all('img'):
                    img['src'] = TODAY_REGEX + img['src']
                # 去除乱码
                _content += str(p)
        news_data.append({'title': _title, 'content': _content.replace(u'\xa0', u' ').replace(u'\u3000', u'  ')})

    return news_data


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
