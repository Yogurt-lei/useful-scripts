#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# yogurt_lei@foxmail.com
# 2018-10-09 11:37
# 小i新闻爬虫


import time
import datetime
import json
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}
BASE_URL = "https://www.xiaoi.com"

now = datetime.datetime.now()
start_time = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                      microseconds=now.microsecond)
start_time_stamp = int(start_time.timestamp())

# 行业分类
APP = {
    "xiaoi": ["小i新闻", "/api/api.aspx?order=" + str(start_time_stamp) + "&intcount=5&Cmd=getnew"]
}
# 置顶新闻
HOT_NEW = '/api/api.aspx?order=99999999999&intcount=1&Cmd=getnew'

TEMPLATE = '<div style="width: 100%; padding-top: 10px; padding-bottom: 20px;" class="col-xs-12 container">\
                <div>\
                    <div class="col-sm-4 col-xs-12">\
                        <div style="font-weight: 700; font-size: 1.2em">\
                            {{title}}\
                        </div>\
                    <div style="padding-bottom: 10px; padding-top: 10px">\
                        <img src="' + BASE_URL + '/Upload/{{pic}}" style="width: 100%" class="NewImg" />\
                    </div>\
                </div>\
                <div class="col-sm-8  col-xs-12 lineheight NewDetail" style="text-align: left">\
                    {{content}}\
                </div>\
            </div>'


def sub_parse(url):
    respJson = requests.get(url, headers=HEADERS).json()
    tmp_list = []
    for data in respJson:
        # 数据接口地址
        data_id = data['id']
        title = data['title']
        data_url = BASE_URL + '/api/api.aspx?id=' + str(data_id) + '&Cmd=get_newsDetail'
        respJson = requests.get(data_url, headers=HEADERS).json()

        # 填充模版 替换转义字符
        content = TEMPLATE.replace('{{title}}', respJson['title']) \
            .replace('{{content}}', respJson['content']) \
            .replace('{{pic}}', respJson['pic']) \
            .replace('&lt;', '<') \
            .replace('&gt;', '>') \
            .replace('<img src=\"/upload/', '<img src=\"' + BASE_URL + '/upload/')

        tmp_list.append({
            'id': data_id,
            'url': data_url,
            'title': title,
            'content': content
        })

    return tmp_list


if __name__ == '__main__':
    print('[%s] start grab xiaoi news data' % time.strftime('%Y-%m-%d %H:%M:%S'))
    news_data = {}
    try:
        xiaoi = APP.get('xiaoi')
        cate_name = xiaoi[0]
        data_list = sub_parse(BASE_URL + HOT_NEW)
        data_list.extend(sub_parse(BASE_URL + xiaoi[1]))
        news_data['xiaoi'] = {'category': cate_name, 'list': data_list}

        print('[%s] complete grab total %s data' % (time.strftime('%Y-%m-%d %H:%M:%S'), len(data_list)))
        params = {'newsData': json.dumps({'origin': '小i新闻', 'data': news_data})}
        resp = requests.post('http://xxxx/kbase-core/action/spider/ai-of-day!save.htm',
                             params, headers=HEADERS, timeout=120)
        if resp.status_code == 200 and resp.content:
            print('[%s] complete save action: %s ' % (time.strftime('%Y-%m-%d %H:%M:%S'), resp.json()))
        else:
            print('[%s] error occurred in save action ' % time.strftime('%Y-%m-%d %H:%M:%S'))
        print('=============================================================================')
    except Exception as e:
        print(str(e))
