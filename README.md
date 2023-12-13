## TAC爬虫

爬取TAC列表。但并不完整，需要和购买的tac.2021.text库进行合并。爬取的包含当前最新的TAC设备清单，如iPhone15系列，三星S23系列。

由于采集的都是非官方地址，准确性无法保证，应当使用付费接口或付费购买成品库，如GSMA的TAC数据库。

由于目标站点托管在了cloudflare上，所以需要应用cloudscraper进行反制。



### 使用docker运行

#### 构建镜像

```bash
start.bat
```

#### 运行

```bash
## windows
docker run -d -v /d/home/rhino/docker:/home/rhino/tac --name tac-crawler-docker tac-crawler-docker:v1
```

在 `docker run` 时使用 `-v <host_pat>:/home/rhino/tac` 将爬取结果挂载到宿主机。

对于 Docker Desktop，需要先在 Docker Desktop 的 Settings > Resources > FILE SHARING中设置共享目录，并使用特殊的路径语法如：`-v /d/home/rhino/docker:/home/rhino/tac` 进行挂载。

```shell
## linux
$ docker run -d -v /home/rhino/docker:/home/rhino/tac --name tac-crawler-docker tac-crawler-docker:v1
```

#### 注意

对于国内环境，需要为cloudscraper增加代理设置。可以使用tor-http-proxy创建自己的代理池。

```shell
$ docker run -d -p 5000:5000 -p 1080:1080 -e tors=25 --name tor-http-proxy tor-http-proxy:v1
```

