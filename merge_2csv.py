from pandas import read_csv,DataFrame
import pandas as pd
import numpy as np
adf=read_csv("matches_testset_0727_pro.csv")
bdf=read_csv("matches_0727_pro.csv")

# cdf=adf.append(bdf)
# print(len(cdf))
# print (len(adf.values))
f=".\\outdated\\"
ff="../outdated"

import os
print (os.path.exists(f))
print (os.path.exists(ff))

def merge_two(a,b):
	adf,bdf=read_csv(a),read_csv(b)
	df_new=pd.concat([adf,bdf],axis=0,ignore_index=True)
	print(len(df_new))
	df_new.drop_duplicates()
	#df_new.drop("Unnamed: 0",axis=1,inplace=True)
	print(len(df_new))
	df_new.to_csv("matches_list_ranking_2e6_0915.csv",index=False)
def delete_row():
	pd_df=read_csv("matches_list_ranking_2e5.csv")
	print (pd_df.index)
	pd_df.drop("Unnamed: 0",axis=1,inplace=True)
	pd_df.to_csv("normalmatch_2e5.csv",index=False)
def change_type_row():
	pd_df=read_csv("matches_list_ranking_2e6.csv")
	# pd_df=pd_df.apply(pd.to_numeric, errors='coerce')
	pd_df["match_id"]=pd_df["match_id"].astype("int64")
	pd_df["radiant_win"]=pd_df["radiant_win"].astype("int")
	print (pd_df.dtypes)
	pd_df.to_csv("matches_list_ranking_2e6.csv",index=False)
# delete_row()
# change_type_row()
def fillter_data_row():
	pd_df=read_csv("matches_list_ranking_2e6.csv")
	print(len(pd_df))
	rows=pd_df.values
	pd_df.dropna(subset=['avg_mmr'],axis=0,inplace=True)
	pd_df.to_csv("matches_list_ranking_2e6.csv",index=False)
	#pd_df=pd_df.drop(pd_df[pd_df.avg_mmr].index)
# fillter_data_row()
def fill_empty_data():
	pass
def stats_dates(a):
	pd_df=read_csv(a)
	pd_df["start_time"]=pd_df["start_time"].map(lambda start_time:start_time[:10])
	pd.set_option('display.max_rows',1000)
	pd.set_option('display.width', 1000)

	pd.set_option('display.max_colwidth',1000)
	print (pd_df.info())
	print (pd_df.groupby("start_time").size())
	# for i in pd_df.groupby("start_time").size():
	# 	print (i)
	# for i in pd_df.groupby("start_time").size():

def Data():
	Columns=["时空序列vb1","时空序列vb2","时空序列vb3"]
	a=DataFrame([[1,2,3],[4,5,6],[4,5,7]],columns=Columns)
	a.to_csv("one_create.csv",index=False)
	# for i,j in enumerate(pd_df):
	# 	if i >10:
	# 		break
	# 	print (j)

	#print (pd_df.groupby("start_time").size())
	# print (pd_df.groupby("duration").size())

if __name__ == '__main__':
	Data()
	# fa,fb="matches_list_ranking_2e6.csv","matches_list_ranking_test1e3.csv"
	# merge_two(fa,fb)
	fname="matches_list_ranking_2e6_0915.csv"
	stats_dates(fname)

	# delete_row()