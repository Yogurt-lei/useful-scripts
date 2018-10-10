#! /bin/sh

# desc    : 安装python3 先行执行环境
# program : spider_env
#  author : yogurt_lei@foxmail.com
#    date : 2018-10-10 15:40:35


# 检查是否是root角色
myself=`whoami`
if [ "$myself" != "root" ]; then
    echo "install role must be root";
    exit 1
fi

# 是否已安装python3
python3 -V
if [ $? -ne 0 ];
    then
    # 先行条件判断
    rpm -qa|grep openssl
    if [ $? -ne 0 ];
        then yum -y install openssl-*
    fi

    rpm -aq|grep zlib
    if [ $? -ne 0 ];
        then yum -y install zlib*
    fi

    # 源码安装
    wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
    tar -zxvf Python-3.6.0.tgz
    cd Python-3.6.0
    ./configure --with-ssl --prefix=/opt/python3 && make && make install

    # 环境配置
    ln -s /opt/python3/python/bin/python3 /usr/bin/python3
    ln -s /opt/python3/python/bin/pip3 /usr/bin/pip3
fi

echo 'now, enviroment is prepare completed, next job is edit crontab to configurate schedule spider task'
echo 'Here are some sample codes:'
echo 'crontab -e'
echo 'add new line : 0 1 * * * /usr/bin/python3 /home/yogurt/spider.py >> /home/yogurt/`date +\%Y\%m\%d`-spider.log 2>&1'
