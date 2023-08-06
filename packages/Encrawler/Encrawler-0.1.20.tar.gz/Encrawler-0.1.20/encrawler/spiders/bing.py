from typing import Optional, List, Dict
import datetime
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from basic_search_engine_spider import EngineBaseSpdier
except:
    from .basic_search_engine_spider import EngineBaseSpdier 
# from utils.proxies import sign, auth, proxy
try:
    from models.result import SearchItem
except:
    from encrawler.models.result import SearchItem
from typing import List, Optional, Union
from lxml.etree import HTML
from urllib import response
import requests
from requests import Response
from pprint import pprint
from loguru import logger
from queue import Queue
import re
from tqdm import tqdm



# logger level
logger.remove()
logger.add(sys.stdout, level='DEBUG')


class BingSpider():
    def __init__(self) -> None:
        """
        url example
        1. https://cn.bing.com/search?q=feapder&sp=-1&pq=feapd&sc=10-5&qs=n&sk=&cvid=B37D311496924EE5BA4A361453603158&ghsh=0&ghacc=0&ghpl=&first=11&FORM=PERE&sid=1AC5DDE16A1B6AC324DACFA26BC96B16&format=snrjson&jsoncbid=0
        2. https://cn.bing.com/search?q=feapder&sp=-1&pq=feapd&sc=10-5&qs=n&sk=&cvid=B37D311496924EE5BA4A361453603158&ghsh=0&ghacc=0&ghpl=&first=21&FORM=PERE1&sid=1AC5DDE16A1B6AC324DACFA26BC96B16&format=snrjson&jsoncbid=1


        参数说明:
        - q 搜索关键词
        - form 不知道
        - sp 不知道
        - pq 不知道 搜索关键词少一部分，具体作用未知
        - sc 不知道 目前固定10-5
        - qs 不知道
        - sk 不知道
        - cvid 不知道
        - first 翻页相关，首页可以没有，从1开始，第二页开始是11，第三页是21
        - FORM 翻页相关，首页可以没有，从PERE开始，第二页是PERE1，第三页是PERE2
        - jsoncbid 页数，从0开始

        """

        self.url = "https://cn.bing.com/search"
        self.headers = {
            "authority": "cn.bing.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://cn.bing.com/?toWww=1&redig=CA031F11A6E043DCB43274F999E219D3&FORM=BEHPTB&ensearch=1",
            "sec-ch-ua": "\"Chromium\";v=\"106\", \"Google Chrome\";v=\"106\", \"Not;A=Brand\";v=\"99\"",
            "sec-ch-ua-arch": "\"x86\"",
            "sec-ch-ua-bitness": "\"64\"",
            "sec-ch-ua-full-version": "\"106.0.5249.119\"",
            "sec-ch-ua-full-version-list": "\"Chromium\";v=\"106.0.5249.119\", \"Google Chrome\";v=\"106.0.5249.119\", \"Not;A=Brand\";v=\"99.0.0.0\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "\"\"",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua-platform-version": "\"15.0.0\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        }
        self.params = {
            "q": "your keyword",
            "form": "QBLHCN",
            "sp": "-1",
            "pq": "feapd",
            "sc": "10-5",
            "qs": "n",
            "sk": "",
            "cvid": "B37D311496924EE5BA4A361453603158",
            "ghsh": "0",
            "ghacc": "0",
            "ghpl": "",
            "first": "",
            "jsoncbid": "",
        }
        # self.if_proxy = False
        self.params_queue = Queue()
        self.url_queue = Queue()
        self.item_queue = Queue()
        self.total_count_no_proxy = 0
        self.total_count_proxy = 0
        

    def start_params(self, keyword_list: List, start_page: int = 0, end_page: int = 0):
        for keyword in keyword_list:
            for page_num in range(start_page, end_page + 1):
                self.params_queue.put((keyword, page_num))

    def single_request(self, keyword: str, page_num=0, proxies:Dict =None, **kwargs) -> requests.Response:
        """
        请求一个关键词的一页数据

        Args:
            keyword (_type_): 关键词
            page_num (int, optional): 页数. Defaults to 0.
            item_num (int, optional): . Defaults to 0.
        
        Returns:
            requests.Response: 返回的response
        
        """
        # 参数处理
        self.params["q"] = keyword
        self.params["first"] = str(page_num * 10 + 1)
        # self.params['FORM'] = "PERE" + str(page_num)
        self.params['jsoncbid'] = str(page_num)
        # 请求
        try:
            if proxies:
                try:
                    response = requests.get(
                        url=self.url, headers=self.headers, params=self.params, timeout=10, proxies=proxies, verify=False, allow_redirects=False)
                    self.total_count_proxy += 1
                    logger.debug(f"使用代理请求，目前已使用代理{self.total_count_proxy}次")
                except Exception as e:
                    self.total_count_no_proxy += 1
                    logger.warning(f"代理请求失败，使用无代理重试，目前已使用无代理{self.total_count_no_proxy}次，错误信息：{e}")
                    response = requests.get(
                        url=self.url, headers=self.headers, params=self.params, timeout=10)
                    
            else:
                logger.debug(f"使用无代理请求, 目前已经使用无代理{self.total_count_no_proxy}次")
                response = requests.get(
                    url=self.url, headers=self.headers, params=self.params, timeout=10)
        except Exception as e:
            logger.error(e)
            raise e
        return response

    def validator(self, response):
        if response.status_code == 200:
            if len(response.text) < 1000:
                logger.error(f"请求失败，返回内容太少，可能被封了，返回内容为{response.text}")
                logger.error("response is too short")
                return False
            else:
                return True

    def parser(self, response, **kwargs) -> List[Dict]:
        """
        解析一个bing搜索返回的response 

        :param requests.Response response: 一个bing搜索返回的response
        :return List[Dict]: 返回一个列表，列表中每个元素是一个字典，字典中包含title, link, content, date
        """
        doc = HTML(response.text)
        items = doc.xpath('//li[@class="b_algo"]')
        page_num = kwargs.get("page_num") if kwargs.get("page_num") else 0
        keyword = kwargs.get("keyword") if kwargs.get("keyword") else "None"
        # item_num = kwargs.get("item_num") if kwargs.get("item_num") else None # 默认如果没有获取到则None，None就按全部返回
        item_list = []
        for i, item in enumerate(items):
            link = item.xpath("div[@class='b_title']/a/@href")
            link = link[0] if len(link) >= 1 else None
            title = item.xpath("div[@class='b_title']/h2/a")
            title = title[0].xpath("string(.)") if len(title) >= 1 else ""
            content = "".join(item.xpath("div[@class='b_caption']/p/text()"))
            # if "\\u2002·\\u2002;" in content:
            if re.findall(r"\u2002·\u2002", content):
                date = re.split(r"\u2002·\u2002", content)[0]
                # content = content.split("$ensp;")[-1]
            else:
                date = ""
            # date = content
            content = "".join(re.split(r"\u2002·\u2002", content)[
                              1:]) if len(content) >= 2 else ""
            rank = i + 1

            try:
                item = SearchItem(title=title, url=link, content=content, search_keyword=keyword,
                                  time=date, source="", page_num=page_num, page_rank=rank)
                item_list.append(item.__dict__)
            except Exception as e:
                logger.error(f"[item parse error]: {e}")
                continue
            else:
                self.item_queue.put(item)
                logger.debug(item.__dict__)

        # if item_num:
        #     logger.debug(f"根据item num返回{item_num}个")
        #     return item_list[:item_num]
        # else:
            # logger.debug(f"返回全部, 共计{len(item_list)}个")
        return item_list

    def saver(self, item: SearchItem):
        # 保存
        with open('local_saver.txt', 'a', encoding='utf-8') as f:
            f.write(str(item.__dict__) + '\r\n')
        pass

    # def start_request(self, keyword_list, start_page, end_page):
    #     self.start_params(keyword_list, start_page, end_page)
    #     while not self.params_queue.empty():
    #         keyword, page_num = self.params_queue.get()
    #         response = self.single_request(keyword, page_num)
    #         if self.validator(response):
    #             self.parser(response, **{"keyword": keyword, "page_num": page_num+1})
    #         else:
    #             logger.error("response is invalid")
    #             self.params_queue.put((keyword, page_num))
    #     while not self.item_queue.empty():
    #         item = self.item_queue.get()
    #         self.saver(item)
        # time.sleep(1)

    def search(self, keyword, start_page: int = 0, end_page: int = 1, item_num: int = 0, proxies=None, callback=None, **kwargs):
        """
        搜索给定关键词并返回结果列表。

        :param keyword: str, 搜索的关键词。
        :param start_page: int, 开始页码（包含），默认为1。
        :param end_page: int, 结束页码（包含）。
        :param item_num: int, 返回每页的结果数，例如，如果item_num为1，则每页仅返回1个结果。默认为10。
        :param kwargs: dict, 其他参数，如代理（proxies）和认证（auth）信息。
        :return: List[Dict], 包含搜索结果的列表，每个结果是一个字典。

        Example:
        带代理的
        kwargs = {
            
        }
        self.search("chatgpt", **kwargs)
        """
        all_item_list = []
        # 若获取代理不为None或不为空字典则启用代理，允许传入空字典，则不启用代理
        if proxies != None:
            auth = kwargs.get("auth") if kwargs.get("auth") else None
            self.headers.update({
                "Proxy-Authorization": auth,
            })
            for i in range(start_page, end_page):
                response = self.single_request(keyword, i, proxies=proxies)
                if self.validator(response):
                    item_list = self.parser(
                        response, **{"keyword": keyword, "page_num": i+1, "item_num": item_num})
                    all_item_list += item_list
                    # return all_item_list
                else:
                    logger.error(f"response is invalid, proxies: {proxies}")
                    continue
        else:
            for i in range(start_page, end_page):
                response = self.single_request(keyword, i)
                if self.validator(response):
                    item_list = self.parser(
                        response, **{"keyword": keyword, "page_num": i+1, "item_num": item_num})
                    all_item_list += item_list
                    # return all_item_list
                else:
                    logger.error("response is invalid")
                    continue
        # 回调
        if callback:
            callback(all_item_list)

        # 处理
        # item_list = self.parser(response, **{"keyword": keyword, "page_num": start_page, "item_num": item_num})
        if item_num != 0:
            logger.info(f"【{keyword}】根据item num返回{item_num}个")
            return all_item_list[item_num:]
        else:
            logger.info(f"【{keyword}】返回全部, 共计{len(all_item_list)}个")
            return all_item_list


class BingNewsSpider(EngineBaseSpdier):
    def __init__(self):
        self.headers = {
            "authority": "global.bing.com",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "referer": "https://global.bing.com/news/search?q=%e5%b0%8f%e7%b1%b3%e7%a7%91%e6%8a%80%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8&qft=sortbydate%3d%221%22&form=YFNR",
            "sec-ch-ua": "\"Google Chrome\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"",
            "sec-ch-ua-arch": "\"x86\"",
            "sec-ch-ua-bitness": "\"64\"",
            "sec-ch-ua-full-version": "\"107.0.5304.106\"",
            "sec-ch-ua-full-version-list": "\"Google Chrome\";v=\"107.0.5304.106\", \"Chromium\";v=\"107.0.5304.106\", \"Not=A?Brand\";v=\"24.0.0.0\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua-platform-version": "\"15.0.0\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        # # 根据时间排序的参数，内容效果不好。
        # self.params =  {
        #     "qft": "sortbydate=\"1\"",
        #     "form": "YFNR",
        #     "InfiniteScroll": "1",
        #     "q": "小米科技有限公司",
        #     "first": "31",
        #     # "IG": "17090128228D48E6BFEA40BB804017C6",
        #     "IID": "NEWS.302",
        #     "SFX": "2",
        #     "PCW": "941"
        # }

        # 根据相关度排序的参数，时间乱，但内容好。
        self.params = {
            "FORM": "HDRSC6",
            "InfiniteScroll": "1",
            "q": "小米科技有限公司",
            "first": "1",
            # "IG": "17090128228D48E6BFEA40BB804017C6",
            "IID": "NEWS.302",
            "SFX": "2",
            "PCW": "1116"
        }

    def _request(self, keyword: str, page_num: int = 0, proxies: Optional[Dict] = {}, cookies: Optional[Dict] = {}, **kwargs) -> Response:
        """
        请求news接口单页数据, 返回Response对象

        :param str keyword: 关键词
        :param int page_num: 请求第几页, defaults to 0
        :param Optional[Dict] proxies: 代理信息, defaults to {}
        :param Optional[Dict] cookies: cookies信息, defaults to {}
        :raises e: _description_
        :return Reponse: request response对象
        """
        # 参数处理
        self.params["q"] = keyword
        self.params["first"] = str(page_num*10+1)
        self.url = "https://global.bing.com/news/infinitescrollajax"

        # 请求
        try:
            # proxy判断
            if proxies == {} or proxies == None:  # 无proxy
                if cookies == {} or cookies == None:  # 无cookie
                    response = requests.get(
                        url=self.url, headers=self.headers, params=self.params, timeout=10)
                else:  # 有cookie
                    response = requests.get(
                        url=self.url, headers=self.headers, params=self.params, cookies=cookies, timeout=10)
            else:  # 有proxy
                proxies = kwargs.get("proxies")
                if cookies == {} or cookies == None:  # 无cookie
                    response = requests.get(
                        url=self.url, headers=self.headers, params=self.params, timeout=10, proxies=proxies, verify=False, allow_redirects=False)
                else:  # 有cookie
                    response = requests.get(url=self.url, headers=self.headers, params=self.params,
                                            cookies=cookies, timeout=10, proxies=proxies, verify=False, allow_redirects=False)
        except Exception as e:
            logger.error(e)
            raise e
        return response

    def parser(self, response, **kwargs) -> List[Dict]:
        """
        解析response, 返回item_list

        :param _type_ response: _description_
        :return _type_: _description_
        """
        item_list = []
        doc = HTML(response.text)
        res = doc.xpath('//div[contains(@class,"news-card")]')
        # title_list = [item.xpath('.//a[@class="title"]/text()')[0] for item in res]
        # print(title_list)
        res = res[::2]
        title_list = [item.xpath('.//a[@class="title"]/text()')[0] for item in res]
        logger.debug(f"title list {title_list}")
        crawltime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        page_num = kwargs.get("page_num")
        keyword = kwargs.get("keyword")
        for i, item in enumerate(res):
            title = item.xpath('.//a[@class="title"]/text()')[0]
            url = item.xpath('.//a[@class="title"]/@href')[0]
            content = item.xpath(
                './/div[contains(@class,"snippet")]/text()')[0]
            raw_source = item.xpath(
                ".//div[@class='source biglogo']/a[@class='biglogo_link']/@aria-label")
            source = item.xpath(".//div[@class='source biglogo']/a[@class='biglogo_link']/@aria-label")[
                0].replace("Search news from ", "") if len(raw_source) >= 1 else ""
            raw_publish_time = item.xpath(
                ".//div[@class='source biglogo']/div/span[2]/@aria-label")
            publish_time = raw_publish_time[0] if len(
                raw_publish_time) >= 1 else ""
            # 注意这里time还没有处理，还是以28d，5h，1m的形式存在
            page_num = kwargs.get("page_num")
            page_rank = i
            validate_item = SearchItem(title=title, url=url, content=content, search_keyword=keyword,
                                       time=publish_time, source=source, page_num=page_num, page_rank=page_rank, crawltime=crawltime)
            item_list.append(validate_item)
        return item_list

    def search(self, keyword, start_page: int = 0, end_page: int = 1, proxy: Dict = {}, **kwargs):
        """
        传入一个关键词，返回一个item list
        @keyword: 关键词
        @start_page: 开始页
        @end_page: 结束页
        @proxy: 代理
        @kwargs: 其他参数，如代理的auth, params的修改，cookies等
        """
        all_item_list = []
        for i in range(start_page, end_page):

            # 代理判断
            proxy = kwargs.get("proxy")
            # 无代理
            if proxy == {} or proxy == None:
                if kwargs.get('cookie') != None and kwargs.get('cookie') != {}:
                    cookie = kwargs.get("cookie")
                    response = self._request(keyword, i, cookies=cookie)
                else:
                    response = self._request(keyword, i)
            # 有代理
            else:
                if kwargs.get('cookie') != None and kwargs.get('cookie') != {}:
                    cookie = kwargs.get("cookie")
                    response = self._request(
                        keyword, i, proxies=proxy, cookies=cookie)
                else:
                    response = self._request(keyword, i, proxies=proxy)

            # 解析
            search_item_list = self.parser(
                response, **{"keyword": keyword, "page_num": i+1})
            all_item_list += search_item_list
        return all_item_list


if __name__ == "__main__":
    # baisc search
    # spider = BingSpider()
    # res = spider.search("自称家里有50辆宾利女车主发声",0, 3)
    # for item in res:
    #     pprint(item)

    # news search
    spider = BingNewsSpider()
    cookies = {
        "MUID": "007E5F15311D65FF38444D58308964F4",
        "_EDGE_V": "1",
        "SRCHD": "AF=NOFORM",
        "SRCHUID": "V=2&GUID=18FB639A544A47C1ADB5693A85AF096F&dmnchg=1",
        "_UR": "QS=0&TQS=0",
        "ANIMIA": "FRE=1",
        "MUIDV": "NU=1",
        "ZHCHATSTRONGATTRACT": "TRUE",
        "SUID": "M",
        "ipv6": "hit=1668005259440&t=4",
        "SRCHUSR": "DOB=20221030&T=1668001657000&TPC=1668001668000",
        "ZHCHATWEAKATTRACT": "TRUE",
        "MUIDB": "007E5F15311D65FF38444D58308964F4",
        "_EDGE_S": "SID=33E7CE590CE063403B92DC0E0D86625E&mkt=en-us&ui=en-us",
        "_clck": "9xqb8t|1|f6f|0",
        "_HPVN": "CS=eyJQbiI6eyJDbiI6MywiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MywiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MywiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMi0xMS0wOVQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIkRmdCI6bnVsbCwiTXZzIjowLCJGbHQiOjAsIkltcCI6MTF9",
        "_BINGNEWS": "SW=1903&SH=929",
        "SRCHHPGUSR": "SRCHLANG=en&BRW=XW&BRH=M&CW=1920&CH=929&SCW=1903&SCH=2647&DPR=1.0&UTC=480&DM=0&PV=15.0.0&HV=1668002893&PRVCW=1920&PRVCH=929&WTS=63803598465&BZA=1",
        "_RwBf": "ilt=12&ihpd=2&ispd=3&rc=41&rb=0&gb=0&rg=200&pc=36&mtu=0&rbb=0&g=0&cid=&clo=0&v=9&l=2022-11-09T08:00:00.0000000Z&lft=2022-11-07T00:00:00.0000000-08:00&aof=0&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2022-11-09T14:08:11.2078072+00:00&rwred=0",
        "_SS": "SID=33E7CE590CE063403B92DC0E0D86625E&R=41&RB=0&GB=0&RG=200&RP=36",
        "_clsk": "8fbovk|1668002892749|4|0|d.clarity.ms/collect",
        "SNRHOP": "I=&TS="
    }
    kwargs = {}
    kwargs["cookie"] = cookies

    res = spider.search("维护国家主权和领土完整的能力", 0, 2, proxy=proxies,**kwargs)
    for item in res:
        pprint(item.__dict__['title'])
