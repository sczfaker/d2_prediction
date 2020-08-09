#coding:utf-8
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
import time
import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
import joblib
import matplotlib.pyplot as plt
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(ch)

class Match_stat(object):
    """docstring for ClassName"""
    def __init__(self,trainmode=None):
        self.match_catalog="MATCH_JSON_DIR_0727/"
        with open("hero_id_name.json","r+") as f:
            self.hero_id_name=load(f)
        with open ("hero_name_id.json","r+") as f:
            self.hero_name_id=load(f)
        backdate_model=""#以前的模型pkl需要以前的pretrain数据也就是counter和syn
        self.match_files  = [file for file in listdir(self.match_catalog) if file[-4:]=="json" and match("\d{10,}",file[:-5])]
        self.match_normal= [file for file in listdir(self.match_catalog) if file[-4:]=="json" and file[:6]=="normal"]
        self.match_files=self.match_files#self.match_normal
        print (len(self.match_files),len(self.match_normal))
        self.time_limit="2020-06-29 08:54:01"#版本更新比赛的日期格式
        struct_time_limit=time.strptime(self.time_limit,"%Y-%m-%d %H:%M:%S")
        self.sec_time=time.mktime(struct_time_limit)
        self.train_pro_csv="matches_0727_pro.csv"
        self.test_pro_csv="matches_testset_0727_pro.csv"
        if trainmode=="pro":
            self.save_everymatch_tocsv()
            print("创建新的测试集和训练集完毕...")
            pre_df1=pd.read_csv(self.train_pro_csv)
            pre_df2=pd.read_csv(self.test_pro_csv)
            self.pre_lenth=len(pre_df1.append(pre_df2))
            newest_model='promodel_'+str(datetime.date.today())+"_"+str(self.pre_lenth)+'.pkl'#"model_2020-07-06.pkl#"model_2020-07-06.pkl"
            self.MODEL_NAME=newest_model#
            print ("新csv:准备生成模型:",self.MODEL_NAME)
        elif trainmode=="4430":
            self.create_testset_csv_4430()
            newest_model='promodel_'+str(datetime.date.today())+"_"+str(self.pre_lenth)+'.pkl'#"model_2020-07-06.pkl#"model_2020-07-06.pkl"
            self.MODEL_NAME=newest_model#
        else:
            pre_df1=pd.read_csv(self.train_pro_csv)
            pre_df2=pd.read_csv(self.test_pro_csv)
            self.pre_lenth=len(pre_df1.append(pre_df2))
            newest_model='model_'+str(datetime.date.today())+"_"+str(self.pre_lenth)+'.pkl'#"model_2020-07-06.pkl#"model_2020-07-06.pkl"
            print (newest_model)
            self.MODEL_NAME=newest_model#
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
        fname="matches_list_ranking_2e6.csv"
        total_csv=read_csv(fname)
        self.pre_lenth=len(total_csv)
        COLUMNS = ['match_id','radiant_win','radiant_team','dire_team',"start_time",'avg_mmr','num_mmr','game_mode','duration','dire_score','radiant_score']#teamfights#draft_timings
        train_set, test_set = train_test_split(total_csv, test_size=0.2, random_state=42)
        pd.DataFrame(train_set,columns=COLUMNS).to_csv("matches_0727.csv",index=False)
        pd.DataFrame(test_set,columns=COLUMNS).to_csv("matches_testset_0727.csv",index=False)
    def save_everymatch_tocsv(self):
        #print ("时长过滤:",len(self.match_files))
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
        self.RATIO_TESET=len(self.match_files)//20
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
                    dic_one_match["avg_mmr"]=choice(range(6000,6700,20))
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
            pd.DataFrame(result_dataframe,columns=COLUMNS).to_csv(self.train_pro_csv,index=False)
            pd.DataFrame(test_dataframe,columns=COLUMNS).to_csv(self.test_pro_csv,index=False)
        except:
            assert 1>2,"Fail in creating set"
        return result_dataframe
    def iterate_file(self):#创建所以重要比赛的dict字典,并且验证id是否正确.
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
            synergies = np.loadtxt('pretrained/synergies_all_0727_pro.csv')
            counters = np.loadtxt('pretrained/counters_all_0727_pro.csv')
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
        print ("value长度",len(dataset_np),"总长度",len(dataset_df))
        for row_amatch in dataset_np:
            self.update_dicts(row_amatch, self.synergy, self.counter)
        self.compute_winrates(self.synergy, self.counter, self.heroes_released)
        self.synergy_matrix,self.counter_matrix =self.calculate_advantages(self.synergy, self.counter, self.heroes_released)
        #print (self.synergy_matrix)
        #print (self.counter_matrix)
        # assert 1>2
        np.savetxt('pretrained/synergies_all_0727_pro.csv', self.synergy_matrix)
        np.savetxt('pretrained/counters_all_0727_pro.csv',self.counter_matrix)
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
        synergies = np.zeros((heroes_released, heroes_released))
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
    def train(self,advantages_update_pretrain=True):
        print (advantages_update_pretrain)
        dataset_train, _ = self.read_dataset(self.train_pro_csv,advantages=advantages_update_pretrain)
        dataset_test, _ = self.read_dataset(self.test_pro_csv,advantages=advantages_update_pretrain)
        print (len(dataset_train),len(dataset_test))
        result=self.evaluate(dataset_train, dataset_test, cv=15, save_model=self.MODEL_NAME)
        return result
    def evaluate(self,train_data, test_data,cv=3,save_model=None):
        x_train, y_train = train_data
        x_test, y_test = test_data
        scaler = StandardScaler()
        scaler.fit(x_train)
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)
        cross_val_mean = -1
        if cv > 0:
            model = LogisticRegression(C=0.005, random_state=57)
            cross_val_scores = cross_val_score(model, x_train, y_train, cv=cv, scoring='roc_auc',
                                               n_jobs=-1)
            cross_val_mean = np.mean(cross_val_scores)
            logger.info("Cross validation scores over the training set (%d folds): %.3f +/- %.3f", cv,
                        cross_val_mean,
                        np.std(cross_val_scores))
        model = LogisticRegression(C=0.005,solver="sag",max_iter=1000, random_state=58)
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
        self.x_train,self.y_train=x_train,y_train
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
        print("using_model:",model)
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
        if counters is None:        
            cnts = np.loadtxt('pretrained/counters_all_0727_pro.csv')
        else:
            cnts = np.loadtxt(counters)            
        if synergies is None:
            syns = np.loadtxt('pretrained/synergies_all_0727_pro.csv')
        else:
            syns = np.loadtxt(synergies)
        if mmr < 2000:
            model_dict = joblib.load(os.path.join("pretrained", "2000-.pkl"))
            logger.info("Using 0-2000 MMR model")
        #elif mmr > 5000
        model_dict = joblib.load(self.MODEL_NAME)
        logger.info("Using 5000-10000 MMR model")
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
        for one_full_url in instance.match_url:
            radiant_full,dire_full,rname,dname=instance.get_trackdota(one_full_url)
            print (radiant_full,dire_full)
            radiant_name[rname]=[]
            dire_name[dname]=[]
            for teamel_a,teamel_b in zip(radiant_full,dire_full):
                radiant.append(int(self.hero_name_id[teamel_a]))
                dire.append(int(self.hero_name_id[teamel_b]))
                radiant_name[rname].append(teamel_a)
                dire_name[dname].append(teamel_b)         
            if len(radiant)==5 and len(dire)==5:
                    print (radiant,type(radiant[0]))
                    full_result=self.query(6000,radiant,dire)
                    confirm=full_result.split(" ")[0].lower()
                    print ("预测结果:%s ----r:%s:%s vs d:%s:%s"%(full_result,rname,radiant_name[rname],dname,dire_name[dname]))
            self.r=radiant
            self.d=dire
            print(radiant,"vs",dire)
            self.pick_statistics()
            radiant,dire=[],[]
        return radiant,dire,rname,dname
    def single_query(self):
        radiant,dire,rname,dname=self.get_match_bp()
        full_result=self.query(6000,radiant,dire)
        confirm=full_result.split(" ")[0].lower()
        # self.get_teamid_tostr(str(rtid),str(dtid))
        print ("预测结果:%s ----r:%s vs d:%s"%(full_result,rname,dname))
    def team_value(self):
    	return
    def pick_statistics(self, mmr_info="1"):
        self.pick_dict,self.win_dict,self.win_rate={},{},{}
        for i in self.hero_id_name:
            self.pick_dict[self.hero_id_name[i]]=0
            self.win_dict[self.hero_id_name[i]]=0
            self.win_rate[self.hero_id_name[i]]=0 

        # pick_rate = games / np.sum(games)
        df=pd.read_csv(self.train_pro_csv)
        df_test=pd.read_csv(self.test_pro_csv)
        for i,j,rw in zip(df.radiant_team,df.dire_team,df.radiant_win):
            a,b=i.split(","),j.split(",")
            for i,j in zip(a,b):
                self.pick_dict[self.hero_id_name[i]]+=1
                self.pick_dict[self.hero_id_name[j]]+=1
                if rw:
                    self.win_dict[self.hero_id_name[i]]+=1
                if not rw:
                    self.win_dict[self.hero_id_name[j]]+=1  
        # print (self.pick_dict)
        # print (len(self.pick_dict))
        pick_listto_sort=self.pick_dict.items()
        x=sorted(pick_listto_sort,key=lambda x:x[1])
        # print (x)
        self.cr,self.cd=[self.hero_id_name[str(i)] for i in self.r],[self.hero_id_name[str(i)] for i in self.d]
        # print (self.cr,self.cd)
        rad_p,dire_p=[],[]
        for i,j in zip(self.cr,self.cd):
            rad_p.append([i,self.pick_dict[i]])
            dire_p.append([j,self.pick_dict[j]])
        print ("两边总统计数:",rad_p,"vs",dire_p)
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
        hero_dict = self.hero_id_name
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
    def plot_learning_curve(self,x_train=None, y_train=None, subsets=200, mmr=None, cv=3, tool='matplotlib'):
        dataset_train, _ = self.read_dataset('matches_0727.csv', low_mmr=6000,advantages=True)
        dataset_test, _ = self.read_dataset('matches_testset_0727.csv', low_mmr=6000,advantages=True)
        x_train, y_train=dataset_train
        x_test,y_test=dataset_test
        subset_sizes = np.exp(np.linspace(3, np.log(len(y_train)), subsets)).astype(int)
        results_list = [[], []]
        for subset_size in subset_sizes:
            print("执行",subset_size)

            _, _, cv_score, roc_auc, _ = self.evaluate([x_train[:subset_size], y_train[:subset_size]],
                                                  [x_test, y_test], cv=5)
            results_list[0].append(1 - cv_score)
            results_list[1].append(1 - roc_auc)
        if tool == 'matplotlib':
            self.plot_matplotlib(subset_sizes, results_list, mmr)

if __name__ == '__main__':
    update_model_logic=True
    REALTIME_PREDICT=False
    if update_model_logic==True:
        print ("start..")
        instance=Match_stat(trainmode="pro")#update_dataset_and_testset=True
        # instance.save_everymatch_tocsv()
        train_result=instance.train()
        print (train_result,"训练成功:","模型(逻辑回归):")
    if REALTIME_PREDICT==True:
        instance=Match_stat(trainmode=None)#update_dataset_and_testset=True
        instance.get_match_bp()
        #instance.plot_learning_curve()