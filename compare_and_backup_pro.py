#coding:utf-8
print("excute")
import os
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from fake_useragent import UserAgent
from re import findall,compile,match
from os import chdir,listdir,rename
from itertools import combinations
from json import load,dump,loads
from requests import get
from time import sleep
from random import choice
import numpy as np
import pandas as pd
import operator
import random
import logging
import sys,io
import datetime
print("excute")
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
import joblib
import matplotlib.pyplot as plt
# import plotly.graph_objects as go
# import plotly as py
# plt = py.offline.plot
# fh = logging.FileHandler(path,encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# console log
#formatter = logging.Formatter('%(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(ch)
# logger.addHandler(fh)
class Match_stat(object):
    """docstring for ClassName"""
    def __init__(self,update_dataset_and_testset=False):
        self.match_catalog="MATCH_JSON_DIR_0727/"
        with open("hero_id_name.json","r+") as f:
            self.hero_id_name=load(f)
        with open ("hero_id_name_id.json","r+") as f:
            self.hero_id=load(f)
        self.match_files  = [file for file in listdir(self.match_catalog) if file[-4:]=="json" and match("\d{10,}",file[:-5])]
        self.match_normal= [file for file in listdir(self.match_catalog) if file[-4:]=="json" and file[:6]=="normal"]
        self.match_files=self.match_normal+self.match_files
        print (len(self.match_files),len(self.match_normal))
        if update_dataset_and_testset:
            self.save_everymatch_tocsv()
            pre_df1=pd.read_csv("matches_0727.csv")
            pre_df2=pd.read_csv("matches_testset_0727.csv")
            self.pre_lenth=len(pre_df1.append(pre_df2)).pkl
            self.MODEL_NAME='model_'+str(datetime.date.today())+"_"+str(self.pre_lenth)+'.pkl'#"model_2020-07-06.pkl#"model_2020-07-06.pkl"
            print ("新csv:准备生成模型:",self.MODEL_NAME)
        else:
            pre_df1=pd.read_csv("matches_0727_pro.csv")
            pre_df2=pd.read_csv("matches_testset_0727_pro.csv")
            self.pre_lenth=len(pre_df1.append(pre_df2))
            self.MODEL_NAME='model_'+str(datetime.date.today())+"_"+str(self.pre_lenth)+'.pkl'#"model_2020-07-06.pkl#"model_2020-07-06.pkl"
            print ("旧csv:现有模型长度:",self.MODEL_NAME)
        print (self.pre_lenth)
        self.time_limit="2020-06-30 08:54:01"#版本更新比赛的日期格式
        self.real_match={}
        self.game_version="0727"
        self.ua = UserAgent()
        self.headers={"user-agent":self.ua.random}
        self.heroes_released=129
    def gethero_frombanpick(self,banpick):
        direteam,radiantteam=0,0
    def save_everymatch_tocsv(self):
        fname="matches_0727.csv"
        #print ("时长过滤:",len(self.match_files))
        COLUMNS = ['match_id','radiant_win','radiant_team','dire_team','avg_mmr','num_mmr','game_mode','duration','dire_score','radiant_score']#teamfights#draft_timings
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
                if dic_one_match["duration"]>1400 and dic_one_match["game_mode"]==2:
                    self.filter_matchfile.append(match_file)
                    self.right_count+=1
                if dic_one_match["game_mode"] in [22,3] and dic_one_match["duration"]>1000:
                    try:
                        assert dic_one_match["radiant_team"] and dic_one_match["dire_team"]
                        self.mid_count+=1
                        assert len(dic_one_match["radiant_team"].split(","))==5 and len(dic_one_match["dire_team"].split(","))==5
                        self.left_count+=1
                        self.filter_matchfile.append(match_file)
                    except:
                        continue
                        # if "radiant_team" not in dic_one_match:
                        #     radiant,dire=[],[]  
                        #     pickbans=dic_one_match["picks_bans"] 
                        #     for pickbanseq in pickbans:
                        #         if pickbanseq["is_pick"]==True:
                        #                 hero_id=pickbanseq["hero_id"]
                        #                 hero_name=self.hero_id_name[str(hero_id)]
                        #                 if pickbanseq["team"]==1:
                        #                     dire.append(hero_id)
                        #                 else:
                        #                     radiant.append(hero_id)
                        #     dic_one_match["dire_team"]=",".join([str(i) for i in dire])
                        #     dic_one_match["radiant_team"]=",".join([str(i) for i in radiant])
                # print (dic_one_match["radiant_team"])

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
            # print ("比赛数据类型",single_match,len(self.real_match[single_match]),type(self.real_match[single_match]))
            with open(self.match_catalog+one_train_file,"r+",encoding="utf-8") as f:
                dic_one_match=load(f)
                if dic_one_match["game_mode"]==2:
                    radiant,dire=[],[]
                    #win_object=lambda:"radiant" if dic_one_match["randiant_win"] else "dire"
                    pickbans,direid,rid=dic_one_match["picks_bans"],dic_one_match["dire_team_id"],dic_one_match["radiant_team_id"]
                        #print (pickbans)
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
                        # print (dic_one_match["dire_team"])
                        dic_one_match["radiant_team"]=",".join([str(i) for i in radiant])
                        # print (dic_one_match["radiant_team"])
                        dic_one_match["avg_mmr"]=choice(range(6000,6500,20))
                        dic_one_match["num_mmr"]=random.randint(0,9)
                        current_dataframe=pd.json_normalize(dic_one_match)
                        result_dataframe=result_dataframe.append(current_dataframe)
                else:

                    dic_one_match["avg_mmr"]=choice(range(6000,6500,20))
                    dic_one_match["num_mmr"]=random.randint(0,9)
                    current_dataframe=pd.json_normalize(dic_one_match)
                    result_dataframe=result_dataframe.append(current_dataframe)
            self.count_iteration+=1
            # print (self.count_iteration)
        for one_test_file in self.test_files:
            with open(self.match_catalog+one_test_file,"r+",encoding="utf-8") as f:
                dic_test_match=load(f)
                if dic_test_match["game_mode"]==2:
                    radiant,dire=[],[]
                    #win_object=lambda:"radiant" if dic_test_match["randiant_win"] else "dire"
                    pickbans,direid,rid=dic_test_match["picks_bans"],dic_test_match["dire_team_id"],dic_test_match["radiant_team_id"]
                        #print (pickbans)
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
                        # print (dic_test_match["dire_team"])
                        dic_test_match["radiant_team"]=",".join([str(i) for i in radiant])
                        # print (dic_test_match["radiant_team"])
                        dic_test_match["avg_mmr"]=choice(range(6000,6500,20))
                        dic_test_match["num_mmr"]=random.randint(0,9)
                        current_dataframe=pd.json_normalize(dic_test_match)
                        test_dataframe=test_dataframe.append(current_dataframe)
                else:
                    dic_one_match["avg_mmr"]=choice(range(6000,6500,20))
                    dic_one_match["num_mmr"]=random.randint(0,9)
                    current_dataframe=pd.json_normalize(dic_test_match)
                    test_dataframe=test_dataframe.append(current_dataframe)                
                    # print ("add one data frame success")
        print (len(self.match_files),"比较过滤时长后的",len(result_dataframe))
        try:
            pd.DataFrame(result_dataframe,columns=COLUMNS).to_csv(fname,index=False)
            pd.DataFrame(test_dataframe,columns=COLUMNS).to_csv("matches_testset_0727.csv",index=False)
        except:
            assert 1>2,"Fail in creating set"
        return result_dataframe
        #filter_duration=self.real_match.copy()
        #for single_match in filter_duration:
        #    if filter_duration[single_match]["duration"]>1500:
        #        self.real_match.pop(single_match)
        # print (len(self.real_match),len(self.test_files_dict))
        # with open("normal_match_info.json","d+",encoding="utf-8") as f:
        #     dict_normal_to_realmatch.load(f)
        #     for team in dict_normal_to_realmatch:
        #         for pid in dict_normal_to_realmatch[team]:
        #             for one_match in dict_normal_to_realmatch[team][pid]:
        #                 self.real_match[one_match[0]]["radiant_team"]=one_match[2]
        #                 self.real_match[one_match[0]]["dire_team"]=one_match[3]
        #                 self.real_match[one_match[0]]["avg_mmr"]=one_match[-3]
        #                 self.real_match[one_match[0]]["radiant_win"]=one_match[-2]
        #                 self.real_match[one_match[0]]["duration"]=one_match[-1]
        #                 self.real_match[one_match[0]]["game_mode"]=one_match[-4]
        #                 self.real_match[one_match[0]]["match_id"]=one_match[0]
            #     illegal_banpick.append(single_match)
        # print("没有十个暂时不存储到csv:",len(illegal_banpick))
        # for i in illegal_banpick:
            # print ("检查banpick字典",i)
        # for il in illegal_banpick:
            # self.real_match.pop(il)

    def iterate_file(self):#创建所以重要比赛的dict字典,并且验证id是否正确.
        self.rigth_count,need_to_fix=0,[]
        for match in self.match_files:
            with open (self.match_catalog+"/"+match,"r+",encoding="utf-8") as f:
                dict_match=load(f)
                if not dict_match["picks_bans"]:
                    continue
            self.real_match[match[:-5]]=dict_match
            # if dict_match["game_mode"]==2:
            # print(type(dict_match),match)
            # elif dict_match["game_mode"]==1 or dict_match["game_mode"]==3:
            #     self.real_match[match[:-5].split("_")[-1]]=dict_match
        # print (256,">",len(self.real_match))
        for rm in self.real_match:
            if str(self.real_match[rm]["match_id"])==rm.split("_")[-1]:
                self.rigth_count+=1
            else:
                print (rm,"!=",self.real_match[rm]["match_id"])
                need_to_fix.append(rm)
            # if not self.real_match[rm]["picks_bans"]:
                # print ("删除没有选人数据的比赛:",rm,len(self.real_match))
                # self.real_match.pop(rm)
        print("过滤掉中单模式的比赛:",self.rigth_count)
        # print(need_to_fix)
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
        if low_mmr:
            dataset_df = dataset_df[dataset_df.avg_mmr > low_mmr]
        if high_mmr:
            dataset_df = dataset_df[dataset_df.avg_mmr < high_mmr]
        logger.info("The dataset contains %d games", len(dataset_df))
        if advantages:
            logger.info("Computing advantages...")
            advantages_list = self.compute_advantages(dataset_df)
            # print (advantages_list[0]["winrate"].max())
            # print (advantages_list[1]["winrate"].max())
            # assert 1>2
            # for i in advantages_list:
                # print (i.shape)
        else:
            logger.info("Loading advantages from files...")
            synergies = np.loadtxt('pretrained/synergies_all_0727.csv')
            counters = np.loadtxt('pretrained/counters_all_0727.csv')
            advantages_list = [synergies, counters]
        logger.info("Transforming dataframe in feature map...")
        feature_map = self.dataset_to_features(dataset_df, advantages=advantages_list)
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
        #print (len(dataset_np))
        for row_amatch in dataset_np:
            self.update_dicts(row_amatch, self.synergy, self.counter)
        self.compute_winrates(self.synergy, self.counter, self.heroes_released)
        self.synergy_matrix,self.counter_matrix =self.calculate_advantages(self.synergy, self.counter, self.heroes_released)
        #print (self.synergy_matrix)
        #print (self.counter_matrix)
        # assert 1>2
        np.savetxt('pretrained/synergies_all_0727.csv', self.synergy_matrix)
        np.savetxt('pretrained/counters_all_0727.csv',self.counter_matrix)
        return [self.synergy_matrix, self.counter_matrix]
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
        for i in range(5):
            for j in range(5):
                if i != j:
                    # print (len(radiant_heroes))
                    # print ("错误",radiant_heroes[i],radiant_heroes[j])
                    # print ("错误",type(radiant_heroes[i]),type(radiant_heroes[j]))
                    #synergy['games'][]
                    # print (synergy["games"].shape)
                    synergy['games'][radiant_heroes[i] - 1, radiant_heroes[j] - 1] += 1
                    synergy['games'][dire_heroes[i] - 1, dire_heroes[j] - 1] += 1

                    if radiant_win:
                        synergy['wins'][radiant_heroes[i] - 1, radiant_heroes[j] - 1] += 1
                    else:
                        synergy['wins'][dire_heroes[i] - 1, dire_heroes[j] - 1] += 1

                counter['games'][radiant_heroes[i] - 1, dire_heroes[j] - 1] += 1
                counter['games'][dire_heroes[i] - 1, radiant_heroes[j] - 1] += 1

                if radiant_win:
                    counter['wins'][radiant_heroes[i] - 1, dire_heroes[j] - 1] += 1
                else:
                    counter['wins'][dire_heroes[i] - 1, radiant_heroes[j] - 1] += 1
    def compute_winrates(self,synergy, counter, heroes_released):
        for i in range(heroes_released):
            for j in range(heroes_released):
                if i!=j:
                    if synergy['games'][i, j] != 0:
                        synergy['winrate'][i, j] = synergy['wins'][i, j]/float(synergy['games'][i, j])
                            # print ("hero",i,j,synergy['winrate'][i, j])
                    if counter['games'][i, j] != 0:
                        counter['winrate'][i, j] = counter['wins'][i, j]/float(counter['games'][i, j])
                        # print ("hero",i,j,counter['winrate'][i, j])
    def calculate_advantages(self,synergy, counter, heroes_released):
        synergies = np.zeros((heroes_, heroes_released))
        counters = np.zeros((heroes_released, heroes_released))                                
        base_winrate = np.zeros(heroes_released)
        for i in range(heroes_released):
            if np.sum(synergy['games'][i])!=0:
                base_winrate[i] = np.sum(synergy['wins'][i]) / np.sum(synergy['games'][i])
                #print (synergy["wins"][i],synergy["games"][i],synergy["winrate"][i])
                # print (base_winrate[i],i)
        for i in range(heroes_released):
            for j in range(heroes_released):
                if i!=j:
                    if synergy['games'][i, j] > 0:
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
        heroes_released = 129
        synergy_matrix, counter_matrix = None, None
        if advantages:
            x_matrix = np.zeros((dataset_df.shape[0], 2 * heroes_released + 3))
            [synergy_matrix, counter_matrix] = advantages
        else:
            x_matrix = np.zeros((dataset_df.shape[0], 2 * heroes_released))
        y_matrix = np.zeros(dataset_df.shape[0])
        dataset_np = dataset_df.values
        for i, row in enumerate(dataset_np):
            radiant_win = row[1]
            radiant_heroes = list(map(int, row[2].split(',')))
            dire_heroes = list(map(int, row[3].split(',')))

            for j in range(5):
                x_matrix[i, radiant_heroes[j] - 1] = 1
                x_matrix[i, dire_heroes[j] - 1 + heroes_released] = 1
                if advantages:
                    x_matrix[i, -3:] = self.augment_with_advantages(synergy_matrix,
                                                               counter_matrix,
                                                               radiant_heroes,
                                                               dire_heroes)
            y_matrix[i] = 1 if radiant_win else 0
        return [x_matrix, y_matrix]
    def augment_with_advantages(self,synergy, counter, radiant_heroes, dire_heroes):
        synergy_radiant = 0
        synergy_dire = 0
        counter_score = 0
        for i in range(5):
            for j in range(5):
                if i > j:
                    synergy_radiant += synergy[radiant_heroes[i] - 1][radiant_heroes[j] - 1]
                    synergy_dire += synergy[dire_heroes[i] - 1][dire_heroes[j] - 1]
                counter_score += counter[radiant_heroes[i] - 1][dire_heroes[j] - 1]
        return np.array([synergy_radiant, synergy_dire, counter_score])
    def create_testset(self):
        result_dataframe=pd.DataFrame()
        fname="matches_testset_0727.csv"
        COLUMNS = ['match_id','radiant_win','radiant_team','dire_team','avg_mmr','num_mmr','game_mode', 'lobby_type','duration','draft_timings','dire_score','radiant_score']#teamfights
        for single_testset_match in self.test_files_dict:
            current_dataframe=pd.json_normalize(self.test_files_dict[single_testset_match])
            result_dataframe=result_dataframe.append(current_dataframe)
        pd.DataFrame(result_dataframe,columns=COLUMNS).to_csv(fname,index=False)
        return result_dataframe
    def train(self,advantages_nouse_pretrain=True):
        print (advantages_nouse_pretrain)
        dataset_train, _ = self.read_dataset('matches_0727.csv', low_mmr=6000,advantages=advantages_nouse_pretrain)
        dataset_test, _ = self.read_dataset('matches_testset_0727.csv', low_mmr=6000,advantages=advantages_nouse_pretrain)
        print (len(dataset_train),len(dataset_test))
        result=self.evaluate(dataset_train, dataset_test, cv=7, save_model=self.MODEL_NAME)
        return result
    def evaluate(self,train_data, test_data, cv=5, save_model=None):
        x_train, y_train = train_data
        x_test, y_test = test_data
        scaler = StandardScaler()
        scaler.fit(x_train)
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)
        cross_val_mean = -1
        if cv > 0:
            model = LogisticRegression(C=0.005, random_state=42)
            cross_val_scores = cross_val_score(model, x_train, y_train, cv=cv, scoring='roc_auc',
                                               n_jobs=-1)
            cross_val_mean = np.mean(cross_val_scores)
            logger.info("Cross validation scores over the training set (%d folds): %.3f +/- %.3f", cv,
                        cross_val_mean,
                        np.std(cross_val_scores))
        model = LogisticRegression(C=0.005, random_state=42)
        model.fit(x_train, y_train)
        probabilities = model.predict_proba(x_test)
        roc_auc = roc_auc_score(y_test, probabilities[:, 1])
        labels = model.predict(x_test)
        acc_score = accuracy_score(y_test, labels)
        if save_model:
            model_dict = {}
            model_dict['scaler'] = scaler
            model_dict['model'] = model
            joblib.dump(model_dict, save_model)
        logger.info("Test ROC AUC: %.3f", roc_auc)
        logger.info("Test accuracy score: %.3f", acc_score)
        return (x_train.shape[0], x_test.shape[0], cross_val_mean, roc_auc, acc_score)
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
    def query_full(self,model,scaler,radiant_heroes,dire_heroes,synergies,counters,heroes_released):
        # print("using_model:",model)
        features = np.zeros(2 * heroes_released + 3)
        for i in range(5):
            features[radiant_heroes[i] - 1] = 1
            features[dire_heroes[i] - 1 + heroes_released] = 1
        extra_data = self.augment_with_advantages(synergies, counters, radiant_heroes, dire_heroes)
        features[-3:] = extra_data

        features_reshaped = features.reshape(1, -1)
        features_final = scaler.transform(features_reshaped)

        probability = model.predict_proba(features_final)[:, 1] * 100

        if probability > 50:
            return "Radiant has %.3f%% chance" % probability
        else:
            return "Dire has %.3f%% chance" % (100 - probability)
    def query(self,mmr,radiant_heroes, dire_heroes, synergies=None, counters=None, similarities=None):
        # if similarities is None:
        #     sims = np.loadtxt('pretrained/similarities_all.csv')
        # else:
        #     sims = np.loadtxt(similarities)
        if counters is None:        
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
        #elif mmr > 5000
        model_dict = joblib.load(self.MODEL_NAME)
        logger.info("Using 5000-10000 MMR model")
        # else:
        #     file_list = [int(valid_file[:4]) for valid_file in listdir('pretrained')
        #                  if '.pkl' in valid_file]
        #     file_list.sort()            
        #     min_distance = 10000
        #     final_mmr = -1000
        #     for model_mmr in file_list:
        #         if abs(mmr - model_mmr) < min_distance:
        #             min_distance = abs(mmr - model_mmr)
        #             final_mmr = model_mmr
        #     logger.info("Using closest model available: %d MMR model", final_mmr)            
        #     model_dict = joblib.load(os.path.join("pretrained", str(final_mmr) + ".pkl"))
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

        # query for the result given the 4v5 or 5v4 configuration in a game around 3000 average MMR
        # radiant team: Huskar, Clinkz, Lifestealer, Luna, Lich
        # dire team: Venomancer, Faceless Void, Leshrac, Ancient Apparition
        # the missing element of the 2nd list is the one the suggestion is made for
        # the result is a list of (hero, (win_chance, overall_team_similarity)) sorted by win_chance
        # partial_result = self.query(6000,
        #                        [59, 56, 54, 48, 31],
        #                        [40, 41, 52, 68])
        # logger.info("The result of the partial query is: \n%s", partial_result)
    def get_teamid_tostr(self,rtid,dtid):
        urlprefix="https://api.opendota.com/api/teams/"
        #print(rtid,dtid,len(self.teamid_to_name))
        if rtid in self.teamid_to_name:
            rname=self.teamid_to_name[rtid]["fullname"]
        else:
            rname=rtid
        if dtid in self.teamid_to_name:
            dname=self.teamid_to_name[dtid]["fullname"]
        else:
            dname=dtid
        return rname,dname
        # else:
        #     req_object_1=get(urlprefix+str(rtid),headers=self.headers)
        #     if req_object_1.status_code==200:
        #         rname=loads(req_object_1.text)["name"]
        #         teamid_to_name[rtid]=rname
        # else:
        #     req_object_2=get(urlprefix+str(dtid),headers=self.headers)
        #     if req_object_2.status_code==200:
        #         dname=loads(req_object_2.text)["name"]
        #         teamid_to_name[dtid]=dname
        # with open("teamid_to_name.json","w+",encoding="utf-8") as f:
        #     dump(teamid_to_name,f,ensure_ascii=True)
        #sleep(1)
    def get_match_bp(self):
        self.match_url=[]
        from dotadata_mining_banpick import Ban_Pick
        radiant,dire=[],[]
        radiant_name,dire_name={},{}
        instance=Ban_Pick()
        print (instance.match_url,"比赛实时列表长度:",len(instance.match_url))
        for one_full_url in instance.match_url:
            radiant_full,dire_full,rname,dname=instance.get_content(one_full_url)
            radiant_name[rname]=[]
            dire_name[dname]=[]
            for teamel_a,teamel_b in zip(radiant_full,dire_full):
                radiant.append(teamel_a["_id"])
                dire.append(teamel_b["_id"])
                radiant_name[rname].append(teamel_a["name_zh"])
                dire_name[dname].append(teamel_b["name_zh"])         
            if len(radiant)==5 and len(dire)==5:
                    full_result=self.query(6000,radiant,dire)
                    confirm=full_result.split(" ")[0].lower()
                    print ("预测结果:%s ----r:%s:%s vs d:%s:%s"%(full_result,rname,radiant_name[rname],dname,dire_name[dname]))
            radiant_5=radiant
            dire_5=dire
            print(radiant,"vs",dire)
            self.pick_statistics(radiant_5,dire_5)
            radiant,dire=[],[]
        #print (radiant,dire,type(radiant[0]),type(dire[0]))
        return radiant,dire,rname,dname
    def single_query(self):
        radiant,dire,rname,dname=self.get_match_bp()
        full_result=self.query(6000,radiant,dire)
        confirm=full_result.split(" ")[0].lower()
        # self.get_teamid_tostr(str(rtid),str(dtid))
        print ("预测结果:%s ----r:%s vs d:%s"%(full_result,rname,dname))
            # print (mid)
    def team_value(self):
        return
    def pick_statistics(self, mmr_info="1"):
        self.pick_dict,self.win_dict,self.win_rate={},{},{}
        for i in self.hero_id:
            self.pick_dict[self.hero_id[i]]=0
            self.win_dict[self.hero_id[i]]=0
            self.win_rate[self.hero_id[i]]=0 

        # pick_rate = games / np.sum(games)
        df=pd.read_csv("matches_0727.csv")
        df_test=pd.read_csv("matches_testset_0727.csv")
        print (len(df),len(df_test))
        assert 1>2
        for i,j,rw in zip(df.radiant_team,df.dire_team,df.radiant_win):
            a,b=i.split(","),j.split(",")
            for i,j in zip(a,b):
                self.pick_dict[self.hero_id[i]]+=1
                self.pick_dict[self.hero_id[j]]+=1
                if rw:
                    self.win_dict[self.hero_id[i]]+=1
                if not rw:
                    self.win_dict[self.hero_id[j]]+=1  
        # print (len(self.pick_dict))
        pick_listto_sort=self.pick_dict.items()
        x=sorted(pick_listto_sort,key=lambda x:x[1])
        # print (x)
        self.cr,self.cd=[self.hero_id[str(i)] for i in self.r],[self.hero_id[str(i)] for i in self.d]
        # print (self.cr,self.cd)
        rad_p,dire_p=[],[]
        for i,j in zip(self.cr,self.cd):
            rad_p.append([i,self.pick_dict[i]])
            dire_p.append([j,self.pick_dict[j]])
        print ("两边总统计数:",rad_p,"vs",dire_p)


        #assert 1>2
        # pick_rate_dict = dict()
        # win_dcit=dict()
        # hero_dict = self.hero_id
        # for heronum in range(1,130):
        #     try:
        #         pick_rate_dict[hero_dict[str(heronum)]] = [games[heronum-1],wins[heronum-1],games[heronum-1]-wins[heronum-1],(wins[heronum-1])/games[heronum-1]]#wins[heronum-1]/games[heronum-1]]
        #     except:
        #         continue
        # sorted_pickrates = sorted(pick_rate_dict.items(), key=operator.itemgetter(1))
        # print (sorted_pickrates[0])
        # # assert 1>2
        # print (len(sorted_pickrates))
        # x_plot_data = [x[0] for x in sorted_pickrates]
        # total_plot_data = [x[1][0] for x in sorted_pickrates]
        # win_plot_data=[x[1][1] for x in sorted_pickrates]
        # lose_plot_data=[x[1][2] for x in sorted_pickrates]

        # xrange_num=np.arange(0,80,1)
        # print (x_plot_data,len(x_plot_data))
        # print (y_plot_data,len(y_plot_data))
        # title = 'Hero pick rates at ' + ' MMR'
        # y=np.arange(119)
        # plot1=plt.barh(y,total_plot_data,align='center')
        # print (win_plot_data+lose_plot_data)
        # plot1=plt.barh(x_plot_data,total_plot_data)
        # plt.yticks(y,win_plot_data)
        # plt.xticks(xrange_num)
        # plot1=plt.barh(y,lose_plot_data,left=win_plot_data,align='center')
        # plot2=plt.barh(win_plot_data,x_plot_data,align='center')
        # ax.invert_yaxis()
        # plt.xlabel("pick num")
        # plt.title("hero picks")
        # plt.show()
        # sorted_pickrates = sorted(pick_rate_dict.items(), key=lambda r:r[1][3])
        # lose_rate=[x[1][3] for x in sorted_pickrates]
        # x_plot_data = [x[0] for x in sorted_pickrates]
        # plt.bar(lose_rate,y,align='center')
        # xrange_num=np.arange(0,1,0.05)
        # plt.yticks(y,x_plot_data)    
        # plt.title("hero loserate")
        # plt.xticks(xrange_num)
        # plt.show()
    def winrate_statistics(self,dataset_df, mmr_info="1"):
        x_data, y_data = dataset_df

        wins = np.zeros(129)
        games = np.zeros(129)
        winrate = np.zeros(129)

        for idx, game in enumerate(x_data):
            for i in range(258):
                if game[i] == 1:
                    games[i % 129] += 1

                    if y_data[idx] == 1:
                        if i < 129:
                            wins[i] += 1
                    else:
                        if i >= 129:
                            wins[i - 129] += 1
        winrate = wins / games
        winrate_dict = dict()
        hero_dict = self.hero_id
        for i in range(129):
            try:
                winrate_dict[hero_dict[str(i)]] = winrate[i]
            except:
                continue
        sorted_winrates = sorted(winrate_dict.items(), key=operator.itemgetter(1))
        x_plot_data = [x[0] for x in sorted_winrates]
        y_plot_data = [x[1] for x in sorted_winrates]
        title = 'Hero winrates at ' + mmr_info + ' MMR'
        data = [go.Bar(
            y=x_plot_data,
            x=y_plot_data,
            orientation='h'
        )]
        layout = go.Layout(
            title=title,
            width=1000,
            height=1400,
            yaxis=dict(title='hero',
                       ticks='',
                       nticks=129,
                       tickfont=dict(
                           size=8,
                           color='black')
                       ),
            xaxis=dict(title='win rate',
                       nticks=30,
                       tickfont=dict(
                           size=10,
                           color='black')
                       )
        )
        fig = go.Figure(data=data, layout=layout)
        plt(data, filename='hero_win_1.html')
    def plot_learning_curve(self,x_train, y_train, subsets=200, mmr=None, cv=5, tool='matplotlib'):
        x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2)
        subset_sizes = np.exp(np.linspace(3, np.log(len(y_train)), subsets)).astype(int)
        results_list = [[], []]
        for subset_size in subset_sizes:
            logger.info('Performing cross validation on subset_size %d', subset_size)
            _, _, cv_score, roc_auc, _ = self.evaluate([x_train[:subset_size], y_train[:subset_size]],
                                                  [x_test, y_test], cv=cv)
            results_list[0].append(1 - cv_score)
            results_list[1].append(1 - roc_auc)
        if tool == 'matplotlib':
            self.plot_matplotlib(subset_sizes, results_list, mmr)
        #else:
            #plot_plotly(subset_sizes, results_list, mmr)
    def plot_matplotlib(self,subset_sizes, data_list, mmr):
        """ Plots learning curve using matplotlib backend.
        Args:
            subset_sizes: list of dataset sizes on which the evaluation was done
            data_list: list of ROC AUC scores corresponding to subset_sizes
            mmr: what MMR the data is taken from
        """
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
    def plot_plotly(self,subset_sizes, data_list, mmr):
        """ Plots learning curve using plotly backend.
        Args:
            subset_sizes: list of dataset sizes on which the evaluation was done
            data_list: list of ROC AUC scores corresponding to subset_sizes
            mmr: what MMR the data is taken from
        """
        if mmr:
            title = 'Learning curve plot for %d MMR' % mmr
        else:
            title = 'Learning curve plot'

        trace0 = go.Scatter(
            x=subset_sizes,
            y=data_list[0],
            name='Cross validation error'
        )
        trace1 = go.Scatter(
            x=subset_sizes,
            y=data_list[1],
            name='Test error'
        )
        data = go.Data([trace0, trace1])

        layout = go.Layout(
            title=title,

            xaxis=dict(
                title='Dataset size (logspace)',
                type='log',
                autorange=True,
                titlefont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='Error',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=15,
                    color='#7f7f7f'
                )
            )
        )
        fig = go.Figure(data=data, layout=layout)
        py.iplot(fig, filename='learning_curve_%dMMR' % mmr)
    def feture_vector_space(self,model,scalar,radiant_heroes,dire_heroes,synergies,counters,similarities,hero_released):
        return
    def match_duration(self,model,scalar,radiant_heroes,dire_heroes,synergies,counters,similarities,hero_released):
        return
    def match_team(self):
        return 
    def real_validation_set(self):
        with open("teamid_to_name_0727.json","r+",encoding="utf-8") as f:
            self.teamid_to_name=load(f)
        df1,df2=pd.read_csv("matches_0727.csv"),pd.read_csv("matches_testset_0727.csv")
        test_and_data_set=list(df1.match_id)+list(df2.match_id)
        correct,total=0,0
        self.real_validation=[i for i in os.listdir("real_validation_0727")]
        print(len(self.real_validation))
        self.predict_wrong=[]
        for amatch in self.real_validation:
            radiant,dire=[],[]
            mid=amatch[:-5]
            with open("real_validation_0727/"+amatch,"r+",encoding="utf-8") as f:
                amatch_dict=load(f)
            if mid not in test_and_data_set:
                w=lambda:"radiant" if amatch_dict["radiant_win"] else "dire"
                rtid,dtid=amatch_dict["radiant_team_id"],amatch_dict["dire_team_id"]
                #print(self.teamid_to_name[rtid],self.teamid_to_name[dtid])
                rname,dname=self.get_teamid_tostr(str(rtid),str(dtid))
                win_object=w()
                pickbans=amatch_dict["picks_bans"]
                self.no_pickbans_match=0
                if pickbans:
                    for a_pickban in pickbans:
                        if a_pickban["is_pick"]==True:
                                hero_id=a_pickban["hero_id"]
                                hero_name=self.hero_id_name[str(hero_id)]
                                if a_pickban["team"]==1:
                                    dire.append(int(hero_id))
                                else:
                                    radiant.append(int(hero_id))                
                    # print("双方阵容:",radiant,dire)
                    full_result=self.query(6000,radiant,dire)
                    confirm,percentage=full_result.split(" ")[0].lower(),full_result.split(" ")[2]         
                    # print ("预测结果:%s ----r:%s vs d:%s"%(full_result,rname,dname))
                    rate=float(percentage[:-1])
                    if win_object==confirm and rate>50 and rate<80:
                        correct+=1
                    else:
                        self.predict_wrong.append([mid,rname,dname])
                    if rate>50 and rate<80:
                        total+=1
                else:
                    self.no_pickbans_match+=1
        print ("预测正确的",correct,"总实际比赛",total,"正确率",correct/total)#"缺少banpick数据的",self.no_pickbans_match
        print("预测错误的:",self.predict_wrong)
    def model_validate(self,match_set_filename):
        f="F:\\cl\\reqdotadata\\data_recent_mmr\\"+match_set_filename#"matches_0727.csv"
        real_test_set=pd.read_csv(f,encoding="utf-8")[:3000]
        right,total=0,len(real_test_set)
        print("实际验证模型长度:",total)
        dire_count,radiant_count=0,0
        count=0
        count_80=0
        for one_game in real_test_set.values:
            radiant_team, dire_team ,radiant_win= one_game[2], one_game[3], one_game[4]
            radiant,dire=[int(i) for i in radiant_team.split(",")],[int(i) for i in dire_team.split(",")]
            # print (radiant,dire)
            full_result=self.query(6000,radiant,dire)
            confirm,percentage=full_result.split(" ")[0].lower(),full_result.split(" ")[2]         
            rate=float(percentage[:-1])
            if rate>52 and rate<98:
                count_80+=1
                if confirm=="radiant" and radiant_win:
                    right+=1
                elif confirm=="dire" and not radiant_win:
                    right+=1
                count +=1
        return "学习器:正确数,统计总数,正确率,错误数",right,count_80,right/count,total-right,radiant_count,dire_count,match_set_filename

            # if rate>80:
            #     if confirm=="radiant" and not radiant_win:
            #         right+=1        
            #     elif confirm=="dire" and radiant_win:
            #         right+=1
            # print (full_result)
    def random_predict(self,match_set_filename):
        f="F:\\cl\\reqdotadata\\data_recent_mmr\\"+match_set_filename#"matches_0727.csv"
        real_test_set=pd.read_csv(f,encoding="utf-8")[:3000]
        # print (real_test_set.head())
        right,total=0,len(real_test_set)
        dire_count,radiant_count=0,0
        # for i in os.listdir("."):
        # assert 1>2
        right,count_total=0,0
        for one_game in real_test_set.values:
            radiant_team, dire_team ,radiant_win= one_game[2], one_game[3], one_game[4]
            radiant,dire=[int(i) for i in radiant_team.split(",")],[int(i) for i in dire_team.split(",")]
            count_total+=1
            #rate=float(percentage[:-1])
            result=random.randint(0,1)
            if result==1 and radiant_win:
                right+=1
            elif result==0 and not radiant_win:
                right+=1
            if radiant_win:
                radiant_count+=1
            else:
                dire_count+=1
        return "随机预测:正确数,统计总数,正确率,错误数",right,count_total,right/count_total,count_total-right,radiant_count,dire_count
    def pick_statistics(self,ra5=None,di5=None,mmr_info="1"):
        self.pick_dict,self.win_dict,self.win_rate={},{},{}
        for i in self.hero_id:
            self.pick_dict[self.hero_id[i]]=0
            self.win_dict[self.hero_id[i]]=0
            self.win_rate[self.hero_id[i]]=0 
        # pick_rate = games / np.sum(games)
        df=pd.read_csv("matches_0727.csv")
        df_test=pd.read_csv("matches_testset_0727.csv")
        for i,j,rw in zip(df.radiant_team,df.dire_team,df.radiant_win):
            a,b=i.split(","),j.split(",")
            for i,j in zip(a,b):
                self.pick_dict[self.hero_id[i]]+=1
                self.pick_dict[self.hero_id[j]]+=1
                if rw:
                    self.win_dict[self.hero_id[i]]+=1
                if not rw:
                    self.win_dict[self.hero_id[j]]+=1      

        for i in self.pick_dict:
            fraction_format="%s/%s"%(self.win_dict[i],self.pick_dict[i])
            self.win_rate[i]=[fraction_format,round(self.win_dict[i]/self.pick_dict[i],3)]
        # print (self.win_rate)
        #self.win_rate[self.hero_id[i]]=["%s/%s"%(self.win_dict[self.hero_id[i]],self.pick_dict[self.hero_id[i]]),round(self.win_dict[self.hero_id[i]]/self.pick_dict[self.hero_id[i]],2)]
        #self.win_rate[self.hero_id[j]]=["%s/%s"%(self.win_dict[self.hero_id[i]],self.pick_dict[self.hero_id[i]]),round(self.win_dict[self.hero_id[j]]/self.pick_dict[self.hero_id[j]],2)]

        # print (self.pick_dict)
        # print (len(self.pick_dict))
        pick_listto_sort=self.pick_dict.items()
        win_listto_sort=self.win_dict.items()
        winrate_listto_sort=self.win_rate.items()
        # print (self.win_dict,self.win_rate)
        pick_view=sorted(pick_listto_sort,key=lambda x:x[1])
        win_view=sorted(win_listto_sort,key=lambda x:x[1])
        winrate_view=sorted(winrate_listto_sort,key=lambda x:x[1][1])
        # print (winrate_view)
        if ra5 and di5:
            self.cr,self.cd=[self.hero_id[str(i)] for i in ra5],[self.hero_id[str(i)] for i in di5]
            # print (self.cr,self.cd)
            rad_p,dire_p=[],[]
            for i,j in zip(self.cr,self.cd):
                rad_p.append([i,self.pick_dict[i]])
                dire_p.append([j,self.pick_dict[j]])
            print ("两边总统计数:",rad_p,"vs",dire_p)

FILE_VALIDATE_SET=["matches_list_ranking_2e6.csv"]#[i for i in listdir("data_recent_mmr") if i[:3]=="exp"]#
#"exp_10000.csv"
print (len(FILE_VALIDATE_SET),":一共这么多文件")

high_mmr_validation=True
sommatch_validation=True
preview=False
print ("start..")
instance=Match_stat()#update_dataset_and_testset=True
if high_mmr_validation==True:
    for file in FILE_VALIDATE_SET:
        preview_result=instance.model_validate(file)
        random_result=instance.random_predict(file)
        with open("model_test.txt","a+",encoding="utf-8") as f:
            f.seek(0)
            print (preview_result,file=f)
            print (random_result,file=f)
            print (instance.MODEL_NAME,file=f)

if sommatch_validation==True:
    instance.real_validation_set()

#x=instance.model_rank()

    # print (x)
    # instance.save_everymatch_tocsv()#creoate dataset
    # print (instance.match_normal,len(instance.match_normal))
    # instance.iterate_file()
    # instance.create_testset()#create testset
    # instance.get_match_bp()
    # instance.single_query()
    # instance.real_validation_set()
        # a,al=instance.read_dataset("matches_0727.csv",advantages=True)
        # b,bl=instance.read_dataset("matches_testset_0727.csv",advantages=True)
        # instance.get_heroid_content()
        # instance.pick_statistics()
    # instance.winrate_statistics(a)
# instance.get_heroid_content()
# b,al=instance.read_dataset("matches_testset.csv",advantages=True)
# evl_result=instance.evaluate(a,b,cv=5,save_model="model_"+str(datetime.date.today())+".pkl")
# instance.plot_learning_curve(a[0],a[1],subsets=200,cv=3,mmr=6000,tool='matplotlib')
# print (evl_result)
# instance.query_example()
# print (evl_result)

#instance.get_heroid_content()

#logger.info("First 5 rows from the mined dataframe are: \n%s", mined_df.head().to_string())



# instance.iterate_file()
#求二分组合后的二分排列
#求二分组后的子集,求10的子集,求10,<5的子集
#创造特征向量([1,1,0,1,1,0])
#根据特征向量的值决定预测值
#调整特征向量的取值决定,调整特征向量本身
#instance.d()
#instance.get_heroid_content()
#instance.build_team_hero_dict()
#instance.all_match_bp()
# x=instance.get_heroid_content()
# print (x)
