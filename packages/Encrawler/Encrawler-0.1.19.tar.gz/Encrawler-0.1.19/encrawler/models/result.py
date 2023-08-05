from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from typing import List, Dict, Optional, Union



today = datetime.now().strftime('%Y-%m-%d')
# print("&ensp;" * 2)


class SearchItem(BaseModel):
    title: str
    content: str
    search_keyword: str
    url: Optional[str]
    time: Optional[str]
    img_url: Optional[str]
    source: str
    page_num: int
    page_rank: int
    author: Optional[str]
    crawltime: str = today
    
    # @validator('url')
    # def url_validator(cls, v):
    #     if not v.startswith("http"):
    #         raise ValueError("url must start with http")
    #     return v



class TopsKeywordItem(BaseModel):
    keyword: str # 关键词
    url: Optional[str] # 详情链接
    title: Optional[str] # 详情标题
    content: Optional[str] # 详情内容
    time: Optional[str] 
    source: str
    crawltime: str = today
    page_num: int
    page_rank: int

    img_url: Optional[str]