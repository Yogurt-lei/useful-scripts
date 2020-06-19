#!/usr/bin/python
# -*- coding: utf-8 -*-
# yogurt_lei@foxmail.com
# 2020-02-06

import datetime
import requests
from chinese_calendar import is_holiday

weather = 'http://wthrcdn.etouch.cn/weather_mini?citykey='
webhook = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={yourBotKey}'


def get_weather_info(citykey):
    '''
    获取天气信息
    :param citykey: 城市编码 中国天气网
    :return: 凭借的天气信息字符创
    '''
    resp = requests.get(weather + citykey)
    result = resp.json()

    data = result.get('data')
    city = data['city']
    ganmao = data['ganmao']
    wendu = data['wendu']
    today = data['forecast'][0]
    date = today['date']
    high = today['high'][len('高温 '):]
    low = today['low'][len('低温 '):]
    fengli = today['fengli'][len('<![cdata['):-len(']]>')]
    fengxiang = today['fengxiang']
    type = today['type']

    return '<font color="info">%s</font>: %s, 当前温度%s℃(%s-%s) 风向/风力:%s%s.\n%s' \
           % (city, type, wendu, low, high, fengxiang, fengli, ganmao)


def push_msg(content):
    '''
    推消息到企业微信
    :param content: 推送内容主体 markdown
    :return:
    '''
    wxjson = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    resp = requests.post(webhook, json=wxjson, headers={'content-type': 'application/json'})
    print(resp.text)


if __name__ == '__main__':
    now = datetime.datetime.today()
    tomorrow = now + datetime.timedelta(days=1)

    if is_holiday(now):
        print('do nothing')
        exit(0)

    if now.hour == 18:
        push_msg('上班辛苦了, 下班请勿忘记打卡, 更改Redmine状态，记得发工作日报噢.')

    if now.hour == 8:
        # 天气提醒
        shanghai = get_weather_info('101020100')
        zhangjaikou = get_weather_info('101090301')
        push_msg('上班勿忘打卡,今日天气提醒:''\n>' + shanghai + '\n>' + zhangjaikou)
