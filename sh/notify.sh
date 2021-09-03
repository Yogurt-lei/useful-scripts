#!/bin/bash

curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' \
   -H 'Content-Type: application/json' \
   -d '
    {
      "msgtype": "markdown",
      "markdown": {
          "content": "[x](y) <font color=\"warning\">构建成功,开发环境已更新.</font> 请相关同事注意 "
      }
    }'
