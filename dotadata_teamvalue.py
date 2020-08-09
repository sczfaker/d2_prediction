import sys,io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
from fake_useragent import UserAgent
from re import findall,compile,match
from os import chdir,listdir,rename
from re import findall,compile
from json import load,dump,loads
from bs4 import BeautifulSoup
from requests import get
from pandas import DataFrame
from time import sleep
from random import randint
from json import dump,load
import datetime
import requests
import os
import re

class TeamValue(object):#除了阵容外的胜率a+b/2 上限容易计算 下限难计算一点
    def __init__(self):
        self.ip_other=self.get_proxy()
        self.proxie={'http':self.ip_other}
        self.CREATE_DICT_TEAM_PLAYERID=True
        self.match_catalog="MATCH_JSON_DIR_0727"
        self.ua = UserAgent()
        self.prefix_team="https://www.dotabuff.com/esports/teams"
        self.prefix_team="http://dotamax.com/match/tour_famous_team_list/"
        month_suffix_update="".join(str(datetime.date.today()).split("-")[0:2])
        self.tourpreview_filename="Tournaments_Preview_"+month_suffix_update+".json"
        self.headers={"User-Agent":self.ua.random,"Accept-Encoding":"gzip"}
        self.rigth_count,need_to_fix=0,[]
        self.real_match={}
        self.teamid_to_name={}
        self.game_version="0727"
    def get_proxy(self):
        PROXY_POOL_URL="http://localhost:5555/random"
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            return None
    def get_lp_person_info(self,url,game_name):
        self.folder_name="player_html/"
        full_path_name=self.folder_name+game_name+".txt"
        if os.path.exists(full_path_name)==False or (os.path.exists(full_path_name)==True and os.stat(full_path_name).st_size<1e4):
            try:
                self.headers={"User-Agent":self.ua.random,"Accept-Encoding":"gzip"}#"LiveScoresBot/1.0(scz526600266@gmail.com)"
                self.ip_other=self.get_proxy()
                self.proxie={'http':self.ip_other}
                randint_num=randint(randint(1,4),randint(6,16))
                print ("休息",randint_num,"秒",flush=True)
                sleep(randint_num)
                req_object=requests.get(url,headers=self.headers,proxies=self.proxie,timeout=30)
                with open(full_path_name,"w+",encoding="utf-8") as f:
                    f.write(req_object.text)
                return -1
            ana_info={}
            with open(full_path_name,"r+",encoding="utf-8") as f:
                person_text=f.read()
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
                    return -1
        else:
            return -1
    def get_current_partici_liquidpedia(self):
        prefix="https://liquipedia.net"
        update_url_html=True
        self.tour_url_togetteam=[]
        if os.path.exists("current_p_team.json"):
            with open("current_p_team.json","r+",encoding="utf-8") as f:
                current_p_team=load(f)
        else:
            with open("current_p_team.json","w+",encoding="utf-8") as f:
                current_p_team={}
        # with open("Tournaments_Preview.json","r+",encoding="utf-8") as f:    
        with open(self.tourpreview_filename,"r+",encoding="utf-8") as f:
            dict_tournament=load(f)
        # print (dict_tournament,len(dict_tournament))
        dict_tournament.pop("upcoming")
        for time_state_tour in dict_tournament:
            for one_tourna in dict_tournament[time_state_tour]:
                price=dict_tournament[time_state_tour][one_tourna]["pricepoul"]
                print (one_tourna,price,type(price))
                if price>1000:
                    self.tour_url_togetteam.append([dict_tournament[time_state_tour][one_tourna]["url"],price,one_tourna])
        self.tour_url_togetteam.sort(key=lambda x:x[1])                
        # print (self.tour_url_togetteam,len(self.tour_url_togetteam))
        dict_recent_earn={}
        team_earn_list=[]
        for match_num,one_tour_url in enumerate(self.tour_url_togetteam):
            # print ("url:",one_tour_url[0],flush=True)
            print("目标数据结构长度:",len(dict_recent_earn),len(team_earn_list))
            match_file_name=str(match_num)+"_"+one_tour_url[2]+"_"+str(one_tour_url[1])+".txt"
            match_file_name=match_file_name.replace(":","_")
            match_file_name=match_file_name.replace("/","_")
            match_file_name=match_file_name.replace(" ","_")
            if update_url_html==True:
                try:
                    self.headers={"User-Agent":self.ua.random,"Accept-Encoding":"gzip"}#"LiveScoresBot/1.0(scz526600266@gmail.com)"
                    self.ip_other=self.get_proxy()
                    self.proxie={'http':self.ip_other}
                    # print (match_file_name,flush=True)
                    if os.path.exists(match_file_name)==False or (os.path.exists(match_file_name)==True and os.stat(match_file_name).st_size<1e4):
                        randint_num=randint(randint(1,3),randint(3,10))
                        # print ("休息",randint_num,"秒",flush=True)
                        sleep(randint_num)
                        req_object=requests.get(one_tour_url[0],headers=self.headers,proxies=self.proxie,timeout=30)
                        with open(match_file_name,"w+",encoding="utf-8") as f:
                            f.write(req_object.text)
                        print("write new page ok.") 
                except:
                    print ("cant crawl")
                    continue
            with open(match_file_name,"r+",encoding="utf-8") as f:
                one_tour_text=f.read()
            bs4_obejct=BeautifulSoup(one_tour_text,"html.parser")
            p_object=bs4_obejct.find("div",attrs={"style":re.compile("max-width:\d{3,4}px;")})#max-width:1200px;
            if p_object:
                team_list=p_object.find_all("div",class_="template-box")
                for team_div in team_list:
                    player_dict={}
                    try:
                        team_name=team_div.find("center").b.get_text().strip()
                        team_url=prefix+team_div.find("center").b.a["href"]
                        team_fname=team_name+".txt"
                        print("队伍url到底对不对???",team_url,flush=True)
                        if len(team_url.split("/")[-1])>30:
                            continue
                        try:
                            if os.path.exists("teaminfo/")==False:
                                os.mkdir("teaminfo")
                            if os.path.exists("teaminfo/"+team_fname)==False:
                                team_text=get(team_url,headers=self.headers,timeout=60)
                                with open("teaminfo/"+team_fname,"w+",encoding="utf-8") as f:
                                    f.write(team_text.text)                                
                            else:
                                with open("teaminfo/"+team_fname,"r+",encoding="utf-8") as f:
                                    team_text=f.read()
                                    bs4_team_object=BeautifulSoup(team_text,"html.parser")
                                    flag_money_info_true=bs4_team_object.prettify().find("Total Earnings:")
                                    if flag_money_info_true:
                                        div_total_money=bs4_team_object.find("div",class_="fo-nttax-infobox-wrapper infobox-dota2")
                                        if div_total_money:
                                            pattern="\$(\d|,).*"
                                            earn_str_tag=div_total_money.find("div",text=compile(pattern))
                                            str_money=earn_str_tag.get_text()
                                            print (str_money,flush=True)
                                            team_info=[team_name,str_money,team_url]
                                            if team_info not in team_earn_list:
                                                team_earn_list.append(team_info)
                                            if team_name not in dict_recent_earn:
                                                dict_recent_earn[team_name]=1
                                            else:
                                                dict_recent_earn[team_name]+=1
                                    else:
                                        print (team_name,":队伍无信息?")
                        except:
                            assert 1>2,"队伍页面无法抓取..."
                        # print ("队伍页面!!!:",team_text.text,len(team_text))
                        continue
                        team_mate_tag_list=team_div.find_all("tr")[:5]
                        for position_to_str,info in enumerate(team_mate_tag_list):
                            link_tag_list=info.find_all("a")
                            if len(link_tag_list)==2:
                                country,person=link_tag_list[0],link_tag_list[1]
                                lp_person_url=prefix+person["href"]
                                game_virtual_id=person.get_text().strip()
                                lp_country_url=prefix+country["href"]
                                analyze_info=self.get_lp_person_info(lp_person_url,game_virtual_id)
                                player_dict[position_to_str]={"game_id":game_virtual_id,"url":lp_person_url,'country':lp_country_url,"outlink_info":analyze_info}
                            else:
                                assert 1/0,"one name tag with wrong lenth"
                        # print ("队伍",team_name,flush=True)
                        if team_name in current_p_team and not current_p_team[team_name]["current_state"]["teammate"]:
                            if {one_tourna:price,"result":{"award":0,"pos":0}} not in current_p_team["parti"]:
                                current_p_team[team_name]["parti"].append({one_tourna:price,"result":{"award":0,"pos":0}})
                        else:
                            if analyze_info!=-1:
                                current_p_team[team_name]={"parti":[{one_tourna:price,"result":{"award":0,"pos":0}}],"bp_before_value":0,"current_state":{"teammate":player_dict,"manager_mate":{"data_analyze":{},"coach":{},"teamguide":{}}},"past_state":{},"future_state":{}}
                            elif analyze_info==-1:
                                try:
                                    self.lqd_team_info="/crawl_log/lqd_team_info.log"
                                except:
                                    continue
                    except:
                        assert 1>2,'??'
                        print ("fail geting team earn:",team_name,flush=True)
            else:
                print (match_file_name,"tour cannot crawl")
                continue
        pd_object=DataFrame(team_earn_list,columns=["team_name","str_money","team_url"])
        pd_object.to_csv("team_earn.csv",index=False)
        with open("team_parti_json.json","w+",encoding="utf-8") as f:
            dump(dict_recent_earn,f,ensure_ascii=False)
        with open("current_p_team.json","w+",encoding="utf-8") as f:
            dump(current_p_team,f,ensure_ascii=False)
    def Tournament_preview(self):
        update_mainpage=True
        month_suffix_update="".join(str(datetime.date.today()).split("-")[0:2])
        if os.path.exists(self.tourpreview_filename):
            import shutil
            match_info_cache="old_match_info"
            outdate_filename="oldmatchinfo_"+self.tourpreview_filename
            os.rename(self.tourpreview_filename,outdate_filename)
            if os.path.exists(match_info_cache):
                shutil.move(outdate_filename,match_info_cache+"\\"+outdate_filename)
            else:
                os.mkdir(match_info_cache)
                shutil.move(outdate_filename,match_info_cache+"\\"+outdate_filename)
            dict_tournament={"ongoing":{},"upcoming":{},"recent":{}}
        else:
            with open(self.tourpreview_filename,"w+",encoding="utf-8") as f:
                dict_tournament={"ongoing":{},"upcoming":{},"recent":{}}
        tournament_page_html=str(datetime.date.today()).replace("-","_")+"tournament_page"    
        if update_mainpage:
            self.tournament_page="https://liquipedia.net/dota2/Portal:Tournaments"
            req_object=requests.get(self.tournament_page,headers=self.headers,proxies=self.proxie,timeout=60)
            with open(tournament_page_html+".txt","w+",encoding="utf-8") as f:
                f.write(req_object.text)
                print("write new page ok.")
        with open(tournament_page_html+".txt","r+",encoding="utf-8") as f:
            bs4_obejct=BeautifulSoup(f.read(),"html.parser")
            upcoming_ongogin=bs4_obejct.find_all("h3")
            print (len(upcoming_ongogin))
            upcoming_ongogin_tag=[]
            for tag in upcoming_ongogin[:3]:
                table=tag.next_sibling.next_sibling
                upcoming_ongogin_tag.append(table.div)
        #print (len(upcoming_ongogin_tag),upcoming_ongogin_tag)
        prefix="https://liquipedia.net"
        for type_tag,tag in enumerate(upcoming_ongogin_tag):
            div_row=tag.find_all("div",class_="divRow")
            div_hea=tag.find("div",class_="divHeaderRow")
            title_list=div_hea.find_all("divCell")
            print ("已经结束|正在进行|未来:",len(div_row))
            print (type_tag)
            for one_row in div_row:
                dict_info_tour={}
                one_attr_list=one_row.find_all("div",class_=re.compile("divCell.{10,}"))
                tournament_headtag=one_attr_list[0].find("b").find("a")
                tournament_link,title=tournament_headtag["href"],tournament_headtag.get_text()
                full_url=prefix+tournament_link
                print (full_url)
                date=one_attr_list[1].get_text()
                pricepoul=one_attr_list[2].get_text()
                pricepoul="".join(pricepoul[1:].split(","))
                # print ("金额:",pricepoul)
                if pricepoul:
                    pricepoul=int(pricepoul)
                else:
                    pricepoul=0
                # print (pricepoul)
                team_num=one_attr_list[3].get_text()
                location=one_attr_list[4].span.get_text()
                dict_info_tour["date"]=date
                dict_info_tour["pricepoul"]=pricepoul
                dict_info_tour["team_num"]=team_num
                dict_info_tour["location"]=location
                dict_info_tour["url"]=full_url
                if type_tag==0:
                    dict_tournament["upcoming"][title]=dict_info_tour
                elif type_tag==1:
                    dict_tournament["ongoing"][title]=dict_info_tour
                elif type_tag==2:
                    dict_tournament["recent"][title]=dict_info_tour

        # print (len(dict_tournament["upcoming"]),len(dict_tournament["ongoing"]),len(dict_tournament["recent"]))
        with open(self.tourpreview_filename,"w+",encoding="utf-8") as f:
            dump(dict_tournament,f,ensure_ascii=False)
    def get_teamid_tostr(self,rtid,dtid):
        urlprefix="https://api.opendota.com/api/teams/"
        if rtid not in self.teamid_to_name:
            req_object_1=get(urlprefix+str(rtid),headers=self.headers)
            self.teamid_to_name[rtid]={}
            self.teamid_to_name[rtid]['fullname']=""
            if req_object_1.status_code==200:
                try:
                    rname=loads(req_object_1.text)["name"]
                except:
                    print("load error")
                self.teamid_to_name[rtid]['fullname']=rname
            self.teamid_to_name[rtid]['winlose']={"win":0,'lose':0}
        if dtid not in self.teamid_to_name:
            req_object_2=get(urlprefix+str(dtid),headers=self.headers)
            self.teamid_to_name[dtid]={}
            self.teamid_to_name[dtid]['fullname']=""
            if req_object_2.status_code==200:
                try:
                    dname=loads(req_object_2.text)["name"]
                except:
                    print("load error")
                self.teamid_to_name[dtid]['fullname']=dname
            self.teamid_to_name[dtid]['winlose']={"win":0,'lose':0}
        print ("afight with team record",len(self.teamid_to_name))
        sleep(1)
    def create_team_dict(self):
        for match in self.real_match:
            rtid=self.real_match[match]['dire_team_id']
            dtid=self.real_match[match]['radiant_team_id'] 
            self.get_teamid_tostr(rtid,dtid)
            rad_winlose=self.real_match[match]["radiant_win"]
            if rad_winlose:
                winid=self.real_match[match]["radiant_team_id"]
                loseid=self.real_match[match]["dire_team_id"]
            else:
                loseid=self.real_match[match]["radiant_team_id"]
                winid=self.real_match[match]["dire_team_id"]
            self.teamid_to_name[winid]["winlose"]["win"]+=1
            self.teamid_to_name[loseid]["winlose"]["lose"]+=1
        with open("teamid_to_name_"+self.game_version+".json","w+",encoding="utf-8") as f:
            dump(self.teamid_to_name,f,ensure_ascii=False)
    def other_stats(self):
        with open("teamid_to_name_"+self.game_version+".json","r+",encoding="utf-8") as f:
            self.full_team_dic=load(f)
        for i in self.full_team_dic:
            total=self.full_team_dic[i]["winlose"]["win"]+self.full_team_dic[i]["winlose"]["lose"]
            self.full_team_dic[i]["winlose"]["total"]=total
            self.full_team_dic[i]["winrate"]=self.full_team_dic[i]["winlose"]["win"]/self.full_team_dic[i]["winlose"]["total"]
        with open("teamid_to_name_"+self.game_version+".json","w+",encoding="utf-8") as f:
            dump(self.full_team_dic,f,ensure_ascii=False)
    def visulize_team_winlose(self):
        with open("teamid_to_name_"+self.game_version+".json","r+",encoding="utf-8") as f:
            self.full_team_dic=load(f)
        list_fullteam=self.full_team_dic.items()
        totalgame_sort=[i for i in sorted(list_fullteam,key=lambda x:x[1]["winlose"]["total"],reverse=True) if i[1]["winlose"]["total"]>=10]
        winrate_sort=[i for i in sorted(list_fullteam,key=lambda x:x[1]["winrate"],reverse=True) if i[1]["winlose"]["total"]>=10]
        for team in winrate_sort:
            print (team)
    def sum_of_allteam(self):
        with open ("team_and_player.json","r+",encoding="utf-8") as f:
            dict_teamplayer=load(f)
        total=sum([len(dict_teamplayer[team]) for team in dict_teamplayer])
        for team in dict_teamplayer:
            print (dict_teamplayer,dict_teamplayer[team])
        return total
    def team_players(self):
        #headers = {'Host': 'www.dotabuff.com', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.88 Safari/537.36 Vivaldi/2.4.1488.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'https://www.dotabuff.com/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9'}
        #cookies url = 'http://dotamax.com/accounts/login/'
        self.pagelimit=10
        self.nextpage=False
        self.url_login="http://dotamax.com/accounts/login/"
        headers = {'Host': 'dotamax.com', 'Connection': 'keep-alive', 'Content-Length': '1335', 'Cache-Control': 'max-age=0', 'Origin': 'http://dotamax.com', 'Upgrade-Insecure-Requests': '1', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.88 Safari/537.36 Vivaldi/2.4.1488.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'http://dotamax.com/accounts/logout/?src=bets', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9'}
        cookies = {'_ga': 'GA1.2.917068991.1593764201', '_gid': 'GA1.2.981710910.1593764201', 'Hm_lvt_575895fe09d48554a608faa5ef059555': '1593764202', 'csrftoken': 'PP0Xh0PvPbiSWlk7tzkeVaJf7Cc9gUPe', '_gat': '1', 'Hm_lpvt_575895fe09d48554a608faa5ef059555': '1593768133'}
        data = {'csrfmiddlewaretoken': 'PP0Xh0PvPbiSWlk7tzkeVaJf7Cc9gUPe', 'phoneNumCipherb64': 'UI0XFR3urBNVZ2ZhsAP6fdKLZQqmCW13D4m3Ol0vAcpcSi4V8mU9k4T%2Bzw%2FLlDsE%0D%0A65LU0FXmRQFiSbgIwh%2FU%2F%2BNtI%2F2t0ULb8Pj29S%2BOwbCTzVdAu1kIEuNPOFIKllMy%0D%0ATvJ9MQLnw22CPRWWZIGY5QEPZPAgpwsk%2FftrmQ4QmL3X%2BU0PiJ1bBE0rXt8N%2BHXN%0D%0AEZaZ97w1En2umsVdwk4lSZrS%2Fg4iB%2Bgi82bwAx8oWIaL%2FHRBuFqxFYa1iCS4T6S9%0D%0AFf0bDFMMYdKvatLAvnnCP1HIwMOYPSddHgfOvVFLOdvm3Uo00vu%2Fh9ELNzHR%2Fz4g%0D%0AGKn5nlrcGyx3di1FR2sQMA%3D%3D', 'usernameCipherb64': 'Shga8IDmEK1HIIqZc3EGtVd4QpQtbC70aJOxA3La6SKzwqNsrx%2BblNY9LgOfreCr%0D%0AiGxBQdEgm0yKVja5RsIT4SMUSvIpf08xxGAwGK53KDwbRMuw3WMU4ZCJIAOaArMW%0D%0AiY8yb%2BsDFh%2BtKxOyW60MG3bYIVjDYWMwTeiGllqO%2FzsLMXJdlXhM2x%2BC5txlILjm%0D%0ALQAaBYMkW%2F%2BZt0YE9MwUyVIrBLcamhMaTM9jLzwV8DT289LAR7JCzDoWGP%2FHT%2FEz%0D%0AvNXm33KGhhhas3zYvvLrieUuA2nytbvtvJHZzmcn1aALuDzjWvDm%2FdCR1bnOQJj9%0D%0AnWZ1w3bVnI7imZFqd4%2B93Q%3D%3D', 'passwordCipherb64': 'YbFgL6BLlMLlX1s957%2FOBSbUiPIo3GUevWF%2BJAmPUrQDkHhicgZQKEnSkVQOnvSC%0D%0A8pmKhawfIjoRFP4hfWxhCSeDU6ZWlKyZc2zxQSkJE34FYKVgEjPdsq0lgB7mK%2BMS%0D%0ArL1c2l%2BZoHMWnz3sTf3EeIAljenoL4uKpc8l60uGkdYjdQZ%2Fg9hJB4KQp7BaSXYX%0D%0AbOSIaBppwHXPXdBoU%2BnIFUMff91QS8SO%2FklN5T5cswRKW60mxeMuiEhVQXQCTEDL%0D%0AtpsMAVWJgyH15292A2YuAahVT6u5BstvkXxUN5fQEQUGKYhHFKWBV2SmYDVWE0te%0D%0Ad04vmBSkUmoms%2BvD1cj4Lg%3D%3D', 'account-type': '2', 'src': 'bets'}
        if self.CREATE_DICT_TEAM_PLAYERID:
            # html = requests.post(self.url_login, headers=headers, verify=False, cookies=cookies, data=data)= {'_tz': 'Asia%2FShanghai', '_ga': 'GA1.2.961090768.1592724898', '__qca': 'P0-368302978-1592724902240', '__gads': 'ID', '_ym_uid': '1590651080726563724', '_ym_d': '1592724907', 'pbjs-id5id': '%7B%22ID5ID%22%3A%22ID5-ZHMOrDEaxifVhvRNRZHJiq0L_-oXr7wWsAZNImUX5g%22%2C%22ID5ID_CREATED_AT%22%3A%222020-06-21T07%3A35%3A25.74Z%22%2C%22ID5_CONSENT%22%3Atrue%2C%22CASCADE_NEEDED%22%3Atrue%2C%22ID5ID_LOOKUP%22%3Atrue%2C%223PIDS%22%3A%5B%5D%7D', '_s': 'ZUUyb0ZqNzU1SldBSklybk5yWUk2UzZDL0ViTGNaMVpiZzFhcmkzMXYvQUZPSWwrbkY3WjZralJrcy9vMEdaeFVJa0psUW5tb21vOUpYYnVFUFVVTHNiRjErRGhOZkE1QVBiejNDeUxDcmUzZWplVS9KZDJ5dW5VL296NWJkc2N5Wk01dG9ROFM3TEF1Qll4cWpMa0dOVkI5K3RHYmxCTVZkT0Y0a0lXaVJkOXRxS3lrUmNLVlhrYXVrUUpBSzFoLS15OFJwUkJKWFVJSzF1Qm1OZ3Vsa1h3PT0%3D--ac927341bcffe876cc4f814411d07ae4e96c3637', '_gid': 'GA1.2.590241721.1593564884', '_ym_visorc_52686388': 'w', '_ym_isad': '2', 'pbjs-id5id_last': 'Fri%2C%2003%20Jul%202020%2008%3A18%3A43%20GMT', '_hi': '1593765578384'}
            # url = 'http://dotamax.com/match/tour_famous_team_list/'
            # teampage_headers = {'Host': 'dotamax.com', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.88 Safari/537.36 Vivaldi/2.4.1488.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'http://dotamax.com/bets/index/', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9'}
            # teampage_cookies = {'_ga': 'GA1.2.917068991.1593764201', '_gid': 'GA1.2.981710910.1593764201', 'Hm_lvt_575895fe09d48554a608faa5ef059555': '1593764202', 'csrftoken': 'PP0Xh0PvPbiSWlk7tzkeVaJf7Cc9gUPe', 'pkey': 'MTU5Mzc2ODE0My42MnNjel8wMDBfMnNjbHBlY2x3dGxzbnVrYWg__', '_gat': '1', 'Hm_lpvt_575895fe09d48554a608faa5ef059555': '1593768539'}
            # req_object=get(self.prefix_team,headers=teampage_headers,cookies=teampage_cookies)
            #with open (".txt","w+",encoding="utf-8") as f:
            #    f.write(req_object.text)
            team_and_player={}
            file_page_list=["team_page1.htm","team_page2.htm","team_page3.htm","team_page4.htm","team_page5.htm","team_page6.htm"]
            for file_page in file_page_list:
                with open (file_page,"r+",encoding="utf-8") as f:
                    text_teampage=f.read()
                    # player_id=findall("/player/detail/\d{7,}",text_teampage)
                    # for tag in player_id:
                    #     one_player_id=tag.split("/")[-1]
                    #     if one_player_id!="226124774":
                    #         print ("----")
                    bs4_object=BeautifulSoup(text_teampage,"html.parser")
                    team_tag=bs4_object.find_all("tr",id=compile("matchrow_\d{1,2}"))
                    print (len(team_tag))
                    for tag in team_tag:
                        team_name=tag.find("td",class_="table-title-font").get_text().strip()
                        team_and_player[team_name]=[]
                        all_teammates_id=tag.find_all("a",href=compile("/player/detail/\d{7,}"))
                        for tid_tag in all_teammates_id:
                            tid=tid_tag['href'].split("/")[-2]
                            team_and_player[team_name].append(tid)
            print (team_and_player)
        if True:                            
            with open ("team_and_player.json","w+",encoding="utf-8") as f:
                dump(team_and_player,f,ensure_ascii=False)
            return team_and_player
    def get_current_team_json(self):
        # with open ("current_p_team.json","r+",encoding="utf-8") as f:
        #     dict_team=load(f)
        # for team in dict_team:
        return
    def team_view(self):
        with open ("team_and_player.json","r+",encoding="utf-8") as f:
            dict_teamplayer=load(f)
        total=sum([len(dict_teamplayer[team]) for team in dict_teamplayer])
        for team in dict_teamplayer:
            for player in dict_teamplayer["current_state"]["teammate"]:
                player,dict_teamplayer["current_state"]["teammate"][player][""]

    def update_player_dataset(self):
        self.player_dict_filename="player_dict.json"
        self.team_and_player_filename="team_and_player.json"
        if os.path.exists(self.player_dict_filename)==False:
            with open(self.team_and_player_filename,"r+",encoding="utf-8") as f:
                dict_player_id=load(f)
            self.single_player={}
            for i in dict_player_id:
                for j in dict_player_id[i]:
                    self.single_player[j]={"hero_exp":{},"position_exp":{},"playing_state":[],"是否人工|机器检查":0}#
            with open (self.player_dict_filename,"w+",encoding="utf-8") as f:
                dump(self.single_player,f,ensure_ascii=False)
        with open (self.player_dict_filename,"r+",encoding="utf-8") as f:
            dict_teamplayer=load(f)

if __name__ == '__main__':
    TournamentPreview=False#获取基本页面信息和URL
    TOUR_INFO_UPDATE=True#存储战队页面到字典
    Get_Current_Team_Json=False
    MANUAL_TEAM_AND_PLAYER=False
    UPDATE_TEAMPLAYER_ID=False
    GET_RECENT_MMR_CHANGE=False # 
    VIEW_TEAM_PLAYER=False
    Analyze_Person=False
    VIEW=False
    PLAYER_DATASET=False
    teva=TeamValue()
    if TournamentPreview==True:
        teva.Tournament_preview()
    if TOUR_INFO_UPDATE==True:
        teva.get_current_partici_liquidpedia()
    if Get_Current_Team_Json==True:
        teva.team_view()
    elif MANUAL_TEAM_AND_PLAYER==True:
        teva.team_view()
    elif UPDATE_TEAMPLAYER_ID==True:
        teva.team_players()
        # teva.visulize_team_winlose()
        # teva.other_stats()
        # teva.visulize_team_winlose()
    elif GET_RECENT_MMR_CHANGE==True:
        print (teva.sum_of_allteam())
    elif VIEW_TEAM_PLAYER==True:
        teva.sum_of_allteam()
    elif PLAYER_DATASET==True:
        teva.update_player_dataset()