from pandas import read_csv

fname='./data_recent_mmr/matches_list_ranking_2e6.csv'#%("1300")
pd_object=read_csv(fname)

print (len(set(list(pd_object["match_id"]))))
# print (len(set(list(pd_object["match_id"])))