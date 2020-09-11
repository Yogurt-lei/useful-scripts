#!/bin/bash

curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=bbc0db25-53b3-4a40-b2cb-0c3e1abfdef9' \
   -H 'Content-Type: application/json' \
   -d '
    {
      "msgtype": "markdown",
      "markdown": {
          "content": "[掌上智库](http://git.qianet.cn/shwise_dev/wise-live/pipelines) <font color=\"warning\">构建成功,开发环境已更新.</font> 请相关同事注意 "
      }
    }'
