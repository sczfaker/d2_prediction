# requests.packages.urllib3.disable_warnings()
from fake_useragent import UserAgent
from json import dump,loads,load
from requests import get
import datetime
import requests
import random
print(60000/60/60)
print()
import sys,io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
import psycopg2
class Bet_Board(object):
    def __init__(self):
        self.urlprefix="https://esportsgamelink.com/v2/odds?match_id="
        self.url="https://esportsgamelink.com/v2/odds?match_id=37213609"   
        #self.header={"user-agent":"RayClient/2.0.30(157)(Android9)"}
        self.ua = UserAgent()
        self.header={"user-agent":self.ua.random}
    def get_match_info(self):
        # import ssl
        # ssl._create_default_https_context = ssl._create_unverified_context
        t=get(self.url,headers=self.header,verify=False)
        content_text=t.text
        print (len(content_text))
        print (type(content_text))
        with open("amatch.json","w+",encoding="utf-8") as f:
            dump(loads(content_text),f)
    def stat_match(self):
        with open("amatch.json","r+",encoding="utf-8") as f:
            dic=load(f)
            betboard=dic["result"]["odds"]
            start_time=dic["result"]["start_time"]
            round_type=dic["result"]["round"]
        # print (betboard)
        for i in betboard:      
            print(i)
            # print(i,betboard[i])
            # for el_el in dic[el]:
                # print (el_el)
a=Bet_Board()

if False:
    a.get_match_info()
if False:
    a.stat_match()
#http://redirector.gvt1.com/edgedl/release2/a-Yt9tr9F-6Lj2kqiphJiw_1476/APRRvtDoJGB7M4TCKFNT4Ag
#http://avatar.csdnimg.cn:443