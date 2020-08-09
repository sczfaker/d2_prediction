import requests
import sys,io,os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from random import randint
from time import sleep
import PyV8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')




class Raybb(object):
    """docstring for Raybb"""
    def __init__(self, arg):
        super(Raybb, self).__init__()
        self.ua=UserAgent()
        self.headers={"user-agent":self.ua.random}
        self.arg = arg
    def text(self):
        reqobject=requests.get(self.arg,headers=self.headers,verify=False,timeout=30)
        if os.path.exists("main_page.txt")==False:
            with open("main_page.txt","w+",encoding="utf-8") as f:
                f.write(reqobject.text)
            return -1
        with open("main_page.txt","r+",encoding="utf-8") as f:
            text=f.read()
        one_bs4_object=BeautifulSoup(text,"html.parser")
        print (one_bs4_object.prettify())
if __name__ == '__main__':
    instance=Raybb("https://www.raybet1.com")
    instance.text()