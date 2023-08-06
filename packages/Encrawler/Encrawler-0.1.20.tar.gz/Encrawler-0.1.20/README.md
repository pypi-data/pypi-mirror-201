# SearchEngineCrawler

#### 介绍
搜索引擎爬虫

#### 接口

- baidu: `https://www.baidu.com/s?wd={}`, method: GET
- bing国内: ``
- bing境外: `https://global.bing.com/news/?setlang=en-us&setmkt=en-us`
- 


#### 安装教程

```
pip install Encrawler
```

#### 使用说明

所有的搜索引擎爬虫都是通过search方法作为入口。参数有
- keyword：关键词
- start_page = 

1.  Bing爬虫

```
from spdiers.bing import BingSpider


bing_spider = BingSpider()
proxy_args = {
    "proxies": "ur proxy info",
    "auth": "ur auth info"
}
bing_spider.search("原神 派蒙", start_page = 0, end_page = 1, item_num = 1, **kwargs)

```
#### 关于bing news global
接口:
https://global.bing.com/news/?setlang=en-us&setmkt=en-us

**说明**：





必须要的COOKIE是

```
MUIDB= 007E5F15311D65FF38444D58308964F4;_EDGE_S= SID=33E7CE590CE063403B92DC0E0D86625E&mkt=en-us&ui=en-us;
```

其中_EDGE_S好像是固定的
MUIDB可以通过访问一次获得set-cookie，有效期大概能25天。

