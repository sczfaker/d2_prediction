from fake_useragent import UserAgent
from json import dump,load,loads
from random import randint
from requests import get
from time import sleep
import datetime
import os
import re
MATCH_JSON_DIR="MATCH_JSON_DIR_0727"

if os.path.exists(MATCH_JSON_DIR)==False:
    os.mkdir(MATCH_JSON_DIR)
url="https://api.opendota.com/api/publicMatches?less_than_match_id="
class OpendotaReq(object):
    """docstring for ClassName"""
    def __init__(self):
        #super(ClassName, self).__init__()
        self.ua = UserAgent()
        self.matchurl = "https://api.opendota.com/api/matches/"
        #self.playerurl = "https://api.opendota.com/api/players/"
        self.headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
        self.heroes="https://api.opendota.com/api/heroes"
        self.teams_id="https://api.opendota.com/api/teams/"
        self.teamid="https://api.opendota.com/api/teams/"
        self.teamid="https://api.opendota.com/api/226124774/"
        self.teamid="https://api.opendota.com/api/226124774/"    
        self.headers={"user-agent":self.ua.random}
        self.path="W:/cl/req_gamesportsdata/MATCH_JSON_DIR_0727/queue_0727.txt"
        with open(self.path,"r+",encoding="utf-8") as f:
            self.matchid_0727=f.read().split("\n")[:-1]
    def match_info(self,matchid):
        s=get(self.matchurl+matchid,headers=self.headers)
        print (s.status_code)
        if s.status_code==200:
            print (len(s.text))
            return s.text
    def account_info(self,accountid):
        s=get(self.playerurl+accountid,headers=self.headers)
        return s.text
    def get_hero_id(self):
        s=get(self.heroes,headers=self.headers)
        print (s.text)
        d=load(s.text)
        print (type(d))
        if s.status_code==200:
            with open (MATCH_JSON_DIR+"/"+"heroes_id.json","w+",encoding="utf-8") as f:
                dump(f,d,ensure_ascii=False)
        print (d)
    def get_team_id(self):
        s=get(self.teamid,headers=self.headers)
        d=loads(s.text)
        if s.status_code==200:
            with open (MATCH_JSON_DIR+"/"+"team_id.json","w+",encoding="utf-8") as f:
                dump(f,d,ensure_ascii=False)
        print (d,len(d))        
    def stats_queue(self,f):
        with open(f,"r+",encoding="utf-8") as f:
            fl=set(f.readlines())
        return len(fl)
    def check(self):
        self.clean_banpic_match_json=0
        self.clean_banpic_match_txt=0
        self.no_radiant_team_count=0
        self.leagal_txt=0
        self.folder_info={"normalmatch.json":0,"professional_match":0,"already_crawled_profess":0,"wait_crawl_json_normal":0,"crawled_json_normal":0,"wait_crawl_json_profess":0,"normalmatch_html_txt_uncheck":0}
        for file in os.listdir(MATCH_JSON_DIR+"/"):
            if re.match("normalmatch_\d{5,}.json",file):
                self.folder_info["normalmatch.json"]+=1
                with open(MATCH_JSON_DIR+"/"+file,"r+",encoding="utf-8") as f:
                    dict_match=load(f)
                    try:
                        # print (dict_match["radiant_team"])
                        if dict_match["radiant_team"] and len(dict_match["radiant_team"].split(","))==5:
                            self.clean_banpic_match_json+=1
                    except:
                        self.no_radiant_team_count+=1
                        continue
            if re.match("\d{5,}.json",file):
                self.folder_info["professional_match"]+=1
            if file=="queue_0727.txt":
                self.folder_info["already_crawled_profess"]=self.stats_queue(MATCH_JSON_DIR+"/"+file)
            if file=="queue_normal.txt":
                self.folder_info["wait_crawl_json_normal"]=self.stats_queue(MATCH_JSON_DIR+"/"+file)
            if file=="already_crawled_normal.txt":
                self.folder_info["crawled_json_normal"]=self.stats_queue(MATCH_JSON_DIR+"/"+file)
            if True:
                f="matchid_file_"+str(datetime.date.today())+".txt"
                self.folder_info["wait_crawl_json_profess"]=self.stats_queue(f)
            if re.match("normalmatch_\d{5,}.txt",file):
                self.folder_info["normalmatch_html_txt_uncheck"]+=1
                if os.stat(MATCH_JSON_DIR+"/"+file).st_size>5000:
                    self.clean_banpic_match_txt+=1
    def queue_repeat(self,file):
        with open(MATCH_JSON_DIR+"/"+file,"r+",encoding="utf-8") as f:
            fl=list(set(f.readlines()))
        with open(MATCH_JSON_DIR+"/"+"queue_normal.txt","w+",encoding="utf-8") as f:
            for i in fl:
                f.write(i)
MATCH_MISS=True
QUEUE_MISS=True
NORMAL_QUEUE_MISS=False
instance=OpendotaReq()
if False:
    instance.get_team_id()
if False:
    instance.get_hero_id()
if MATCH_MISS:
    with open("matchid_file_"+str(datetime.date.today())+".txt","r+") as f:
        matchid=[i.strip() for i in f.readlines()]
        print (len(matchid))
    num=0
    fail_id_list=[]    
    if QUEUE_MISS:
        with open (MATCH_JSON_DIR+"/"+"queue_0727.txt","a+") as f:
            f.seek(0)
            queue_list=[i.strip() for i in f.readlines()]
            matchid=[mid for mid in matchid if mid not in instance.matchid_0727]
            if False:
                for mid in matchid:
                    f.write(mid+"\n")
            if MATCH_MISS:
                for m_id in matchid:
                    match_dict={}
                    if m_id not in queue_list:
                        try:
                            match_str=instance.match_info(m_id)
                            match_dict=loads(match_str)
                            sleep(randint(1,3))
                        except:
                            fail_id_list.append(m_id)
                            num+=1
                            print("fail:",num)
                            continue
                        if match_dict:
                            with open(MATCH_JSON_DIR+"/"+m_id+".json","w+",encoding="utf-8") as f_0:#open("myaccount.json","w+",encoding="utf-8") as f_a:
                                dump(match_dict,f_0,ensure_ascii=False)
                                print (m_id+" ok")
                                queue_list.append(m_id)
                                f.write(m_id+"\n")
                    else:
                        print ("already in queue.")
fail_normal_list=[]
num=0
count_match=0
if NORMAL_QUEUE_MISS:
    instance.queue_repeat("queue_normal.txt")
    with open (MATCH_JSON_DIR+"/queue_normal.txt","r+",encoding="utf-8") as f:
        match_id=[mid.strip() for mid in f.readlines()]
    if False:
        with open (MATCH_JSON_DIR+"/queue_normal.txt","w+",encoding="utf-8") as f:
            f.writelines(match_id)
    print("待获取长度:",len(set(match_id)),len(match_id))
    with open (MATCH_JSON_DIR+"/already_crawled_normal.txt","a+",encoding="utf-8") as f:
        f.seek(0)
        already_match_id=[mid.strip() for mid in f.readlines()]
        for mid in match_id:
            if mid not in already_match_id:
                try:
                    match_str=instance.match_info(mid)
                    match_dict=loads(match_str)
                    print("not good")
                    sleep(randint(1,3))
                except:
                    fail_normal_list.append(mid)
                    num+=1
                    print("fail:",num)
                    continue
                print("转换成字典后的长度",len(match_dict))        
                if match_dict:
                    with open(MATCH_JSON_DIR+"/"+"normalmatch_"+mid+".json","w+",encoding="utf-8") as f_0:#open("myaccount.json","w+",encoding="utf-8") as f_a:
                        dump(match_dict,f_0,ensure_ascii=False)
                        print (mid+" ok",count_match)
                        count_match+=1
                        already_match_id.append(mid)
                        f.write(mid+"\n")
            else:
                print ("already in queue.")
CHECK_JSON_QUEUELINE_TXT=True
if CHECK_JSON_QUEUELINE_TXT==True:
    instance.check()
    for i in instance.folder_info:
        print (i,instance.folder_info[i])
    print ("total_json:",instance.clean_banpic_match_json)
    print ("legal_txt:",instance.clean_banpic_match_txt)
    print ("illeagal_Json:",instance.no_radiant_team_count)
    #account_str=t.account_info("226124774")
    #account_dict=loads(account_str)
#assert 1>2+#2print (s,s1)

        #dump(account_dict,f_a,ensure_ascii=False)
# if True:
#   with open("data.json","r+",encoding="utf-8") as f,open("myaccount.json","r+",encoding="utf-8") as f_a:
#       s=load(f)
#       s1=load(f_a)
#   for i in s:
#       print (i)
