#coding:utf-8
# from keras.layers import LSTM, Dense, Activation, Embedding, Masking, Dropout, Conv1D, MaxPooling1D, Reshape
# from sklearn.model_selection import cross_val_score
# from sklearn.metrics import roc_auc_score, accuracy_score
# from sklearn.preprocessing import StandardScaler
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import train_test_split
# from matplotlib.font_manager import FontProperties
# import keras
from itertools import combinations
from keras.models import load_model
from pandas import read_csv,DataFrame
from keras.models import Sequential
from fake_useragent import UserAgent
from re import findall,compile,match
from os import chdir,listdir,rename
from itertools import combinations
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates       # 让坐标显示月份
# import matplotlib as mpl 
from json import load,dump,loads
from requests import get
from time import sleep
from random import choice
import numpy as np
import pandas as pd
import datetime
import operator
import random
import logging
import sys,io
import time
import math
import time
import sys
import os
from os import popen,system
import subprocess
# os.environ['THEANO_FLAGS'] = "device=gpu"  # 改变环境变量添加THEANO_FLAGS,在导入theano的时候可以设置使用gpu
#from keras.utils.visualize_plots import figures   # TODO：一个手动添加的模块，用来绘制误差值随着迭代次数的曲线，并保存图像
# mpl.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签  
mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号  
class Data_Meaning_Learn(object):
    def __init__(self, arg1="1234"):
        self.replay_id = arg1
        self.command_clarity_install_mvn_jar={"inspector":["mvn -P info package","java -jar %starget/combatlog.one-jar.jar %s"],"MatchEnd":["mvn -P dtinspector package","java -jar %starget/matchend.one-jar.jar %s"],"combatlog":["mvn -P combatlog package","java -jar %starget/lifestate.one-jar.jar %s"],"info":["mvn -P matchend package","java -jar %starget/info.one-jar.jar %s"],"lifestate":["mvn -P lifestate package","java -jar %starget/dtinspector.one-jar.jar %s"]}
        for i in self.command_clarity_install_mvn_jar:
            print(i,self.command_clarity_install_mvn_jar[i][0],self.command_clarity_install_mvn_jar[i][1])
        # self.command_parse_dem_type={""}
        self.program_path="W:/cl/clarity-examples/"
  #       self.a="java -jar target/combatlog.one-jar.jar %s.dem"%(self.replay_id)
        # self.b="java -jar target/matchend.one-jar.jar %s.dem"%(self.replay_id)
        # self.c="java -jar target/lifestate.one-jar.jar %s.dem"%(self.replay_id)
        # self.d="java -jar target/info.one-jar.jar %s.dem"%(self.replay_id)
        # self.e="java -jar target/dtinspector.one-jar.jar %s.dem"%(self.replay_id)
        self.replay_version="0727_"
        self.out_put_file_name=" >W:/cl/req_gamesportsdata/replay_raw_data/%s.txt"
    def pick_combination_match(self):
        self.hero_seed_name="hero_id_name_id.json"
        with open(self.hero_seed_name,"r+",encoding="utf-8") as f:
            dict_hero_129=load(f)
        hero_name_list=[i for i in dict_hero_129.values()]
        print (hero_name_list)
        return 
    def get_raw_dem_data(self):
        dem_path="W:/cl/req_gamesportsdata/promatch_replay/"
        dem_list=[dem_path+i for i in os.listdir(dem_path) if i.endswith("dem")]
        self.ipe_name=self.replay_id
        for i in dem_list:
            prefix=i.split(".")[0].replace("v0727","inspect_v0727")
            prefix=prefix.split("/")[-1]
            output_fname=self.out_put_file_name%(prefix)
            print (output_fname)
            command=self.command_clarity_install_mvn_jar["inspector"][1]%(self.program_path,i)+output_fname
            try:
                if os.path.exists(output_fname):
                    continue
                os.system(command)
                print ("write success")
            except:
                assert 1>2
    def read_txt_demdata(self):
        pass
        


if __name__ == '__main__':
    instance=Data_Meaning_Learn("2135")
    instance.get_raw_dem_data()