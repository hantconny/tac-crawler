FROM alpine:3.18

RUN echo '@edge https://dl-cdn.alpinelinux.org/alpine/edge/community' >> /etc/apk/repositories && \
    echo '@edge https://dl-cdn.alpinelinux.org/alpine/edge/testing'   >> /etc/apk/repositories && \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
	apk -U upgrade && \
    apk -v add python3@edge py3-pip@edge && \
    rm -rf /var/cache/apk/* && \
    mkdir -p /etc/crawler/

## 加密环境内使用
#COPY /files/app.python /etc/crawler/app.py
#COPY /files/settings.python /etc/crawler/settings.py
#COPY /files/requirements /etc/crawler/requirements
#COPY /files/README.md /etc/crawler/README.md

## 非加密环境内使用
COPY /files/ /etc/crawler/

WORKDIR /etc/crawler

RUN pip install -r requirements

## 在 docker run 时使用 -v <host_pat>:/home/rhino/tac 将爬取结果挂载到宿主机
## 对于 Docker Desktop，需要先在 Docker Desktop 的 Settings > Resources > FILE SHARING中设置共享目录
## 并使用特殊的路径语法如：-v /d/home/rhino/docker:/home/rhino/tac 进行挂载
VOLUME /home/rhino/tac

CMD python3 /etc/crawler/app.py