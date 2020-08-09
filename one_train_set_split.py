from sklearn.model_selection import train_test_split
#train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)
totaltime_limit=355
from pandas import read_csv
import pandas as pd
# with open(,'w+',encoding='utf-8') as f:
path="./data_recent_mmr/exp_%d_0803.csv"%(totaltime_limit)
pd_csv=read_csv(path)
train_set,test_set=train_test_split(pd_csv, test_size=0.2, random_state=42)
print (train_set,test_set)
trainname="train.csv"
testname="test.csv"
pd.DataFrame(train_set).to_csv(trainname,index=False)
pd.DataFrame(test_set).to_csv(testname,index=False)