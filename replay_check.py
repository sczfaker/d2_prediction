from re import findall,compile,search
from fake_useragent import UserAgent
from json import load,dump,loads
from requests import get
from random import choice,randint
from time import sleep
from delorean import Delorean
import os

class REPLAY(object):
    def __init__(self):
        self.url_prefix="https://api.opendota.com/api/matches/"
        match_id_file="matchid_file_2020-09-11.txt"
        self.ua = UserAgent()
        self.headers={"user-agent":self.ua.random}
        with open(match_id_file,"r+",encoding="utf-8") as f:
            self.url_suffix_list=[i.strip() for i in f.readlines()]
        self.replay_path="promatch_replay/"
    def crawl_replay(self):
        fail_list=[]
        self.total_crawled_saved,self.already_crawled_iteration=0,0
        for match_id in self.url_suffix_list:
            one_match=get(self.url_prefix+match_id,headers=self.headers)
            # print (one_match_dict.status_code)
            fname="v0727_"+match_id+".dem.bz2"
            self.abs_path=self.replay_path+fname
            print (fname)
            if os.path.exists(self.abs_path):
                self.already_crawled_iteration+=1
                state="重复迭代"
                continue
            one_match_dict=loads(one_match.text)
            one_match_replay_bytes=get(one_match_dict["replay_url"],stream=True)
            print (one_match_dict["replay_url"])
            print(len(one_match_replay_bytes.content))
            if one_match_replay_bytes.status_code==200:
                try:
                    with open(self.abs_path,"wb") as f:
                        f.write(one_match_replay_bytes.content)
                    print (fname,"写入成功")
                    state="成功"
                    self.total_crawled_saved+=1
                except:
                    print ("fail-",match_id)
                    fail_list.append(fname)
                    state="失败"
                    continue
            rand_int=randint(1,3)
            with open("dem_log.log","a+",encoding="utf-8") as f:
                d = Delorean()
                d = d.shift('Asia/Shanghai')
                sp_time=d.datetime
                f.seek(0)
                print (match_id,state,len(fail_list),"此次成功文件数:",self.total_crawled_saved,"重复迭代数:",self.already_crawled_iteration,sp_time,file=f,flush=True)
            sleep(rand_int)
            state=None
        print (fail_list,len(fail_list))
if __name__ == '__main__':
    instance=REPLAY()
    instance.crawl_replay()
