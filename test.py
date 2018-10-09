#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# yogurt_lei@foxmail.com
# 2018-07-05 19:29
# TODO

import time
import datetime
import operator as op

if __name__ == '__main__':
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    print(yesterday.strftime("%Y-%m") + '/' + yesterday.strftime("%d"))

    timestr = '2018-10-09 10:07:06'
    timestr = timestr[:timestr.rfind(' ')]
    print(timestr)
    today_timestr = time.strftime("%Y-%m-%d")
    print(today_timestr)
    print(today_timestr == timestr)
    print(op.eq(today_timestr, timestr))
