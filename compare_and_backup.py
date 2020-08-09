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
    def __init__(self,VFL,update_dataset_and_testset=False):
        from dotadata_stat_match_0727 import Match_stat
        self.VALIDATE_FILE_LIST=VFL
        self.instance_ml=Match_stat(trainmode=None)
        self.match_catalog="MATCH_JSON_DIR_0727/"
        with open("hero_id_name.json","r+") as f:
            self.hero_id_name=load(f)
        with open ("hero_id_name_id.json","r+") as f:
            self.hero_id=load(f)

        pre_df1=pd.read_csv("matches_0727.csv")
        pre_df2=pd.read_csv("matches_testset_0727.csv")
        self.pre_lenth=len(pre_df1.append(pre_df2))
        print(self.instance_ml.MODEL_NAME)
        self.instance_ml.MODEL_NAME='model_'+str(datetime.date.today())+"_"+str(self.pre_lenth)+'.pkl'#"model_2020-07-06.pkl#"model_2020-07-06.pkl"
        self.instance_ml.MODEL_NAME_KERAS='kerasmodel_'+str(datetime.date.today())+"_"+str(self.pre_lenth)+'.pkl'#"model_2020-07-06.pkl#"model_2020-07-06.pkl"

        print ("现有模型名|长度|日期:",self.instance_ml.MODEL_NAME,"2e6_samples_20200727_LSTM_mmr_0915.h5")
        print (self.pre_lenth)
        self.time_limit="2020-06-30 08:54:01"#版本更新比赛的日期格式
        self.real_match={}
        self.game_version="0727"
        self.ua = UserAgent()
        self.headers={"user-agent":self.ua.random}
        self.heroes_released=129

    def model_validate(self,match_set_filename):
        f="W:\\cl\\req_gamesportsdata\\data_recent_mmr\\"+match_set_filename#"matches_0727.csv"
        self.lenth_1,self.lenth_2=len(pd.read_csv("matches_0727.csv")),len(pd.read_csv("matches_testset_0727.csv"))
        self.pro_lenth_1,self.pro_lenth_2=len(pd.read_csv("matches_0727_pro.csv")),len(pd.read_csv("matches_testset_0727_pro.csv"))

        fname="matches_list_ranking_2e6_0915.csv"
        total_csv=pd.read_csv(fname)
        self.pre_lenth=len(total_csv)
        real_test_set=pd.read_csv(f,encoding="utf-8")
        right,total=0,len(real_test_set)
        print("实际验证模型长度:",total)
        newest_model='model_'+str(datetime.date.today())+"_"+str(self.pro_lenth_1+self.pro_lenth_2)+'.pkl'#"model_2020-07-06.pkl#"model_2020-07-06.pkl"
        self.MODEL_NAME=newest_model
        dire_count,radiant_count=0,0
        count=0
        count_50=0
        jud=55
        for one_game in real_test_set.values:
            radiant_team, dire_team ,radiant_win= one_game[2], one_game[3], one_game[4]
            radiant,dire=[int(i) for i in radiant_team.split(",")],[int(i) for i in dire_team.split(",")]
            # print (radiant,dire)
            full_result=self.instance_ml.query(6000,radiant,dire)
            confirm,percentage=full_result.split(" ")[0].lower(),full_result.split(" ")[2]         
            rate=float(percentage[:-1])
            if rate>jud:
                count_50+=1
                if confirm=="radiant" and radiant_win:
                    right+=1
                elif confirm=="dire" and not radiant_win:
                    right+=1
        return "学习器(high_mmr):,正确数,统计总数,正确率,错误数,混淆",right/count_50,count_50,len(real_test_set)#right,count,right/count,count-right,match_set_filename
    def pro_model_validate(self,match_set_filename):
        f="W:\\cl\\req_gamesportsdata\\data_recent_mmr\\"+match_set_filename#"matches_0727.csv"
        right=0
        real_test_set=pd.read_csv(f,encoding="utf-8")
        dire_count,radiant_count=0,0
        count=0
        count_50=0
        jud=52
        per_stats=[]
        for one_game in real_test_set.values:
            radiant_team, dire_team ,radiant_win= one_game[2], one_game[3], one_game[4]
            radiant,dire=[int(i) for i in radiant_team.split(",")],[int(i) for i in dire_team.split(",")]
            newest_model='model_'+str(datetime.date.today())+"_"+str(self.lenth_2+self.lenth_1)+'.pkl'
            newest_model='model_'+str(datetime.date.today())+"_"+str(self.pro_lenth_1+self.pro_lenth_2)+'.pkl'
            self.instance_ml.MODEL_NAME=newest_model
            full_result=self.instance_ml.query(6000,radiant,dire,synergies="pretrained/synergies_all_0727_pro.csv",counters="pretrained/counters_all_0727_pro.csv")
            confirm_pro,percentage_pro=full_result.split(" ")[0].lower(),full_result.split(" ")[2]         
            rate_pro=float(percentage_pro[:-1])
            if confirm_pro and (rate>jud and rate_pro>jud):
                if confirm_pro=="radiant" and radiant_win:
                    right+=1
                elif confirm_pro=="dire" and not radiant_win:
                    right+=1
                count +=1
            else:
                per_stats.append({"hight_mmr":[rate,confirm],"pro":[rate_pro,confirm],"actual":[radiant_win]})
        return "学习器(pro and hight_mmr):,正确数,统计总数,正确率,错误数,混淆",right,count,right/count,count-right,match_set_filename,len(per_stats)
    def deepl_predict(self,match_set_filename):
        import keras
        from keras.models import Sequential
        from keras.layers import LSTM, Dense, Activation, Embedding, Masking, Dropout, Conv1D, MaxPooling1D, Reshape
        from keras.models import load_model
        from json import load,dump,loads
        logic_result=[]
        f="W:\\cl\\req_gamesportsdata\\data_recent_mmr\\"+match_set_filename#"matches_0727.csv"
        model_saved_path,model_name=".\\model_keras\\","2e6_samples_20200727_LSTM_mmr_0915.h5"
        real_test_set=pd.read_csv(f,encoding="utf-8")
        right,total=0,len(real_test_set)
        x_label=[]
        self.instance_ml.MODEL_NAME=self.instance_ml.MODEL_NAME
        print("验证集长度:",len(real_test_set))
        mod=5
        for one_game in real_test_set.values:
            radiant_win, radiant_heroes, dire_heroes = one_game[1], one_game[2], one_game[3]    
            radiant_heroes = list(map(int, radiant_heroes.split(',')))
            dire_heroes = list(map(int, dire_heroes.split(',')))
            full_result=self.instance_ml.query(6000,radiant_heroes,dire_heroes)
            confirm,percentage=full_result.split(" ")[0].lower(),full_result.split(" ")[2]         
            rate=float(percentage[:-1])
            logic_result.append([rate,confirm])
            r_vector=np.zeros(129)
            d_vector=np.zeros(129)
            for i,j in zip(radiant_heroes,dire_heroes):
                r_vector[i-1]=1
                d_vector[j-1]=1        
            x_label.append([r_vector,d_vector])
            if len(x_label)<-1:
                print (len(x_label))
        y_label = list(real_test_set.radiant_win)#(pd_match.radiant_win==1.0).astype(np.int)
        test_x = np.array(x_label).reshape(len(x_label),2,129)
        test_y = np.array(y_label).reshape(len(y_label),1)
        model = load_model(model_saved_path+model_name)
        out0 = model.predict(test_x)        
        correct_num = 0
        count_51=0
        for i in range(len(out0)):
            # print(out0[i])
            if (out0[i][0]>0.53 or out0[i][0]<0.47):
                temp_result=None
                if out0[i][0]<0.5:#and logic_result[i][1]=="dire":
                    # print (logic_result[i][0])
                    temp_result = 0.0#预测天辉胜利值为0也就是天辉失败
                elif out0[i][0]>=0.5:#and logic_result[i][1]=="radiant":
                    # print (logic_result[i][0])
                    temp_result = 1.0
                if temp_result!=None:
                    if temp_result==test_y[i][0]:
                        correct_num += 1
                    count_51+=1
            temp_result=None
        print('验证集同时相等而且深度预测53正确准确率：',float(correct_num)/count_51)
        return "预测:正确数,统计总数,正确率",correct_num,count_51,float(correct_num)/count_51,len(out0)
    def incomplete_model_validate(self,match_set_filenameout0):#        f="F:\\cl\\req_gamesportsdata\\data_recent_mmr\\"+match_set_filename#"matches_0727.csv"
        real_test_set=pd.read_csv(f,encoding="utf-8")
        right,total=0,len(real_test_set)
        print("实际验证模型长度:",total)

        dire_count,radiant_count=0,0
        count=0
        count_50=0
        jud=53
        for one_game in real_test_set.values:
            radiant_team, dire_team ,radiant_win= one_game[2], one_game[3], one_game[4]
            radiant,dire=[int(i) for i in radiant_team.split(",")],[int(i) for i in dire_team.split(",")]
            # print (radiant,dire)
            full_result=self.instance_ml.query(6000,radiant,dire)
            confirm,percentage=full_result.split(" ")[0].lower(),full_result.split(" ")[2]         
            rate=float(percentage[:-1])
            if rate>jud:
                count_50+=1
                if confirm=="radiant" and radiant_win:
                    right+=1
                elif confirm=="dire" and not radiant_win:
                    right+=1
                count +=1
        return "学习器(pro_1700+):,正确数,统计总数,正确率,错误数,混淆",right,count,right/count,count-right,match_set_filename
    def random_predict(self,match_set_filename):
        f="W:\\cl\\req_gamesportsdata\\data_recent_mmr\\"+match_set_filename#"matches_0727.csv"
        real_test_set=pd.read_csv(f,encoding="utf-8")
        # print (real_test_set.head())
        right,total=0,len(real_test_set)
        dire_count,radiant_count=0,0
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
        df=pd.read_csv(".csv")
        df_test=pd.read_csv(".csv")
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
        pick_listto_sort=self.pick_dict.items()
        win_listto_sort=self.win_dict.items()
        winrate_listto_sort=self.win_rate.items()
        pick_view=sorted(pick_listto_sort,key=lambda x:x[1])
        win_view=sorted(win_listto_sort,key=lambda x:x[1])
        winrate_view=sorted(winrate_listto_sort,key=lambda x:x[1][1])
        if ra5 and di5:
            self.cr,self.cd=[self.hero_id[str(i)] for i in ra5],[self.hero_id[str(i)] for i in di5]
            # print (self.cr,self.cd)
            rad_p,dire_p=[],[]
            for i,j in zip(self.cr,self.cd):
                rad_p.append([i,self.pick_dict[i]])
                dire_p.append([j,self.pick_dict[j]])
            print ("两边总统计数:",rad_p,"vs",dire_p)

if __name__ == '__main__':
    MANUL_EVALUATE_MODEL=True
    AUTO_EVALUATE_MODEL=False
    preview=False
    print ("用最新(或者更好)数据检验模型的准确率:")
    adf=pd.read_csv("matches_0727_pro.csv")
    bdf=pd.read_csv("matches_testset_0727_pro.csv")
    df_new=pd.concat([adf,bdf],axis=0,ignore_index=True)
    ABS_PATH="W:\\cl\\req_gamesportsdata\\data_recent_mmr\\"
    df_new.to_csv(ABS_PATH+"real_match_"+str(len(df_new))+".csv",index=False)
    FILE_VALIDATE_SET=["matches_list_ranking_test1e3.csv","real_match_1931.csv","matches_list_ranking_5000.csv"]#matches_0727_pro.csv"]#real_match_"+str(len(df_new))+".csv"]#[i for i in listdir("data_recent_mmr") if i[:3]=="exp"]#
    instance=Match_stat(FILE_VALIDATE_SET)#update_dataset_and_testset=True
    #这里加个实际比赛的正则表达式,文件列表
    if MANUL_EVALUATE_MODEL==True:
        for file in FILE_VALIDATE_SET:
            result=instance.deepl_predict(file)
            print (file,"deep_mmr_result_list:",result)
        for file in FILE_VALIDATE_SET:
            result=instance.model_validate(file)
            print (file,"logic_mmr_result_list:",result)    
        # for file in FILE_VALIDATE_SET:
        #     result=instance.pro_model_validate(file)
        #     print (result)
    elif AUTO_EVALUATE_MODEL==True:
        pass

