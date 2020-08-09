from requests import get
from itertools import zip_longest
import sys,io
import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
import time
from time import localtime,strptime,mktime,strftime
from json import dump,load,loads
from time import sleep
import urllib3
urllib3.disable_warnings()
class TeamMate(object):
    """组队匹配"""
    def __init__(self):
        #super(ClassName, self).__init__()
        self.ateamplayers_id=""
        self.my_account = [226124774,140795989,178363403,494060230,876869481]
        self.prefix="https://api.opendota.com/api/"
        self.opendota_accountid_api=["players/%d","players/%d/matches","players/%d/recentMatches","players/%d/heroes","players/%d/peers","players/%d/totals","players/%d/counts","players/%d/rating"]
        self.backuplinks=["players/%d/histograms","players/%d/wardmap","players/%d/wardcloud"]
        self.headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
        self.TEAMATE_DATA="teamate_data"
        self.ehome_i={"","","","",""}
        self.vg_p={"","","","",""}
        self.UPDATE_MID_NORMAL_QUEUE=True
        self.MATCH_DIR_0727="./MATCH_JSON_DIR_0727/"
        self.aster_aries={"","","","",""}
        self.max_play_estimate=40
        self.query_ability="?limit=%d&game_mode=1"%(self.max_play_estimate)
        self.query_draft="?limit=%d&game_mode=3"%(self.max_play_estimate)
        self.query_allpick="?limit=%d&game_mode=22"%(self.max_play_estimate)
        self.time_limit="2020-07-17 08:54:01"#版本更新比赛的日期格式
        self.time_limit=time.mktime(time.strptime(self.time_limit,"%Y-%m-%d %H:%M:%S"))
        query_para=["limit",""]
    def __repr__(self):
        pass
    def my_account_data(self):
        for accountid in self.my_account[:]:
            fullurl=self.prefix+self.opendota_accountid_api[0]%(accountid)
            req_account_object=get(fullurl,headers=self.headers)
            with open(self.TEAMATE_DATA+'/'+str(accountid)+".json","w+",encoding="utf-8") as f:
                dump(req_account_object.text,f,ensure_ascii=False)
                print("ok")
            fullurl_matches_allpick=self.prefix+self.opendota_accountid_api[1]%(accountid)+self.query_allpick
            fullurl_matches_draft=self.prefix+self.opendota_accountid_api[1]%(accountid)+self.query_draft
            fullurl_matches_ability=self.prefix+self.opendota_accountid_api[1]%(accountid)+self.query_ability


            req_account_allpick=get(fullurl_matches_allpick,headers=self.headers)
            req_account_draft=get(fullurl_matches_draft,headers=self.headers)
            req_account_ability=get(fullurl_matches_ability,headers=self.headers)
            with open(self.TEAMATE_DATA+'/matches_'+str(accountid)+"_allpick.json","w+",encoding="utf-8") as f,open(self.TEAMATE_DATA+'/matches_'+str(accountid)+"_draft.json","w+",encoding="utf-8") as f1,open(self.TEAMATE_DATA+'/matches_'+str(accountid)+"_ability.json","w+",encoding="utf-8") as f2:
                dump(req_account_allpick.text,f,ensure_ascii=False)
                dump(req_account_draft.text,f1,ensure_ascii=False)
                dump(req_account_ability.text,f2,ensure_ascii=False)
                print("ok matches")
    def query_my_account(self):
        for accountid in self.my_account[1:2]:
            with open(self.TEAMATE_DATA+'/matches_'+str(accountid)+"_allpick.json","r+",encoding="utf-8") as f,open(self.TEAMATE_DATA+'/matches_'+str(accountid)+"_draft.json","r+",encoding="utf-8") as f1,open(self.TEAMATE_DATA+'/matches_'+str(accountid)+"_ability.json","r+",encoding="utf-8") as f2:
                d1=load(f)
                d2=load(f1)
                d3=load(f2)
                d1=d1.replace("\\","").replace("true","True").replace("null","0").replace("false","False")
                d2=d2.replace("\\","").replace("true","True").replace("null","0").replace("false","False")
                d3=d3.replace("\\","").replace("true","True").replace("null","0").replace("false","False")
                d1_allpick=eval(d1)
                d2_draft=eval(d2)
                d3_ability=eval(d3)
                print (accountid,len(d1_allpick),len(d2_draft),len(d3_ability))
                for i in d3_ability:
                    print (i)
    def get_account_friend(self):
        for suffix in self.opendota_accountid_api:
            for accountid in self.my_account[:]:
                fullurl=(self.prefix+suffix)%(accountid)
                print (fullurl)
                s=get(fullurl,headers=self.headers)
                print (s.status_code)
                if s.status_code==200:
                    print (len(s.text))
                    suffix_jsonfilename=fullurl.split("/")[-1]
                    print(suffix_jsonfilename)
                    if os.path.exists(self.TEAMATE_DATA)==False:
                        os.mkdir(self.TEAMATE_DATA)
                    with open(self.TEAMATE_DATA+"/"+str(accountid)+"_"+suffix_jsonfilename+".json","w+",encoding="utf-8") as f_teamate:#open("myaccount.json","w+",encoding="utf-8") as f_a:
                        dump(s.text,f_teamate,ensure_ascii=False)
                        print ("ok",suffix_jsonfilename)
                        sleep(1)
    def get_highskill_recent_match_id(self):
        with open ("team_and_player.json","r+",encoding="utf-8") as f:
            dic_dota2_id=load(f)
        count_total,limit=0,10
        self.count=0
        self.add_count=0
        list_random=[]
        list_all=[]
        # self.headers = {'Host': 'api.opendota.com', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.88 Safari/537.36 Vivaldi/2.4.1488.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9'}
        self.headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
        # self.cookies = {'_ga': 'GA1.2.654318434.1592888382', '__cfduid': 'd6eccdc8731914f51dde26e1717f02e611593764220', '_gid': 'GA1.2.61074614.1593764226'}
        f=False
        with open("normal_match_info.json","r+",encoding="utf-8") as f:
            dict_match_id=load(f)
        if True:
            for team in dic_dota2_id:
                current_team_total=0
                # if team not in dict_match_id:
                #     dict_match_id[team]={}
                if team not in dict_match_id:
                    dict_match_id[team]={}
                for one_id in dic_dota2_id[team]:
                    dict_match_id[team][one_id]=[]                   
                    url_allpick=(self.prefix+self.opendota_accountid_api[1]+self.query_allpick)%(int(one_id))
                    url_randomdraft=(self.prefix+self.opendota_accountid_api[1]+self.query_draft)%(int(one_id))
                    print (url_allpick,url_randomdraft)
                    try:
                        req_object_allpick=get(url_allpick,headers=self.headers,verify=False,timeout=30)
                        d1=req_object_allpick.text
                        d1=d1.replace("\\","").replace("true","True").replace("null","0").replace("false","False")
                        d1_allpick=eval(d1)
                        print ("格式化成功比赛长度:",len(d1_allpick))
                        sleep(0.5)
                    except:
                        print (one_id,"全英雄选择格式化错误")
                        continue
                    try:
                        req_object_randomdraft=get(url_randomdraft,headers=self.headers,verify=False,timeout=30)
                        d2=req_object_randomdraft.text              
                        d2=d2.replace("\\","").replace("true","True").replace("null","0").replace("false","False")
                        d2_draft=eval(d2)
                        print ("格式化成功比赛长度:",len(d2_draft))
                        sleep(0.5)
                    except:
                        print (one_id,"随机征召错误")
                        continue
                    #print (req_object_allpick.encoding,req_object_randomdraft.encoding)
                        # dict_match_id
                    try:
                        if one_id in dict_match_id[team]:
                            list_of_match=dict_match_id[team][one_id]
                            cur_len=len(list_of_match)
                            for one_allpick,one_draft in zip_longest(d1_allpick,d2_draft,fillvalue=0):
                                if one_allpick and type(one_allpick)==dict:
                                    # print ("数据正常:",type(one_allpick))
                                    mid_all,start_time_all=one_allpick["match_id"],one_allpick["start_time"]
                                    value=[mid_all,start_time_all]
                                    if value not in list_of_match:
                                        list_of_match.append(value)
                                        self.add_count+=1
                                    # mid_all,start_time_all,rpicks,dpicks,game_mode,avg_mmr,radiant_win,duration=one_allpick["match_id"],one_allpick["start_time"],one_allpick["radiant_team"],one_allpick["dire_team"],one_allpick["game_mode"],one_allpick["avg_mmr"],one_allpick["radiant_win"],one_allpick["duration"]
                                    # list_of_match.append([mid_all,start_time_all,rpicks,dpicks,game_mode,avg_mmr,radiant_win,duration])
                                    # print (strftime("%Y-%m--%d %H:%M:%S",localtime(start_time_all)))
                                    self.count+=1
                                else:
                                    continue
                                if one_draft and type(one_draft)==dict:
                                    # print ("数据正常:",type(one_draft))
                                    mid_draft,start_time_draft=one_draft["match_id"],one_draft["start_time"]
                                    value=[mid_draft,start_time_draft]
                                    if value not in list_of_match:
                                        list_of_match.append(value)
                                        self.add_count+=1
                                    self.count+=1
                                else:
                                    continue
                                # mid_draft,start_time_draft,rpicks,dpicks,game_mode,avg_mmr,radiant_win,duration=one_draft["match_id"],one_draft["start_time"],one_draft["radiant_team"],one_draft["dire_team"],one_draft["game_mode"],one_draft["avg_mmr"],one_draft["radiant_win"],one_draft["duration"]
                                # list_of_match.append([mid_draft,start_time_draft,rpicks,dpicks,game_mode,avg_mmr,radiant_win,duration])
                                # print (strftime("%Y-%m--%d %H:%M:%S",localtime(start_time_draft)))
                            if cur_len!=len(list_of_match):
                                print ("此id",one_id,"新增比赛:",len(list_of_match)-cur_len)
                                with open("playerid_count.txt","a+",encoding="utf-8") as f:
                                    f.seek(0)
                                    f.write(one_id+str(len(list_of_match))+str(curlen)+"\n")
                                dict_match_id[team][one_id]=list_of_match
                            print (team,"此id当前的比赛总长度",len(list_of_match))
                            current_team_total+=len(list_of_match)
                    except:
                        print ("数据不正常显示:",one_id,one_allpick,one_draft)
                        #assert 1>2,"需要检查为什么不正常"
                        continue
                    #print (type(d1_allpick),type(d2_draft))
                    # list_all+=d1
                    # list_random+=d2
                print (team,"队员 的 最近比赛总长度:",current_team_total,)
            print ("最近比赛总长度:",self.count,"新增比赛总长度",self.add_count)
            with open("normal_match_info.json","w+",encoding="utf-8") as f,open("normal_match_count.txt","a+",encoding="utf-8") as f_0:
                f_0.seek(0)
                f_0.write(str(datetime.date.today())+":"+str(self.count)+"\n")
                dump(dict_match_id,f,ensure_ascii=False)
    def save_to_queue(self):
        with open ("normal_match_info.json","r+",encoding="utf-8") as f:
            dict_match=load(f)
        with open(self.MATCH_DIR_0727+"queue_normal.txt","a+",encoding="utf-8") as f:
            f.seek(0)
            queue_list=f.readlines()
        self.outdate=0
        self.repeated=0
        new_id=[]
        for team in dict_match:
            for pid in dict_match[team]:
                for id_and_time in dict_match[team][pid]: 
                    try:
                        if len(id_and_time)==2 and self.htmltime_to_strptime(id_and_time[1]):
                            if str(id_and_time[0])+"\n" not in queue_list:
                                queue_list.append(str(id_and_time[0]))
                                new_id.append(str(id_and_time[0])+"\n")
                            else:
                                self.repeated+=1
                        else:
                            self.outdate+=1
                    except:
                        print ("one id_and_time illeagal")
                        continue
            print ("当前合法id长度",len(new_id),"quelist",len(queue_list))
        print ("新增长度:",len(new_id),"总长度:",len(queue_list),"过期比赛:",self.outdate)
        with open(self.MATCH_DIR_0727+"queue_normal.txt","a+",encoding="utf-8") as f:
            f.seek(0)
            f.writelines(new_id)
    def htmltime_to_strptime(self,one_time_match):
        """time format 时间格式"""
        if one_time_match>self.time_limit:
            return True
        else:
            return False

if __name__ == '__main__':
    instance=TeamMate()
    #x.my_account_data()
    print (instance.time_limit)
    instance.get_highskill_recent_match_id()
    instance.save_to_queue()
    # x.query_my_account()