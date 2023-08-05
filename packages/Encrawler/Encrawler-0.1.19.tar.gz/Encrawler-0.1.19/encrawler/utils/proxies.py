import sys
import time
import hashlib
import requests


orderno = ""    
secret = ""
ip = "dtan.xiongmaodaili.com"

port = "8088"


ip_port = ip + ":" + port

timestamp = str(int(time.time()))    
txt = ""
txt = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp

txt = txt.encode()

md5_string = hashlib.md5(txt).hexdigest()           
sign = md5_string.upper()                      
# print(sign)
auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp + "&change=true"

# print(auth)
proxy = {"http":"http://" + ip_port, "https": "http://" + ip_port}
# print(proxy)
headers = {"Proxy-Authorization": auth,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}

# r = requests.get("http://2022.ip138.com", headers=headers, proxies=proxy, verify=False,allow_redirects=False)

# print(r.text)