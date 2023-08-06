from typing import List, Optional
from lxml.etree import HTML
from urllib import response
import requests
from requests.models import Response
from pprint import pprint
from loguru import logger
import sys
import os
from queue import Queue
import re
from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from models.result import SearchItem
    from utils.proxies import sign, auth, proxy
except:
    from encrawler.models.result import SearchItem
    from encrawler.utils.proxies import sign, auth, proxy
from typing import List, Optional, Dict



# print(os.path.abspath(__file__)

# logger level
logger.remove()
logger.add(sys.stdout, level='INFO')

logger.debug(f"os: {os.path.dirname(os.path.abspath(os.path.curdir))}")
logger.debug(f"sys: {sys.path[0]}")


class BaseSpider(object):
    def _request(self, url: str):
        """
        @summary:单次请求
        ---------
        @param url: 请求url
        --------
        @result: request, response
        """
        pass
    
    
    def validator(self, response: Response) -> bool:
        """
        @summary: 验证response是否有效
        --------
        @param response: requests.Response
        """
        pass
    
    def parser(self, response: str):
        """
        @summary: 解析response
        --------
        @param response: requests.Response
        """
        pass
    
    def search(self, keyword: str):
        """Search"""
        pass
    
    def saver(self, db_type:str = 'mongo') -> None:
        """Saver"""
        pass



class EngineBaseSpdier(BaseSpider):

    def __init__(self, headers:Optional[Dict] = {}, params:Optional[Dict] = {}, url:Optional[str] = "", **kwargs):
        """
        @summary: 初始化
        ------
        @param headers: 请求头
        """
        self.headers = headers
        self.url = "https://global.bing.com/news/search"
        self.params = {
            "q": "python",
            "qft": "sortbydate=\"1\"",
            "form": "YFNR"
        }
        self.proxy = kwargs.get("proxy")
         
    def _request(self, keyword:str, start_page=0, end_page=1, proxies=None, **kwargs):
        """
        @summary:单次请求
        ---------
        @param url: 请求url
        --------
        @result: request, response
        """
        # 参数处理
        self.params["q"] = keyword
        # 请求
        try:
            # proxy判断
            if proxies == {} or proxies == None:
                response = requests.get(
                    url=self.url, headers=self.headers, params=self.params, timeout=10)                
            else:
                proxies = kwargs.get("proxies")
                response = requests.get(
                    url=self.url, headers=self.headers, params=self.params, timeout=10, proxies=proxies, verify=False, allow_redirects=False)
        except Exception as e:
            logger.error(e)
            raise e
        return response

















class BaseBSpider():
    def __init__(self) -> None:
        """
        url example

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
        
        self.url = ""
        self.headers = {}
        self.params = {}
        # self.if_proxy = False
        self.params_queue = Queue()
        self.url_queue = Queue()
        self.item_queue = Queue()

    def start_params(self, keyword_list: List, start_page: int = 0, end_page: int = 0):
        for keyword in keyword_list:
            for page_num in range(start_page, end_page + 1):
                self.params_queue.put((keyword, page_num))


    def single_request(self, keyword:str, page_num=0, **kwargs):
        """请求一个关键词的一页数据

        Args:
            keyword (_type_): 关键词
            page_num (int, optional): 页数. Defaults to 0.
            item_num (int, optional): . Defaults to 0.
        """
        # 参数处理
        self.params["q"] = keyword
        self.params["first"] = str(page_num * 10 + 1)
        # self.params['FORM'] = "PERE" + str(page_num)
        self.params['jsoncbid'] = str(page_num)
        # 请求
        try:
            if kwargs.get("proxies"):
                proxies = kwargs.get("proxies")
                response = requests.get(
                    url=self.url, headers=self.headers, params=self.params, timeout=10, proxies=proxies, verify=False, allow_redirects=False)
            else:
                response = requests.get(
                    url=self.url, headers=self.headers, params=self.params, timeout=10)
        except Exception as e:
            logger.error(e)
            raise e
        return response

    
    def validator(self, response):
        if response.status_code == 200:
            if len(response.text) < 1000:
                logger.error("response is too short")
                return False
            else:
                return True

    def parser(self, response, **kwargs):
        # 解析
        doc = HTML(response.text)
        items = doc.xpath('//li[@class="b_algo"]')
        # links = doc.xpath("//li[contains(@class,'b_algo')]//h2/a/@href")
        # title = doc.xpath("//li[@class='b_algo']//h2/a")
        # title = [item.xpath("string(.)") for item in title]
        # content = doc.xpath("//li[contains(@class,'b_algo')]//p/text()")
        # logger.debug(kwargs)
        page_num = kwargs.get("page_num") if kwargs.get("page_num") else 0
        keyword = kwargs.get("keyword") if kwargs.get("keyword") else "None"
        item_num = kwargs.get("item_num") if kwargs.get("item_num") else None # 默认如果没有获取到则None，None就按全部返回
        item_list = []
        for i, item in enumerate(items):
            link = item.xpath("div[@class='b_title']/a/@href")
            link = link[0] if len(link) >= 1 else None
            title = item.xpath("div[@class='b_title']/h2/a")
            title = title[0].xpath("string(.)") if len(title) >= 1 else ""
            content = item.xpath("div[@class='b_caption']/p/text()")
            content = content[0] if len(content) >= 1 else ""
            rank = i + 1
            if "$ensp;" in content:
                date = content.split("$ensp;")[0]
                content = content.split("$ensp;")[-1]
            else:
                date = ""
            try:
                item = SearchItem(title=title, url=link, content=content, search_keyword=keyword, date=date, source = "bing", page_num=page_num, page_rank=rank)
                item_list.append(item.__dict__)
            except Exception as e:
                logger.error(f"[item parse error]: {e}")
                continue
            else:
                self.item_queue.put(item)
                logger.debug(item.__dict__)
        
        if item_num:
            logger.debug(f"根据item num返回{item_num}个")
            return item_list[:item_num]
        else:
            logger.debug(f"返回全部")
            return item_list


    def saver(self, item: SearchItem):
        # 保存
        with open('local_saver.txt', 'a', encoding='utf-8') as f:
            f.write(str(item.__dict__) + '\r\n')
        pass


    def start_request(self, keyword_list, start_page, end_page):
        self.start_params(keyword_list, start_page, end_page)
        while not self.params_queue.empty():
            keyword, page_num = self.params_queue.get()
            response = self.single_request(keyword, page_num)
            if self.validator(response):
                self.parser(response, **{"keyword": keyword, "page_num": page_num+1})
            else:
                logger.error("response is invalid")
                self.params_queue.put((keyword, page_num))
        while not self.item_queue.empty():
            item = self.item_queue.get()
            self.saver(item)
            # time.sleep(1)
    


    def search(self, keyword, start_page:int = 0, end_page: int = 1, item_num:int = None, **kwargs):
        """
        传入一个关键词，返回一个item list
        @keyword: 关键词
        @start_page: 开始页
        @end_page: 结束页
        @item_num: 返回item数，写1就拿一个。比如我是0，10页，每页100个，但是item写1，就只返回一个。
        @kwargs: 其他参数，如代理包括proxies, auth
        """
        if kwargs.get('proxies'): # 启用代理
            proxies = kwargs.get("proxies") if kwargs.get("proxies") else None
            auth = kwargs.get("auth") if kwargs.get("auth") else None
            self.headers.update({
                "Proxy-Authorization": auth,
            })
            response = self.single_request(keyword, start_page, **kwargs)
        else:
            response = self.single_request(keyword, start_page)
        
        # 处理
        item_list = self.parser(response, **{"keyword": keyword, "page_num": start_page, "item_num": item_num})
        if item_num:
            return item_list[item_num]
        else:
            return item_list

if __name__ == "__main__":
    print("a")
    spider = BaseSpider()
    res = spider.search("海南浪淘沙网络科技有限公司")
    print(res)
    # spider.start_request(["深圳市黑石互娱科技有限公司 企查查"], 0, 1)
    # kwargs = {
    #     "proxies": proxy,
    #     "auth": auth,
    #     "sign": sign,
    # }
    # spider.fetch_items("深圳市黑石互娱科技有限公司 企查查", start_page=0, end_page=1, item_num=1, **kwargs)
