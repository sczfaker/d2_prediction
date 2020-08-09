


train_cot_path="./pretrained/counters_all_0727.json"
train_syn_path="./pretrained/synergies_all_0727.json"

import numpy as np
from pandas import read_csv
from json import loads,load

with open("pretrained/synergies_all_0727.json","r+",encoding="utf-8") as f1,open("pretrained/counters_all_0727","r+",encoding="utf-8") as f2:
    d1=load(f1)
    d2=load(f2)
with open("hero_id_name.json","r+") as f:
    hero_id_name=load(f)
dict_to_view={}
missing_value=[]
not_l=[i for i in list(hero_id_name.keys())]
for i in range(1,130):
    if str(i) not in not_l:
        missing_value.append(str(i))
for hero_id in hero_id_name:
    #if hero_id not in dict_to_view:
    dict_to_view[hero_id]={}
    for hid in hero_id_name:
        if hero_id!=hid:
            dict_to_view[hero_id][hid]={"com":[hero_id_name[hero_id],hero_id_name[hid]],"win":0,"count":0,"win_rate":0}
print (missing_value)
import numpy as np
import heapq

c=[]
# print ("111",a.argmax())
# for i in range(len(a)):
    # b=heapq.nlargest(3,range(len(a[i])),a[i].take)
    # c.append(b)
# print (c)
abc = np.array([[-11,3,5000,1],[1,3,5000,30000],[1,3,5,2],[1,3,5,4],[1,3,5,5]])
ind = np.unravel_index(np.argsort(abc, axis=None), abc.shape)
print(ind,ind[0][-1],ind[1][-1])
for index_cor in range(-1,-15,-1):
    x,y=ind[0][index_cor],ind[1][index_cor]
    print(abc[x,y])
# index = np.unravel_index(a.argmax(), a.shape)
# print (index)

# t=a.argsort()[-3:][::-1]
# t=heapq.nlargest(3,range(len(a)), a.take)


class Nd2INDEX(object):
    """docstring for ClassName"""
    def __init__(self, arg1,arg2):
        with open("hero_id_name.json","r+") as f:
            self.hero_id_name=load(f)
        self.d1=arg1
        self.d2=arg2
        for i in self.d2:
            d2[i]=np.array(self.d2[i])
        # for i in self.d2:
            # d2[i]=np.array(self.d2[i])
    def get_nlargest_com(self,n):
        for i in d2:
            # print (d2[i].shape)
            # print (np.argpartition(d2[i],-4)[-4:])

            # index_list=d2[i].argsort()[-3:][::-1]
            # print (index_list)
            # print (i,self.d2[i].argmax())
            if i=="winrate":
                index = np.unravel_index(np.argsort(d2[i], axis=None), self.d2[i].shape)
                print (index)
                dup=set([]) 
                for index_cor in range(-500,-750,-1):
                    x,y=index[0][index_cor],index[1][index_cor]
                    if set([x,y])==dup:
                        continue
                    pre_x,pre_y=x,y
                    dup=set([pre_x,pre_y])

                    print (i,d2[i][x,y],self.hero_id_name[str(x+1)],self.hero_id_name[str(y+1)])
                    if i=="winrate":
                        print (d2["games"][x,y],d2["wins"][x,y])

            # print (self.d1[index[0]],self.d1[index[1]])
            # print (d1[i][1,98])
            # for index in index_list:
            #     print (i,self.hero_id_name[str(index[0])],self.hero_id_name[str(index[1])])
        dict_result=0
        return dict_result
    def get_nlowest_com(self,n):
        return dict_resut
instance=Nd2INDEX(d1,d2)
instance.get_nlargest_com(5)

for one_syn in d2:#排序,胜率最高的对抗组合
    for hero_id,one_row in enumerate(d2[one_syn]):
        hero_id=str(hero_id+1)
        for hid,data in enumerate(one_row):
            hid=str(hid+1)
            if hid!=hero_id and hid not in missing_value and hero_id not in missing_value:
                if one_syn=="wins":
                    dict_to_view[hero_id][hid]["win"]=data
                elif one_syn=="count":
                    dict_to_view[hero_id][hid]["count"]=data
                else:
                    dict_to_view[hero_id][hid]["win_rate"]=data

hero_list_to_sort=dict_to_view.items()
sorted(hero_list_to_sort)




