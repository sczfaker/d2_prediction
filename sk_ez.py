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

from sklearn import datasets
iris=datasets.load_iris()
print (iris)
# print (list(iris.keys()))

X=iris["data"][:,3:]
y=(iris["target"]==0).astype(np.int)
print (y)


log_reg=LogisticRegression()
log_reg.fit(X,y)
X_new=np.linspace(0,3,1000).reshape(-1,1)
print (X_new)


# import dota_pro
# instance_pro=dota_pro.Match_stat()
# print (instance_pro.query(6000,[1,2,3,4,5],[5,6,7,8,9]))