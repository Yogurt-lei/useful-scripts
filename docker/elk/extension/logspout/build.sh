#!/bin/sh

# unmodified from:
# https://github.com/gliderlabs/logspout/blob/67ee3831cbd0594361bb3381380c65bdbeb3c20f/custom/build.sh

set -e
# 设置国内镜像源
echo "https://mirror.tuna.tsinghua.edu.cn/alpine/v3.11/main" > /etc/apk/repositories
echo "https://mirror.tuna.tsinghua.edu.cn/alpine/v3.11/community" >> /etc/apk/repositories
apk update
apk add --update tzdata go git mercurial build-base

# 设置时区
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
echo "Asia/Shanghai" > /etc/timezone

mkdir -p /go/src/github.com/gliderlabs
cp -r /src /go/src/github.com/gliderlabs/logspout
cd /go/src/github.com/gliderlabs/logspout

# 设置go的国内镜像
export GO111MODULE=on
export GOPROXY=https://goproxy.cn
export GOPATH=/go
go get
go build -ldflags "-X main.Version=$1" -o /bin/logspout
apk del tzdata go git mercurial build-base
rm -rf /go /var/cache/apk/* /root/.glide /root/.cache /tmp/*

# backwards compatibility
ln -fs /tmp/docker.sock /var/run/docker.sock

