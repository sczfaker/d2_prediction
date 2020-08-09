#coding:utf-8
from fake_useragent import UserAgent
from time import localtime,strftime,sleep
from random import randint
import pandas as pd
import requests
import sys
import json
import time

# max_match_id = 999999999999999999   # 设置一个极大值作为match_id，可以查出最近的比赛(即match_id最大的比赛)。
#7-10
low_match_id=0
target_match_num = 200000
lowest_mmr = 4350  # 匹配定位线，筛选该分数段以上的天梯比赛 
print (lowest_mmr)
end_time=""
# url = "https://api.opendota.com/api/matches/5075751801?api_key=YOUR-API-KEY"
newest_matchid=0
latest_matchid=0
base_url = 'https://api.opendota.com/api/publicMatches?less_than_match_id='
session = requests.Session()
time_limit="2020-06-10 08:54:01"
struct_tuple=time.strptime(time_limit,"%Y-%m-%d %H:%M:%S")
lower_time_stamp=time.mktime(struct_tuple)
ua=UserAgent()
totaltime_limit=5000#5000
session.headers = {
    'User-Agent': ua.random
}
def crawl(input_url):
    time.sleep(randint(1,3))   # 暂停一秒，防止请求过快导致网站封禁。
    crawl_tag = 0
    while crawl_tag==0:
        try:
            session.get("http://www.opendota.com/")  #获取了网站的cookie
            content = session.get(input_url,timeout=15)
            crawl_tag = 1
        except:
            print(u"Poor internet connection. We'll have another try.")
            sleep(30)
    json_content = json.loads(content.text)
    json_content = [j for i,j in enumerate(json_content) if i%3==0]
    #print(json_content)
    return json_content
import pandas as pd
from pandas import read_csv,DataFrame
import os

match_list = []
recurrent_times = 0
write_tag = 0#
start_of_mainprogram=time.time()
max_time=0#开始的时间从最大到以前
totaltime=0#起始和结束时间差
max_match_id = 5663575914  #5523612516#5550047918 
def get_new_match_row(frame_para):
    start_len=len(frame_para)
    print ("用两小时抓取文件",flush=True)    
    backup_current_time,backup_time=1,3
    global max_match_id
    global max_time
    global totaltime
    global recurrent_times
    while(len(match_list)<target_match_num):
        one_loop_time_start=time.time()
        json_content = crawl(base_url+str(max_match_id))
        try:
            assert json_content[0]["match_id"],"crawl data error"
            assert len(json_content)>0,"len error"
        except:
            continue
        for i in range(len(json_content)):
            match_id = json_content[i]['match_id']
            radiant_win = json_content[i]['radiant_win']
            start_time = json_content[i]['start_time']
            if max_time==0:
                max_time=start_time
            if start_time>max_time:
                max_time=start_time
            avg_mmr = json_content[i]['avg_mmr']
            if avg_mmr==None:
                avg_mmr = 0
            lobby_type = json_content[i]['lobby_type']
            game_mode = json_content[i]['game_mode']
            radiant_team = json_content[i]['radiant_team']
            dire_team = json_content[i]['dire_team']
            duration = json_content[i]['duration']  # 比赛持续时间
            num_mmr=json_content[i]['num_mmr']
            if totaltime>totaltime_limit*(backup_current_time/3) and backup_current_time!=backup_time:
                frame_para.to_csv(fname,index=False)
                backup_current_time+=1
                log_name='./data_recent_mmr/%s'%("crawl_mmr_match.txt")
                with open (log_name,"a+",encoding="utf-8") as f:
                    f.seek(0)
                    tuple_endtime=localtime(int(start_time))
                    tuple_starttime=localtime(int(max_time))
                    start_time_str = strftime('%Y-%m-%d %H:%M:%S',tuple_starttime)
                    end_time_str = strftime('%Y-%m-%d %H:%M:%S',tuple_endtime)
                    print ("防止中断备份(一小时2次)--超过了版本上次更新的时间",len(match_list),"个3500平均分以上比赛数","结束id:",match_id,"开始id:",max_match_id,"遍历比赛id数:",int(max_match_id)-int(match_id),"开始时间",start_time_str,"结束时间",end_time_str,file=f,flush=True)
            if lower_time_stamp>int(start_time) or totaltime>totaltime_limit:
                print("???",test_current_runtime,flush=True)
                log_name='./data_recent_mmr/%s'%("crawl_mmr_match.txt")
                with open (log_name,"a+",encoding="utf-8") as f:
                    f.seek(0)
                    tuple_endtime=localtime(int(start_time))
                    tuple_starttime=localtime(int(max_time))
                    start_time_str = strftime('%Y-%m-%d %H:%M:%S',tuple_starttime)
                    end_time_str = strftime('%Y-%m-%d %H:%M:%S',tuple_endtime)
                    print ("超过了版本上次更新的时间",len(match_list),"个3000-6000平均分以上比赛数","结束id:",match_id,"开始id:",max_match_id,"遍历比赛id数:",5539163915-int(match_id),"开始时间",start_time_str,"结束时间",end_time_str,file=f)
                    print (totaltime,"秒","个数:",len(frame_para)-start_len,file=f)
                    print ("-"*50,file=f) 
                return frame_para
            if int(avg_mmr)<lowest_mmr or not avg_mmr:  # 匹配等级过低，忽略 没有mmr忽略
                continue
            if int(duration)<1500:   # 比赛时间过短，小于15min，视作有人掉线，忽略。
                continue
            if int(lobby_type)!=7 or (int(game_mode)!=3 and int(game_mode)!=22):
                continue
            x = time.localtime(int(start_time))
            game_time = time.strftime('%Y-%m-%d %H:%M:%S',x)
            if game_time<time_limit:
                continue
            try:
                if match_id in list(frame_para.match_id):
                    print ("match already exists",flush=True)
                    continue
            except:
                pass
            one_match_dict={}
            one_match_dict['match_id'],one_match_dict['radiant_win'],one_match_dict['radiant_team'],one_match_dict['dire_team'],one_match_dict['start_time']=int(match_id),bool(radiant_win),radiant_team,dire_team,game_time
            one_match_dict['game_mode'],one_match_dict['duration']=game_mode,duration
            one_match_dict['avg_mmr'],one_match_dict['num_mmr']=avg_mmr,num_mmr
            # print (one_match_dict)
            current_dataframe=pd.json_normalize(one_match_dict)
            frame_para=frame_para.append(current_dataframe)
            match_list.append([match_id])
        max_match_id = json_content[-1]['match_id']
        recurrent_times += 1
        # print(recurrent_times,len(match_list),max_match_id)
        if len(frame_para)>target_match_num:
            return frame_para
        test_current_runtime=time.time()
        totaltime=test_current_runtime-start_of_mainprogram
        print("第%d次循环用时:"%(recurrent_times),test_current_runtime-one_loop_time_start,len(match_list),max_match_id)
        print ("总循环用时:",totaltime,"secs",flush=True)
def estimate_timeid(matchid,matchtime):
    id_time={"5547466015":"1596302459"}
    for i in id_time:
        pass
    with open("timeid_startend_crawllog.json","r+") as f:
        dict_idtime=load(f)
    with open("timeid_startend_crawllog.json","w+") as f:
        dump(dict_idtime,f,ensure_ascii=False)
    return
if __name__ == '__main__':
    #filename_suffix=3600
    #os.popen('at 17:30 shutdown -s')
    fname='./data_recent_mmr/matches_list_ranking_2e6_0915.csv'#%("1300")
    if os.path.exists(fname):
        pd_match_frame=read_csv(fname)
        print ("读取文件")
        pd_match_frame=get_new_match_row(pd_match_frame)
        print("添加文件")
        pd_match_frame.to_csv(fname,index=False)
    else:
        row_title={'match_id':[],'radiant_win':[],'radiant_team':[],'dire_team':[],'start_time':[],'avg_mmr':[],'num_mmr':[],'game_mode':[],'duration':[],'dire_score':[],'radiant_score':[]}
        df_new=DataFrame(row_title)
        df_new=get_new_match_row(df_new)
        print("生成文件")
        df_new.to_csv(fname,index=False)
        pd_match_frame=read_csv(fname)
        pd_match_frame=get_new_match_row(pd_match_frame)
        pd_match_frame.to_csv(fname,index=False)

# with open('../data/matches_list_ranking.csv','w',encoding='utf-8') as fout:
#     fout.write('比赛ID, 时间, 天辉英雄, 夜魇英雄, 天辉是否胜利\n')
#     for item in match_list:
#         fout.write(str(item[4])+', '+item[0]+', '+item[1]+', '+item[2]+', '+str(item[3])+'\n')
        

    





 