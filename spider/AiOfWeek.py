#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# yogurt_lei@foxmail.com
# 2018-10-09 11:37
# 人工智能网新闻爬虫


import time
import json
import requests
import operator as op
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}
BASE_URL = "http://ai.ofweek.com"
# 行业分类
APP = {
    "robot": ["机器人", "/CAT-201701-robot-1.html"],
    "industry": ["工业4.0", "/CAT-201702-industry-1.html"],
    "smarthome": ["智能家居", "/CAT-201703-smarthome-1.html"],
    "uavs": ["无人系统", "/CAT-201704-uavs-1.html"],
    "vas": ["虚拟助理", "/CAT-201705-vas-1.html"],
    "bi": ["商业智能", "/CAT-201706-bi-1.html"],
    "wearable": ["可穿戴", "/CAT-201707-wearable-1.html"],
    "security": ["安防", "/CAT-201708-security-1.html"],
    "medical": ["医疗", "/CAT-201709-medical-1.html"],
    "finance": ["金融", "/CAT-201710-Finance-1.html"]
}

if __name__ == '__main__':
    print('[%s] start grab aiofweek data' % time.strftime('%Y-%m-%d %H:%M:%S'))
    news_data = {}
    counter = 0
    try:
        for (key, value) in APP.items():
            cate_name = value[0]
            url = BASE_URL + value[1]
            respJson = requests.get(url, headers=HEADERS).json()
            data_list = []
            for data in respJson['newsList']:
                id = data['detailid']
                url = data['htmlpath']
                title = data['title']
                addtimeStr = data['addtimeStr']
                addtimeStr = addtimeStr[:addtimeStr.rfind(' ')]
                # 只取今日的新闻数据
                if not op.eq(time.strftime("%Y-%m-%d"), addtimeStr):
                    continue
                counter = counter + 1
                content = BeautifulSoup(str(requests.get(url, headers=HEADERS).text), "html.parser").find(id='articleC')
                data_list.append({
                    'id': id,
                    'url': url,
                    'title': title,
                    'content': str(content)
                })
            news_data[key] = {'category': cate_name, 'list': data_list}
        print('[%s] complete grab total %s data' % (time.strftime('%Y-%m-%d %H:%M:%S'), counter))
        params = {'newsData': json.dumps({'origin': '人工智能网', 'data': news_data})}
        resp = requests.post('http://localhost:8081/kbase-core/action/spider/ai-of-day!save.htm',
                             params, headers=HEADERS, timeout=120)
        if resp.status_code == 200 and resp.content:
            print('[%s] complete save action: %s ' % (time.strftime('%Y-%m-%d %H:%M:%S'), resp.json()))
        else:
            print('[%s] error occurred in save action ' % time.strftime('%Y-%m-%d %H:%M:%S'))
        print('=============================================================================')
    except Exception as e:
        print(str(e))
