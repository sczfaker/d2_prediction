import sys,io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
from fake_useragent import UserAgent
from re import findall,compile,match
from os import chdir,listdir,rename
from re import findall,compile
from json import load,dump,loads
from bs4 import BeautifulSoup
from requests import get
from time import sleep
from json import dump
import datetime
import requests
import os
import re
def atest():
    ana_info={}
    full_path_name="player_html/midone"
    with open(full_path_name+".txt","r+",encoding="utf-8") as f:
        person_text=f.read()
        print (person_text)
        bs4_person_object=BeautifulSoup(person_text,"html.parser")
        if bs4_person_object:
        #名字,出生日期,钱,steam链接,buff链接,datadota链接,stratz,twii,history
            person_tag=bs4_person_object.find("div",class_="fo-nttax-infobox wiki-bordercolor-light")
            if person_tag:
                person_info_tag=person_tag.find_all("div",class_="infobox-cell-2 infobox-description")
                realname,earn_tour,birth=person_info_tag[0].get_text(),person_info_tag[-1].get_text().replace("$","").replace(",",""),person_info_tag[1].get_text().replace("\"","")
                ana_info[realname],ana_info[earn_tour],ana_info[birth]={},{},{}
            link_tag=bs4_person_object.find("div",class_="infobox-center infobox-icons")
            if link_tag:
                link_tag_list=link_tag.find_all("a")
                for out_link_tag in link_tag_list:
                    if out_link_tag["href"].find("steam")==True:
                        steam_url=out_link_tag["href"]
                        ana_info[steam_url]={}
                    elif out_link_tag["href"].find("dotabuff")==True:
                        buff_url=out_link_tag["href"]
                        ana_info[buff_url]={}
                    elif out_link_tag["href"].find("datadota")==True:
                        dat_url=out_link_tag["href"]
                        ana_info[dat_url]={}
                    elif out_link_tag["href"].find("stratz")==True:
                        stratz_url=out_link_tag["href"]
                        ana_info[stratz_url]={}
        else:
            ana_info={"此选手还无信息":"此选手还无信息"}
    return ana_info
def team_json_check():
    with open("current_p_team.json","r+",encoding="utf-8") as f:
        x=load(f)
    print (len(x))
if __name__ == '__main__':
    # print (atest())
    team_json_check()