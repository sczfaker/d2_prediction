dakd_vueditor.ahk#coding:utf-8
print ("start..")
import os
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from pandas import read_csv,DataFrame
from fake_useragent import UserAgent
from re import findall,compile,match
from os import chdir,listdir,rename
from itertools import combinations
import matplotlib.pyplot as plt
from json import load,dump,loads
from requests import get
from time import sleep
from random import choice
import numpy as np
import pandas as pd
import operator
import random
import datetime
import logging
import sys,io
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
import joblib

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(ch)
class Match_stat(object):
    """docstring for ClassName"""
    def __init__(self,trainmode="mmr"):
        self.match_catalog="MATCH_JSON_DIR_0727/"
        with open("hero_id_name.json","r+") as f:
            self.hero_id_name=load(f)
        with open ("hero_name_id.json","r+") as f:
            self.hero_name_id=load(f)
        self.match_files  = [file for file in listdir(self.match_catalog) if file[-4:]=="json" and match("\d{10,}",file[:-5])]
        self.match_normal= [file for file in listdir(self.match_catalog) if file[-4:]=="json" and file[:6]=="normal"]
        self.match_files=self.match_files#self.match_normal
        print (len(self.match_files),len(self.match_normal))
        self.time_limit="2020-08-01 08:54:01"#版本更新比赛的日期格式
        struct_time_limit=time.strptime(self.time_limit,"%Y-%m-%d %H:%M:%S")
        self.sec_time=time.mktime(struct_time_limit)
        if trainmode=="pro":
            self.save_everymatch_tocsv()
            print("创建新的测试集和训练集完毕...")
            self.MODEL_NAME=newest_model#
            print ("新csv:准备生成模型:",self.MODEL_NAME)
        elif trainmode=="mmr":
            self.create_testset_csv_4430()
            # pre_df1=pd.read_csv("matches_0727.csv")
            # pre_df2=pd.read_csv("matches_testset_0727.csv")
            # self.pre_lenth=len(pre_df1.append(pre_df2))
        else:
            pre_df1=pd.read_csv("matches_0727.csv")
            pre_df2=pd.read_csv("matches_testset_0727.csv")
            self.pre_lenth=len(pre_df1.append(pre_df2))
            newest_model='model_'+str(datetime.date.today())+"_"+str(self.pre_lenth)+'.pkl'#"model_2020-07-06.pkl#"model_2020-07-06.pkl"
            print (newest_model)
            self.MODEL_NAME=newest_model#
        self.best_model='model_'+str(datetime.date.today())+"_"+str(self.pre_lenth)+'.pkl'#"model_2020-07-06.pkl#"model_2020-07-06.pkl"
        self.real_match={}
        self.team_ana={}
        self.afight={}
        self.game_version="0727"
        self.r_pick_score=0
        self.d_pick_score=0
        self.heao_value_measure={}
        self.count=[0,0]
        self.ua = UserAgent()
        self.headers={"user-agent":self.ua.random}
        print (self.headers)
        self.heroes_released=129
    def gethero_frombanpick(self,banpick):
        direteam,radiantteam=0,0
    def create_testset_csv_4430(self):
        fname="matches_list_ranking_2e6_0915.csv"
        total_csv=read_csv(fname)
        self.pre_lenth=len(total_csv)
        newest_model='model_'+str(datetime.date.today())+"_"+str(self.pre_lenth)+'.pkl'#"model_2020-07-06.pkl#"model_2020-07-06.pkl"
        self.MODEL_NAME=newest_model
        COLUMNS = ['match_id','radiant_win','radiant_team','dire_team',"start_time",'avg_mmr','num_mmr','game_mode','duration','dire_score','radiant_score']#teamfights#draft_timings
        train_set, test_set = train_test_split(total_csv, test_size=0.08, random_state=47)
        pd.DataFrame(train_set,columns=COLUMNS).to_csv("matches_0727.csv",index=False)
        pd.DataFrame(test_set,columns=COLUMNS).to_csv("matches_testset_0727.csv",index=False)
    def save_everymatch_tocsv(self):
        #print ("时长过滤:",len(self.match_files))
        # fname="matches_list_ranking_2e6.csv"
        COLUMNS = ['match_id','radiant_win','radiant_team','dire_team',"start_time",'avg_mmr','num_mmr','game_mode','duration','dire_score','radiant_score']#teamfights#draft_timings
        result_dataframe=pd.DataFrame()
        test_dataframe=pd.DataFrame()
        self.filter_matchfile=[]
        random.seed(1)
        print ("start...")
        self.right_count=0
        self.left_count=0
        self.mid_count=0
        for match_file in self.match_files:
            with open(self.match_catalog+match_file,"r+",encoding="utf-8") as f:
                dic_one_match=load(f)
                if dic_one_match["duration"]>1400 and dic_one_match["game_mode"]==2 and self.sec_time<dic_one_match['start_time']:
                    self.filter_matchfile.append(match_file)
                    self.right_count+=1
                if dic_one_match["game_mode"] in [22,3] and dic_one_match["duration"]>1400 and self.sec_time<dic_one_match['start_time']:
                    try:
                        assert dic_one_match["radiant_team"] and dic_one_match["dire_team"]
                        self.mid_count+=1
                        assert len(dic_one_match["radiant_team"].split(","))==5 and len(dic_one_match["dire_team"].split(","))==5
                        self.left_count+=1
                        self.filter_matchfile.append(match_file)
                    except:
                        continue

        print (self.right_count,self.mid_count,self.left_count)#dic_one_match["duration"],type(dic_one_match["duration"])
        self.match_files=self.filter_matchfile
        #print ("时长过滤:",len(self.match_files))
        self.RATIO_TESET=len(self.match_files)//5
        self.test_files=random.sample(self.match_files,self.RATIO_TESET)
        for one_test_file in self.test_files:
            self.match_files.remove(one_test_file)
        print ("基本数据:",self.RATIO_TESET,"总训练数据:",len(self.match_files),"总测试数据:",len(self.test_files)+self.RATIO_TESET)
        self.count_iteration=0
        for one_train_file in self.match_files:
            with open(self.match_catalog+one_train_file,"r+",encoding="utf-8") as f:
                dic_one_match=load(f)
                if dic_one_match["game_mode"]==2:
                    radiant,dire=[],[]
                    pickbans,direid,rid=dic_one_match["picks_bans"],dic_one_match["dire_team_id"],dic_one_match["radiant_team_id"]
                    for pickbanseq in pickbans:
                        if pickbanseq["is_pick"]==True:
                                hero_id=pickbanseq["hero_id"]
                                hero_name=self.hero_id_name[str(hero_id)]
                                if pickbanseq["team"]==1:
                                    dire.append(hero_id)
                                else:
                                    radiant.append(hero_id)
                    if len(dire)==5 and len(radiant)==5:
                        dic_one_match["dire_team"]=",".join([str(i) for i in dire])
                        dic_one_match["radiant_team"]=",".join([str(i) for i in radiant])
                        dic_one_match["avg_mmr"]=choice(range(6000,6500,20))
                        dic_one_match["num_mmr"]=random.randint(0,9)
                        current_dataframe=pd.json_normalize(dic_one_match)
                        result_dataframe=result_dataframe.append(current_dataframe)
                else:
                    dic_one_match["avg_mmr"]=choice(range(6000,6700,20))
                    dic_one_match["num_mmr"]=random.randint(0,9)
                    current_dataframe=pd.json_normalize(dic_one_match)
                    result_dataframe=result_dataframe.append(current_dataframe)
            self.count_iteration+=1
        for one_test_file in self.test_files:
            with open(self.match_catalog+one_test_file,"r+",encoding="utf-8") as f:
                dic_test_match=load(f)
                if dic_test_match["game_mode"]==2:
                    radiant,dire=[],[]
                    pickbans,direid,rid=dic_test_match["picks_bans"],dic_test_match["dire_team_id"],dic_test_match["radiant_team_id"]
                    for pickbanseq in pickbans:
                        if pickbanseq["is_pick"]==True:
                                hero_id=pickbanseq["hero_id"]
                                hero_name=self.hero_id_name[str(hero_id)]
                                if pickbanseq["team"]==1:
                                    dire.append(hero_id)
                                else:
                                    radiant.append(hero_id)
                    if len(dire)==5 and len(radiant)==5:
                        dic_test_match["dire_team"]=",".join([str(i) for i in dire])
                        dic_test_match["radiant_team"]=",".join([str(i) for i in radiant])
                        dic_test_match["avg_mmr"]=choice(range(6000,6500,20))
                        dic_test_match["num_mmr"]=random.randint(0,9)
                        current_dataframe=pd.json_normalize(dic_test_match)
                        test_dataframe=test_dataframe.append(current_dataframe)
                else:
                    dic_one_match["avg_mmr"]=choice(range(6000,6500,20))
                    dic_one_match["num_mmr"]=random.randint(0,9)
                    current_dataframe=pd.json_normalize(dic_test_match)
                    test_dataframe=test_dataframe.append(current_dataframe)                
        print (len(self.match_files),"比较过滤时长后的",len(result_dataframe))
        try:
            pd.DataFrame(result_dataframe,columns=COLUMNS).to_csv("matches_0727_pro.csv",index=False)
            pd.DataFrame(test_dataframe,columns=COLUMNS).to_csv("matches_testset_0727_pro.csv",index=False)
        except:
            assert 1>2,"Fail in creating set"
        return result_dataframe
    def iterate_file(self):
        self.rigth_count,need_to_fix=0,[]
        for match in self.match_files:
            with open (self.match_catalog+"/"+match,"r+",encoding="utf-8") as f:
                dict_match=load(f)
                if not dict_match["picks_bans"]:
                    continue
            self.real_match[match[:-5]]=dict_match
        for rm in self.real_match:
            if str(self.real_match[rm]["match_id"])==rm.split("_")[-1]:
                self.rigth_count+=1
            else:
                print (rm,"!=",self.real_match[rm]["match_id"])
                need_to_fix.append(rm)
        print("过滤掉中单模式的比赛:",self.rigth_count)
    def two_team_futuremeet(self):
        for i in self.match:
            r,d=self.match[i]["dire_team_id"],self.match[i]["radiant_team_id"]
            if r not in self.team_ana:#
                self.team_ana[r]={}
            if d not in self.team_ana:
                self.team_ana[r]={}
        for afight in combinations(self.team_ana.keys(),2):
            self.afight[afight]={}
        print (len(self.afight))
    def get_heroid_content(self):
        self.heroes_released = 129
        self.hero_id={}
        hero_release=[]
        with open ("hero_id_name_id.json","r+") as f:
            self.hero_id=load(f)
        version={}
        with open(self.match_catalog+"/"+"heroes.json") as f:
            hero_id_content=load(f)
        t=[]
        for hero in hero_id_content:
            t.append(hero["id"])
        dd=set(range(1,130))
        self.x=dd.difference(t)
        for hero in hero_id_content:
            #self.hero_id[hero["id"]]=hero["localized_name"].replace(" ","-").lower()
            hero_release.append({"id":hero["id"],"name":hero["localized_name"],"primary_attribute":hero["primary_attr"]})
        version["heroes_7.27"]=hero_release
        return version
    def all_match_bp(self):
        ban_pick_result={}
        for match in self.real_match:
            p,direid,rid=self.real_match[match]["picks_bans"],self.real_match[match]["dire_team_id"],self.real_match[match]["radiant_team_id"]
            win_object=lambda:"radiant" if self.real_match["radiant_win"] else "dire"
            amatch_combination={"dire":[],"rand":[]}
            for i in p:
                if i["is_pick"]==True:
                        hero_id=i["hero_id"]
                        hero_name=self.hero_id_name[str(hero_id)]
                        if i["team"]==1:
                            amatch_combination["dire"].append(hero_name)
                        else:
                            amatch_combination["rand"].append(hero_name)
            ban_pick_result[match]={"sequence":p,"diretid":direid,"rid":rid,"win_object":win_object,"combination":amatch_combination}
        for i in ban_pick_result:
            print (i)
            print (ban_pick_result[i]["combination"])
    def build_team_hero_dict(self):
        a=0
        for i in self.team_ana:
            self.team_ana[i]={}
            a=i
            for j in self.hero_id:
                self.team_ana[i][self.hero_id[j]]=50
        return 
    def read_dataset(self,csv_path,low_mmr=None,high_mmr=None,advantages=False):
        global logger
        dataset_df = pd.read_csv(csv_path)
        print (len(dataset_df))
        if low_mmr:
            dataset_df = dataset_df[dataset_df.avg_mmr > low_mmr]
        if high_mmr:
            dataset_df = dataset_df[dataset_df.avg_mmr < high_mmr]
        print("The dataset contains %d games"%(len(dataset_df)))
        if advantages:
            print("Computing advantages...")
            advantages_list = self.compute_advantages(dataset_df)

        else:
            logger.info("Loading advantages from files...")
            synergies = np.loadtxt('pretrained/synergies_all_0727.csv')
            counters = np.loadtxt('pretrained/counters_all_0727.csv')
            advantages_list = [synergies, counters]
        logger.info("Transforming dataframe in feature map...")
        feature_map = self.dataset_to_features(dataset_df, advantages=advantages_list)
        #将这个二长度数组和pd对象8e6传入dtf返回
        return [feature_map, advantages_list]
    def compute_advantages(self,dataset_df):
        self.synergy = dict()
        self.synergy['wins'] = np.zeros((self.heroes_released, self.heroes_released))
        self.synergy['games'] = np.zeros((self.heroes_released, self.heroes_released))
        self.synergy['winrate'] = np.zeros((self.heroes_released, self.heroes_released))
        self.counter = dict()
        self.counter['wins'] = np.zeros((self.heroes_released, self.heroes_released))
        self.counter['games'] = np.zeros((self.heroes_released, self.heroes_released))
        self.counter['winrate'] = np.zeros((self.heroes_released, self.heroes_released))
        dataset_np = dataset_df.values
        print ("value长度",len(dataset_np),"总长度",len(dataset_df))
        for row_amatch in dataset_np:
            self.update_dicts(row_amatch, self.synergy, self.counter)
        self.compute_winrates(self.synergy, self.counter, self.heroes_released)#得到胜场和总场数后计算胜率
        with open("pretrained/synergies_all_0727.json","w+",encoding="utf-8") as f1,open("pretrained/counters_all_0727.json","w+",encoding="utf-8") as f2:
            s,y=self.synergy.copy(),self.counter.copy()
            for i in s:
                s[i]=s[i].tolist()
            for i in y:
                y[i]=y[i].tolist()
            dump(s,f1,ensure_ascii=False)
            dump(y,f2,ensure_ascii=False)
        self.synergy_matrix,self.counter_matrix =self.calculate_advantages(self.synergy, self.counter, self.heroes_released)
        #print (self.synergy_matrix)
        #print (self.counter_matrix)
        # assert 1>2
        np.savetxt('pretrained/synergies_all_0727.csv', self.synergy_matrix)
        np.savetxt('pretrained/counters_all_0727.csv',self.counter_matrix)
        return [self.synergy_matrix, self.counter_matrix]#一个数组,包含两个np矩阵,每个矩阵值都是129*129坐标的浮点值,0~1
    def update_dicts(self,game, synergy, counter):
        self.radiant_wincount,self.dire_wincount=0,0
        radiant_win, radiant_heroes, dire_heroes = game[1], game[2], game[3]
        if radiant_win:
            self.radiant_wincount+=1
        else:
            self.dire_wincount+=1
        radiant_heroes = list(map(int, radiant_heroes.split(',')))
        dire_heroes = list(map(int, dire_heroes.split(',')))

        assert len(set(radiant_heroes).intersection(set(dire_heroes)))==0
        for i in range(5):#单个比赛的天辉夜宴与天辉英雄序号:访问(1-129数字)
            for j in range(5):#单个比赛的夜宴与天辉英雄序号:访问(1-129数字)
                if i != j:#当序号i不等序号j:计算的是同一边的:序号相同即为重复忽略
                    synergy['games'][radiant_heroes[i] - 1, radiant_heroes[j] - 1] += 1#每一场比赛会获得组合增量为20+20,实际组合增量为10+10
                    synergy['games'][dire_heroes[i] - 1, dire_heroes[j] - 1] += 1
                    if radiant_win:#这里i,j j,i视为一样+1
                        synergy['wins'][radiant_heroes[i] - 1, radiant_heroes[j] - 1] += 1#或者标记+1
                    else:
                        synergy['wins'][dire_heroes[i] - 1, dire_heroes[j] - 1] += 1#获胜标记+1
                counter['games'][radiant_heroes[i] - 1, dire_heroes[j] - 1] += 1#对抗组合+1 
                counter['games'][dire_heroes[i] - 1, radiant_heroes[j] - 1] += 1#对抗组合+1 50 实际增量25
                if radiant_win:#这里比较关键,注意counter会出现i,j 和 j,i的情况 r赢p[ij]+1 d赢p[ji]+1 表示英雄a遇到b的胜场+1 表示英雄b遇到a的胜场+1 两者加起来也是两者遇到的总场数两者获胜概率加起来也是1
                    counter['wins'][radiant_heroes[i] - 1, dire_heroes[j] - 1] += 1
                else:
                    counter['wins'][dire_heroes[i] - 1, radiant_heroes[j] - 1] += 1
    def compute_winrates(self,synergy, counter, heroes_released):
        for i in range(heroes_released):
            for j in range(heroes_released):
                if i!=j:#一个英雄不可能和自己同一边同一边的那个数据的ganme,winrate,win的值都为0
                    #也不可能和自己对抗注意这里的序号ij意义和上面updatedic的ij意义不同
                    if synergy['games'][i, j] != 0:#8w比赛不可能序号不同还为0
                        synergy['winrate'][i, j] = synergy['wins'][i, j]/float(synergy['games'][i, j])
                            # print ("hero",i,j,synergy['winrate'][i, j])
                    if counter['games'][i, j] != 0:#8w比赛不可能序号不同还为0
                        counter['winrate'][i, j] = counter['wins'][i, j]/float(counter['games'][i, j])
                        # print ("hero",i,j,counter['winrate'][i, j])
    def calculate_advantages(self,synergy, counter, heroes_released):
        synergies = np.zeros((heroes_released, heroes_released))#重建两个空矩阵,保存的是所有英雄对的胜率,存储为csv格式
        counters = np.zeros((heroes_released, heroes_released))#重建两个空矩阵,保存的是所有英雄对的胜率,存储为csv格式                              
        base_winrate = np.zeros(heroes_released)#重建一个胜率向量
        for i in range(heroes_released):#迭代syn的胜率 
            if np.sum(synergy['games'][i])!=0:#场数不为0就重新计算胜率
                base_winrate[i] = np.sum(synergy['wins'][i]) / np.sum(synergy['games'][i])#第i行的胜场总数除以第i行的总场数
                #print (synergy["wins"][i],synergy["games"][i],synergy["winrate"][i])
                # print (base_winrate[i],i)
        for i in range(heroes_released):#winrate直接复制单个winrate
            for j in range(heroes_released):
                if i!=j:
                    if synergy['games'][i, j] > 0:#
                        synergies[i, j] = self.adv_synergy(synergy['winrate'][i, j],
                                                       base_winrate[i],
                                                       base_winrate[j])
                    else:
                        synergies[i, j] = 0
                    if counter['games'][i, j] > 0:
                        counters[i, j] = self.adv_counter(counter['winrate'][i, j],
                                                      base_winrate[i],
                                                      base_winrate[j])
                    else:
                        counters[i, j] = 0 
        return synergies, counters
    def adv_synergy(self,winrate_together, winrate_hero1, winrate_hero2):
        return winrate_together
    def adv_counter(self,winrate_together, winrate_hero1, winrate_hero2):
        return winrate_together
    def dataset_to_features(self,dataset_df, advantages=None):
        c,t=10,0
        heroes_released = 129
        synergy_matrix, counter_matrix = None, None
        if advantages:#一般为True是一个2长度的两个胜率矩阵129*129
            x_matrix = np.zeros((dataset_df.shape[0], 2 * heroes_released + 3))#创建新矩阵 长度 为8e6
            [synergy_matrix, counter_matrix] = advantages#赋值
        else:
            x_matrix = np.zeros((dataset_df.shape[0], 2 * heroes_released))
        y_matrix = np.zeros(dataset_df.shape[0])#创建r胜为1r负为0向量
        dataset_np = dataset_df.values#准备迭代所有场次
        for i, row in enumerate(dataset_np):#再次迭代每一场
            radiant_win = row[1]#结果,注意是1 i是序号
            radiant_heroes = list(map(int, row[2].split(',')))
            dire_heroes = list(map(int, row[3].split(',')))

            for j in range(5):
                x_matrix[i, radiant_heroes[j] - 1] = 1#天辉五个在哪些地方设置为1
                x_matrix[i, dire_heroes[j] - 1 + heroes_released] = 1#夜宴5个在哪些地方设置为1
            if advantages:#传入单个场次的同边胜率,矩阵作为最后三个值 第一个为syn总胜率20个概率相加 第二个为syn d总胜率20个概率值相加
            #第三个为counter总胜率25个
                x_matrix[i, -3:] = self.augment_with_advantages(synergy_matrix,
                                                           counter_matrix,
                                                           radiant_heroes,
                                                           dire_heroes)
                # print("最后三个关键数据:",x_matrix[i, -3:])
                # t+=1
                # if t>c:
                #     break
            y_matrix[i] = 1 if radiant_win else 0
        return [x_matrix, y_matrix]#返回两个长度为所有比赛的矩阵 y是胜负 x是英雄1,0和 cot syn胜率和
    def augment_with_advantages(self,synergy, counter, radiant_heroes, dire_heroes):
        synergy_radiant = 0#注意这里是每一行比赛都要重新更新的数据 10对同边胜率直接相加除10有没有意义
        synergy_dire = 0#注意这里是每一行比赛都要重新更新的数据 10对同边胜率直接相加除
        counter_score = 0#注意这里是每一行比赛都要重新更新的数据 25对异边胜率直接相加
        for i in range(5):
            for j in range(5):
                if i > j:#去掉重复的比如1,0和0,1重复
                    synergy_radiant += synergy[radiant_heroes[i] - 1][radiant_heroes[j] - 1]
                    synergy_dire += synergy[dire_heroes[i] - 1][dire_heroes[j] - 1]
                counter_score += counter[radiant_heroes[i] - 1][dire_heroes[j] - 1]
        return np.array([synergy_radiant, synergy_dire, counter_score])#得到每场比赛的数组的三个总概率值 
        #总counter_score表示的是 两边的各自的对抗胜率的和
    def create_testset(self):
        result_dataframe=pd.DataFrame()
        fname="matches_testset_0727.csv"
        COLUMNS = ['match_id','radiant_win','radiant_team','dire_team','avg_mmr','num_mmr','game_mode', 'lobby_type','duration','draft_timings','dire_score','radiant_score']#teamfights
        for single_testset_match in self.test_files_dict:
            current_dataframe=pd.json_normalize(self.test_files_dict[single_testset_match])
            result_dataframe=result_dataframe.append(current_dataframe)
        pd.DataFrame(result_dataframe,columns=COLUMNS).to_csv(fname,index=False)
        return result_dataframe
    def train(self,advantages_update_pretrain=True):
        print (advantages_update_pretrain)
        #_不用是因为advlist已经转换成了dataset_train[xm,ym]
        dataset_train, _ = self.read_dataset('matches_0727.csv',advantages=advantages_update_pretrain)
        dataset_test, _ = self.read_dataset('matches_testset_0727.csv',advantages=advantages_update_pretrain)
        print (len(dataset_train),len(dataset_test))
        result=self.evaluate(dataset_train, dataset_test, cv=100, save_model=self.MODEL_NAME)
        return result
    def evaluate(self,train_data, test_data,cv=3,save_model=None):
        x_train, y_train = train_data
        x_test, y_test = test_data
        scaler = StandardScaler()#创建一个对象,标准化对每个值
        scaler.fit(x_train)
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)
        cross_val_mean = -1
        y_test,y_train=(y_test==True).astype(np.int),(y_train==True).astype(np.int)
        if cv > 0:
            model = LogisticRegression(C=0.005,random_state=58)
            cross_val_scores = cross_val_score(model, x_train, y_train, cv=cv, scoring='roc_auc',
                                               n_jobs=-1)
            cross_val_mean = np.mean(cross_val_scores)
            logger.info("Cross validation scores over the training set (%d folds): %.3f +/- %.3f", cv,
                        cross_val_mean,
                        np.std(cross_val_scores))
        model = LogisticRegression(C=0.005,solver="sag",max_iter=50000,random_state=58)
        model.fit(x_train, y_train)#训练模型
        probabilities = model.predict_proba(x_test)#在标准化训练集后 用predict_pro接受测试集预测概率
        roc_auc = roc_auc_score(y_test, probabilities[:, 1])#直接用测试集去检验roc_auc
        labels = model.predict(x_test)
        acc_score = accuracy_score(y_test, labels)
        if save_model:
            model_dict = {}
            model_dict['scaler'] = scaler
            model_dict['model'] = model
            joblib.dump(model_dict, save_model)
        self.x_train,self.y_train=x_train,y_train
        return (x_train.shape[0], x_test.shape[0], cross_val_mean, roc_auc, acc_score)  
    def query_full(self,model,scaler,radiant_heroes,dire_heroes,synergies,counters,heroes_released):
        features = np.zeros(2 * heroes_released + 3)
        for i in range(5):
            features[radiant_heroes[i] - 1] = 1
            features[dire_heroes[i] - 1 + heroes_released] = 1
        extra_data = self.augment_with_advantages(synergies, counters, radiant_heroes, dire_heroes)
        features[-3:] = extra_data

        features_reshaped = features.reshape(1, -1)
        features_final = scaler.transform(features_reshaped)
        probability_one = model.predict_proba(features_final)[:,1]*100
        if probability_one > 50:
            return "Radiant has %.3f%% chance" % probability_one
        else:
            return "Dire has %.3f%% chance" % (100 - probability_one)
    def query(self,mmr,radiant_heroes, dire_heroes, synergies=None, counters=None, similarities=None):

        if counters is None:#如果是提前给了 syn和cnt pro_csv参数就不会执行 cnts
            cnts = np.loadtxt('pretrained/counters_all_0727.csv')
        else:
            cnts = np.loadtxt(counters)            
        if synergies is None:
            syns = np.loadtxt('pretrained/synergies_all_0727.csv')
        else:
            syns = np.loadtxt(synergies)
        if mmr < 2000:
            model_dict = joblib.load(os.path.join("pretrained", "2000-.pkl"))
            logger.info("Using 0-2000 MMR model")
        model_dict = joblib.load(self.MODEL_NAME)
        scaler = model_dict['scaler']
        model = model_dict['model']
        heroes_released = self.heroes_released
        if len(radiant_heroes) + len(dire_heroes) == 10:
            return self.query_full(model,scaler,radiant_heroes,dire_heroes,syns,cnts,heroes_released)
        return self.query_missing(model,scaler,radiant_heroes,dire_heroes,syns,cnts,sims,heroes_released)
    def query_example(self):
        full_result = self.query(6000,
                            [59, 56, 54, 48, 31],
                            [40, 41, 52, 68, 61])
        logger.info("The result of the full query is: %s", full_result)

    def get_teamid_tostr(self,rtid,dtid):
        urlprefix="https://api.opendota.com/api/teams/"
        print(rtid,dtid,len(self.teamid_to_name))

        if rtid in self.teamid_to_name:
            rname=self.teamid_to_name[rtid]["fullname"]
        if dtid in self.teamid_to_name:
            dname=self.teamid_to_name[dtid]["fullname"]
        return rname,dname

    def get_match_bp(self):
        self.match_url=[]
        from dotadata_mining_banpick import Ban_Pick
        radiant,dire=[],[]
        radiant_name,dire_name={},{}
        instance=Ban_Pick()
        print (instance.match_url,"比赛实时列表长度:",len(instance.match_url))
        instance.match_url=[1]
        for one_full_url in instance.match_url:
            radiant_full,dire_full,rname,dname=instance.get_vpgame()#get_vpgame()
            print(radiant_full,dire_full,rname,dname)
            radiant_name[rname]=radiant_full[:]
            dire_name[dname]=dire_full[:]
            print(radiant_full,dire_full)
            if len(radiant_full)==5 and len(dire_full)==5:
                    self.MODEL_NAME='promodel_'+str(datetime.date.today())+"_"+str(self.pre_lenth)+'.pkl'
                    full_result=self.query(6000,radiant_name[rname],dire_name[dname])
                    pre_df1=pd.read_csv("matches_0727_pro.csv")
                    pre_df2=pd.read_csv("matches_testset_0727_pro.csv")
                    self.pre_lenth=len(pre_df1)+len(pre_df2)
                    self.MODEL_NAME='model_'+str(datetime.date.today())+"_"+str(self.pre_lenth)+'.pkl'
                    full_result_pro=self.query(6000,radiant_name[rname],dire_name[dname],synergies="pretrained/synergies_all_0727_pro.csv",counters="pretrained/counters_all_0727_pro.csv")
                    confirm_pro=full_result_pro.split(" ")[0].lower()
                    percentage=str(float(full_result.split(" ")[2][:-1]))+"%"
                    percentage_pro=str(float(full_result_pro.split(" ")[2][:-1]))+"%"
                    confirm=full_result.split(" ")[0].lower()
                    print (confirm,percentage,confirm_pro,percentage_pro)
                    print ("预测结果3000以上天梯:%s ----:%s:%s vs :%s:%s"%(full_result,rname,radiant_name[rname],dname,dire_name[dname]))
                    print ("预测结果最近职d业比赛:%s ----:%s:%s vs :%s:%s"%(full_result_pro,rname,radiant_name[rname],dname,dire_name[dname]))
                    #增加奖金系数,后面增加水平系数
            pre_df=pd.read_csv("matches_list_ranking_2e6.csv")
            self.pre_lenth=len(pre_df)
            self.r=radiant_full
            self.d=dire_full
            print(radiant,"vs",dire)
        self.pick_statistics()

        return radiant,dire,rname,dname
    def single_query(self):
        radiant,dire,rname,dname=self.get_match_bp()
        full_result=self.query(6000,radiant,dire)
        confirm=full_result.split(" ")[0].lower()
        # self.get_teamid_tostr(str(rtid),str(dtid))
        print ("预测结果:%s ----r:%s vs d:%s"%(full_result,rname,dname))
    def pick_statistics(self, mmr_info="1"):
        self.pick_dict_pro,self.win_dict_pro,self.win_rate_pro={},{},{}
        self.pick_dict,self.win_dict,self.win_rate={},{},{}
        for i in self.hero_id_name:
            self.pick_dict_pro[self.hero_id_name[i]]=0
            self.win_dict_pro[self.hero_id_name[i]]=0
            self.win_rate_pro[self.hero_id_name[i]]=0
            self.pick_dict[self.hero_id_name[i]]=0
            self.win_dict[self.hero_id_name[i]]=0
            self.win_rate[self.hero_id_name[i]]=0       

        # pick_rate = games / np.sum(games)
        df_pro=pd.read_csv("matches_0727_pro.csv")
        df_test_pro=pd.read_csv("matches_testset_0727_pro.csv")
        df_total_pro=pd.concat([df_pro,df_test_pro],axis=0,ignore_index=True)

        for i,j,rw in zip(df_total_pro.radiant_team,df_total_pro.dire_team,df_total_pro.radiant_win):
            a,b=i.split(","),j.split(",")
            for i,j in zip(a,b):
                self.pick_dict_pro[self.hero_id_name[i]]+=1
                self.pick_dict_pro[self.hero_id_name[j]]+=1
                if rw:
                    self.win_dict_pro[self.hero_id_name[i]]+=1
                if not rw:
                    self.win_dict_pro[self.hero_id_name[j]]+=1  
        df_mmr_total=pd.read_csv("matches_list_ranking_2e6.csv")

        for i,j,rw in zip(df_mmr_total.radiant_team,df_mmr_total.dire_team,df_mmr_total.radiant_win):
            a,b=i.split(","),j.split(",")
            for i,j in zip(a,b):
                self.pick_dict[self.hero_id_name[i]]+=1
                self.pick_dict[self.hero_id_name[j]]+=1
                if rw:
                    self.win_dict[self.hero_id_name[i]]+=1
                if not rw:
                    self.win_dict[self.hero_id_name[j]]+=1          

        pick_listto_sort=self.pick_dict_pro.items()
        x=sorted(pick_listto_sort,key=lambda x:x[1])
        # print (x)
        print (self.r,self.d)
        self.cr,self.cd=[self.hero_id_name[str(i)] for i in self.r],[self.hero_id_name[str(i)] for i in self.d]
        # print (self.cr,self.cd)
        rad_p_pro,dire_p_pro=[],[]
        for i,j in zip(self.cr,self.cd):
            rad_p_pro.append([i,self.pick_dict_pro[i]])
            dire_p_pro.append([j,self.pick_dict_pro[j]])
        print ("两边总统计数pro:",rad_p_pro,"vs",dire_p_pro)
        rad_mmr,dire_mmr=[],[]
        for i,j in zip(self.cr,self.cd):
            rad_mmr.append([i,self.pick_dict[i]])
            dire_mmr.append([j,self.pick_dict[j]])
        print ("两边总统计数mmr:",rad_mmr,"vs",dire_mmr)
    def plot_learning_curve(self,x_train=None, y_train=None, subsets=200, mmr=None, cv=3, tool='matplotlib'):
        dataset_train, _ = self.read_dataset('matches_0727.csv', low_mmr=6000,advantages=True)
        dataset_test, _ = self.read_dataset('matches_testset_0727.csv', low_mmr=6000,advantages=True)

        x_train, y_train=dataset_train
        x_test,y_test=dataset_test

        #x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2)
        subset_sizes = np.exp(np.linspace(3, np.log(len(y_train)), subsets)).astype(int)
        results_list = [[], []]
        for subset_size in subset_sizes:
            print("执行",subset_size)
            # logger.info('Performing cross validation on subset_size %d', subset_size)
            _, _, cv_score, roc_auc, _ = self.evaluate([x_train[:subset_size], y_train[:subset_size]],
                                                  [x_test, y_test], cv=5)
            results_list[0].append(1 - cv_score)
            results_list[1].append(1 - roc_auc)
        if tool == 'matplotlib':
            self.plot_matplotlib(subset_sizes, results_list, mmr)
    def plot_matplotlib(subset_sizes, data_list, mmr):
        plt.plot(subset_sizes, data_list[0], lw=2)
        plt.plot(subset_sizes, data_list[1], lw=2)
        plt.legend(['Cross validation error', 'Test error'])
        plt.xscale('log')
        plt.xlabel('Dataset size')
        plt.ylabel('Error')
        if mmr:
            plt.title('Learning curve plot for %d MMR' % mmr)
        else:
            plt.title('Learning curve plot')
        plt.show()
    def plot_basic_learning_view(self):
        pass
    def query_missing(self,model,scaler,radiant_heroes,dire_heroes,synergies,counters,similarities,heroes_released):
        all_heroes = radiant_heroes + dire_heroes
        base_similarity_radiant = 0
        base_similarity_dire = 0
        radiant = len(radiant_heroes) == 4
        for i in range(4):
            for j in range(4):
                if i > j:
                    base_similarity_radiant += similarities[radiant_heroes[i], radiant_heroes[j]]
                    base_similarity_dire += similarities[dire_heroes[i], dire_heroes[j]]
        query_base = np.zeros((heroes_released, 2 * heroes_released + 3))
        for i in range(heroes_released):
            if radiant:
                radiant_heroes.append(i + 1)
            else:
                dire_heroes.append(i + 1)
            for j in range(5):
                query_base[i][radiant_heroes[j] - 1] = 1
                query_base[i][dire_heroes[j] - 1 + heroes_released] = 1
            query_base[i][-3:] = augment_with_advantages(synergies,
                                                         counters,
                                                         radiant_heroes,
                                                         dire_heroes)
            if radiant:
                del radiant_heroes[-1]
            else: 
                del dire_heroes[-1]
        if radiant:
            probabilities = model.predict_proba(scaler.transform(query_base))[:, 1]
        else:
            probabilities = model.predict_proba(scaler.transform(query_base))[:, 0]

        heroes_dict = get_hero_dict()
        similarities_list = []

        results_dict = {}
        for i, prob in enumerate(probabilities):
            if i + 1 not in all_heroes and i != 23:
                if radiant:
                    similarity_new = base_similarity_radiant
                    for j in range(4):
                        similarity_new += similarities[i + 1][radiant_heroes[j]]
                    similarities_list.append(similarity_new)
                else:
                    similarity_new = base_similarity_dire
                    for j in range(4):
                        similarity_new += similarities[i + 1][dire_heroes[j]]
                    similarities_list.append(similarity_new)

                results_dict[heroes_dict[i + 1]] = (prob, similarity_new)
        results_list = sorted(results_dict.items(), key=operator.itemgetter(1), reverse=True)
        similarities_list.sort()
        max_similarity_allowed = similarities_list[len(similarities_list) / 4]
        filtered_list = [x for x in results_list if x[1][1] < max_similarity_allowed]
        return filtered_list  

if __name__ == '__main__':
    update_model_logic=False
    REALTIME_PREDICT=True
    OVERVIEW=False
    if update_model_logic==True:
        print ("start..")
        instance=Match_stat(trainmode="mmr")#更新
        train_result=instance.train()
        print (train_result,"训练成功:","模型(逻辑回归):")
    elif REALTIME_PREDICT==True:
        print ("start..")
        instance=Match_stat(trainmode=None)#update_dataset_and_testset=True
        instance.get_match_bp()
    elif OVERVIEW==True:
        instance=Match_stat(trainmode="None")
        instance.plot_learning_curve()

        #instance.plot_learning_curve()