from fake_useragent import UserAgent
from re import search,findall
import urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup
from requests import get
import requests
import sys,io
import time
import os
import re
from json import loads,dump,load
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
from time import sleep
"https://www.tuotugame.com/dota2/5ef8a9a94302e82c262a1add"
url="app.tuotuesports.com:443"
url_host="www.trackdota.com"#"dragate.dc.oppomobile.com:443"

class Ban_Pick(object):
    """docstring for ClassName"""
    def __init__(self,crawl_banpick_url_id=False):
        self.ua = UserAgent()
        self.id="5557675466"
        self.dotabutff_headers={"user-agent":self.ua.random}
        self.raybet_headers={"user-agent":self.ua.random}
        self.id_list=[]
        if crawl_banpick_url_id==True:
            self.get_live_match_id(update_live_match=True)
        self.match_url=self.id_list[:]
        self.headers = {'Host': 'www.vpgame.com', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.88 Safari/537.36 Vivaldi/2.4.1488.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9'}
        self.cookies = {'_ga': 'GA1.2.54914190.1596865764', '_gid': 'GA1.2.497165365.1596865764', '_hjid': '455f154e-5b0c-47e9-a738-3b4e0287f99e', '_hjIncludedInCCSample': '1', '_hjIncludedInSample': '1'}
        self.cookies={}
        #self.trackdota_id="https://www.trackdota.com/matches/5581593017"
        x="https://www.raybet1.com"
    def get_proxy(self):
        PROXY_POOL_URL="http://localhost:5555/random"
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            return None
    def get_vpgame(self):#https://www.vpgame.com/schedule/dota/dotaS00007718
        with open("request.log","r",encoding="utf-8") as f:
            url_suffix_list=f.readlines()
            elimiate_duplicate=list(set(url_suffix_list))
            url_suffix=elimiate_du3-plicate[0]
            url_suffix=url_suffix.split()[-1]
        url="https://www.vpgame.com"
        ip_other=self.get_proxy()
        proxie={'http':ip_other}
        #proxies=proxie
        with open("request.log","r",encoding="utf-8") as f:
            url_suffix_list=f.readlines()
            elimiate_duplicate=list(set(url_suffix_list))
            url_suffix=elimiate_duplicate[0]
            url_suffix=url_suffix.split()[-1]
        url=url+url_suffix
        req_object=requests.get(url,headers=self.headers,proxies=proxie,verify=False)
        # print(url)
        html_text=req_object.text
        bs4_object=BeautifulSoup(html_text,"html.parser")
        pick_object=bs4_object.find("body",attrs={"lang":"zh_CN"})#.find("script").get_text().strip()[:10]
        # print (pick_object.find("div",class_="pick"))

        # print (pick_object.find("script").string[26:])
        dict_data=loads(pick_object.find("script").string[26:])
        # print (dict_data)
        team1_hero=[]
        team2_hero=[]
        t1zhname=[]
        t2zhname=[]
        team1=dict_data["dota2Live"]["realData"]["data"]["team1"]["abbr"]
        team2=dict_data["dota2Live"]["realData"]["data"]["team2"]["abbr"]
        for key in dict_data["dota2Live"]["realData"]["data"]["team1"]["picks"]:
            team1_hero.append(key["id"])
            t1zhname.append(key["zh_name"])
        for key in dict_data["dota2Live"]["realData"]["data"]["team2"]["picks"]:
            team2_hero.append(key["id"])
            t2zhname.append(key["zh_name"])
        print (t1zhname,team1_hero,team1)
        print (t2zhname,team2_hero,team2)

        return team1_hero,team2_hero,team1,team2
    def get_kuaikegame(self):
        with open("request.log","r",encoding="utf-8") as f:
            url_suffix_list=f.readlines()
            elimiate_duplicate=list(set(url_suffix_list))
            url_suffix=elimiate_duplicate[0]
            url_suffix=url_suffix.split()[-1]
        url="http://kuaikegame.com"+url_suffix#/api/steam/dota/series/getDota2SeriesDtlPageInfo.do?seriesPkId=def4cf12-25e9-4853-af00-bbc6bfc1be6d"
        print (url)
        ip_other=self.get_proxy()
        proxie={'http':ip_other}
        print (proxie)
        url_list=[""]
        req_object=requests.get(url,headers=self.headers,verify=False)#proxies=proxie
        html_text=req_object.text
        json_match_info=loads(html_text)
        with open("kuaike.json","w+",encoding="utf-8") as f:
            dump(json_match_info,f,ensure_ascii=False)
        with open("kuaike.json","r",encoding="utf-8") as f:
            json_match_info=load(f)

        radiant_id,dire_id=[],[]
        for i in loads(json_match_info["content"]["latestBattleData"]["radiant_player_stats"]):
            radiant_id.append(i["heroid"])
        for i in loads(json_match_info["content"]["latestBattleData"]["dire_player_stats"]):
            dire_id.append(i["heroid"])
        radiant_team_name=json_match_info["content"]["latestBattleData"]["team_name_radiant"]
        dire_team_name=json_match_info["content"]["latestBattleData"]["team_name_dire"]

        return radiant_id,dire_id,radiant_team_name,dire_team_name

    def get_trackdota(self,url):
        req_object=requests.get(url,headers=self.headers,verify=False, cookies=self.cookies)
        html_text=req_object.text

        bs4_object=BeautifulSoup(html_text,"html.parser")
        hero_list=bs4_object.find_all("tr",class_=re.compile("(sc-1bsds4m-4 DeHec|sc-1bsds4m-4 DeHec)"))
        teamname=bs4_object.find_all("div",class_=re.compile("(pl5yvg-0 Nrmoj|pl5yvg-0 dvkNLb)"))
        rteamname,dteamname=teamname[0].get_text(),teamname[1].get_text()
        print (rteamname,dteamname)
        r_hero_list,d_hero_list=hero_list[:5],hero_list[10:15]
        radiant_name,dire_name=[],[]
        for heroname_r,heroname_d in zip(r_hero_list,d_hero_list):
            one_rname=heroname_r.find("td").find("div")["title"].split()[:-2]
            one_dname=heroname_d.find("td").find("div")["title"].split()[:-2]
            if len(one_rname)>=2:
                one_rname="-".join(one_rname).lower()
            else:
                one_rname=one_rname[0].lower()
            if len(one_dname)>=2:
                one_dname="-".join(one_dname).lower()
            else:
                one_dname=one_dname[0].lower()
            radiant_name.append(one_rname)
            dire_name.append(one_dname)
        pattern=re.compile("(?<=match/)\d+")
        print(radiant_name,dire_name,rteamname,dteamname)
        return radiant_name,dire_name,rteamname,dteamname
    def get_content(self,url_score):
        req_object=requests.get(url_score,headers=self.headers,verify=False, cookies=self.cookies)
        html_text=req_object.text
        dic_data=loads(html_text)

        radiant_name,dire_name=dic_data["radiant_team"]['tag'],dic_data["dire_team"]['tag']
        radiant,dire=dic_data["radiant_picks"],dic_data["dire_picks"]
        return radiant,dire,radiant_name,dire_name
    def clear(self):
        with open ("request.log","w+",encoding="utf-8") as f:
            pass
    def raybet(self,update_live_match=True):
        print ("函数循环执行不打印")
        from json import dump,loads,load#202
        import json
        url_list=["https://incpgameinfo.esportsworldlink.com/v2/odds?match_id=37273472"]#new_id
        #"https://www.raybet1.com/match/37243802"
        json_file_name="raybet_board.json"
        for url in url_list:
            if update_live_match==True:
                try:
                    req_buff_object=get(url,headers=self.raybet_headers,timeout=30)
                    json_req_buff_object=loads(req_buff_object.text)
                    with open(json_file_name,"w+",encoding="utf-8") as f:
                        json.dump(json_req_buff_object,f,ensure_ascii=False)
                except Exception as e:
                    print (e.args)
            if os.path.exists(json_file_name):
                with open(json_file_name,"r+",encoding="utf-8") as f:
                    self.dict_bet_board=load(f)
        count=0
        bet_json="raybet_sequence.json"
        if os.path.exists(bet_json):
            with open(bet_json,"r+",encoding="utf-8") as f:
                self.bet_rate=load(f)
        else:    
            self.bet_rate={}
        self.r_team_name=self.dict_bet_board["result"]["odds"][0]["name"]
        self.d_team_name=self.dict_bet_board["result"]["odds"][1]["name"]
        for dict_element in self.dict_bet_board["result"]["odds"]:
            team_name=dict_element["name"]
            if count==0:
                if team_name not in self.bet_rate:
                    team_right=team_name
                    self.bet_rate[team_right]={}
            if count==1:
                if team_name not in self.bet_rate:
                    team_left=team_name
                    self.bet_rate[team_left]={}
            if dict_element["match_stage"]=="r1" and dict_element["group_name"]=="获胜者" and team_name in self.bet_rate and dict_element["odds"]:
                if "第一局胜者" not in self.bet_rate[team_name]:
                    self.bet_rate[team_name]["第一局胜者"]=[[team_name,dict_element["odds"]]]
                else:
                    if [team_name,dict_element["odds"]] not in self.bet_rate[team_name]["第一局胜者"]:
                        self.bet_rate[team_name]["第一局胜者"].append([team_name,dict_element["odds"]])
            if dict_element["match_stage"]=="r2" and dict_element["group_name"]=="获胜者" and team_name in self.bet_rate and dict_element["odds"]:
                if "第二局胜者" not in self.bet_rate[team_name]:
                    self.bet_rate[team_name]["第二局胜者"]=[[team_name,dict_element["odds"]]]
                else:
                    if [team_name,dict_element["odds"]] not in self.bet_rate[team_name]["第二局胜者"]:
                        self.bet_rate[team_name]["第二局胜者"].append([team_name,dict_element["odds"]])
            if dict_element["match_stage"]=="final" and dict_element["group_name"]=="获胜者" and team_name in self.bet_rate and dict_element["odds"]:
                if "胜者" not in self.bet_rate[team_name]:
                    self.bet_rate[team_name]["胜者"]=[[team_name,dict_element["odds"]]]
                else:
                    if [team_name,dict_element["odds"]] not in self.bet_rate[team_name]["胜者"]:
                        self.bet_rate[team_name]["胜者"].append([team_name,dict_element["odds"]])
            count+=1
        try:
            print ("更新一次赔率表:",self.update_count,self.total_time,"secs")
            self.update_count+=1
            with open(bet_json,"w+",encoding="utf-8") as f:
                dump(self.bet_rate,f,ensure_ascii=False)
        except:
            assert 1>2,"file error"
        return self.bet_rate
    def calculate_and_show(self):
        with open(bet_json,"r+",encoding="utf-8") as f:
            bet_rate=load(f)        
            bet_rate.items()[0],bet_rate.items()[1]
    def betrate_sequence(self,new_match=True):
        if new_match==True:
            bet_json="raybet_sequence.json"
            em_dict={}
            with open(bet_json,"w+",encoding="utf-8") as f:
                dump(em_dict,f)
        self.update_count=0
        self.start=time.time()
        sleep(1)
        self.end=time.time()
        self.total_time=self.end-self.start
        from random import randint
        while self.total_time<2000:
            team_name_key=list(self.raybet().keys())
            json_of_current_sequence_ratio=self.raybet()
            print ("右赔率",json_of_current_sequence_ratio[self.r_team_name],flush=True)#["第二局胜者"]
            print ("左赔率",json_of_current_sequence_ratio[self.d_team_name],flush=True)#["第二局胜者"]
            keys1,keys2=team_name_key[0],team_name_key[1]
            sleep(randint(10,29))
            self.end=time.time()
            self.total_time=self.end-self.start
    def get_live_match_id(self,update_live_match=False):
        html_fname="buff_esport.html"
        if update_live_match==True:
            req_buff_object=get("https://www.dotabuff.com/esports",headers=self.dotabutff_headers)
            with open("buff_esport.html","w+",encoding="utf-8") as f:
                f.write(req_buff_object.text)
        if os.path.exists(html_fname):
            with open(html_fname,"r+",encoding="utf-8") as f:
                req_buff_text=f.read()
            bs4_buff_obj=BeautifulSoup(req_buff_text,"html.parser")
            live_links=[link["href"] for link in bs4_buff_obj.find_all("a",attrs={"rel":"tooltip"}) if "trackdota" in link["href"]]
            pattern=re.compile("(?<=match/)\d+")
            self.id_list=list(set(live_links))

CLEAR=False
if __name__ == '__main__':
    instance=Ban_Pick(crawl_banpick_url_id=False)
    # print (instance.get_vpgame())
    print (instance.get_vpgame())
    if CLEAR==True:
        instance.clear()

"""
var hosts = 'zkd.me develop.dog';
FiddlerApplication.Log.LogFormat("Logger session {0}, Url: {1}, isHttps: {2}, port: {3}", oSession.id, oSession.fullUrl, oSession.isHTTPS, oSession.port);
if(hosts.indexOf(oSession.host) > -1){
    FiddlerApplication.Log.LogFormat("Capture session {0}, Url: {1}, isHttps: {2}, port: {3}", oSession.id, oSession.fullUrl, oSession.isHTTPS, oSession.port);
    if(oSession.HTTPMethodIs('CONNECT')){
        FiddlerApplication.Log.LogString('create fake tunnel response');
        oSession['x-replywithtunnel'] = 'FakeTunnel';
        return;
    }

    if (oSession.isHTTPS){ 
        FiddlerApplication.Log.LogString('switch https to http request');
        oSession.fullUrl = oSession.fullUrl.Replace("https://","http://");
        oSession.port = 80;
    }   

    FiddlerApplication.Log.LogFormat("Processed session {0}, Url: {1}, isHttps: {2}, port: {3}", oSession.id, oSession.fullUrl, oSession.isHTTPS, oSession.port);
}
FiddlerApplication.Log.LogFormat("Logger session {0}, Url: {1}, isHttps: {2}, port: {3}", oSession.id, oSession.fullUrl, oSession.isHTTPS, oSession.port);
if(oSession.isHTTPS && oSession.url.indexOf(oSession.host)> -1){  
    oSession["ui-color"] = "blue";  
}  
if(!oSession.isHTTPS && oSession.url.indexOf(oSession.host)> -1){  
    oSession["ui-color"] = "green";  
}
"""