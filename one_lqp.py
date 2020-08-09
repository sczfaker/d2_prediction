url="https://liquipedia.net/dota2/HuaLian"
import os
import requests
from fake_useragent import UserAgent
from random import randint

ua = UserAgent()

def get_proxy():
    PROXY_POOL_URL="http://localhost:5555/random"
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
randint_num=randint(randint(1,4),randint(8,30))
#print(randint_num)
if __name__ == '__main__':
    a="圣子华炼.txt"
    k=os.stat(a)
    print (1e4)
    print (k.st_size)



# headers={"User-Agent":ua.random+"LiveScoresBot/1.0(scz526600266@gmail.com)","Accept-Encoding":"gzip"}
# ip_other=get_proxy()
# proxie={'http':ip_other}
# print(ip_other)
# req_object=requests.get(url,headers=headers,proxies=proxie,timeout=30)
# print (req_object.text)
# print (req_object)