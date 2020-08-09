from json import load
from pandas import read_csv
import numpy as np
import pymysql.cursors
import sys,io 
class ViewHandleOneData():
    """docstring for ViewHandleOneData"""
    def __init__(self, arg):
        #super(ViewHandleOneData, self).__init__()
        self.arg = arg
        self.dealed_data_fold="pretrain"
        self.hero_id="hero_id_name_id.json"
        with open (self.hero_id,"r",encoding="utf-8") as f:
            self.heroid2name=load(f)
        print (self.heroid2name,type(self.heroid2name))
        print (self.heroid2name["4"])
        self.heroes_released=129#num max
        
        heroes_released_filt=[str(i) for i in range(1,130) if str(i) in self.heroid2name]#seq
        self.hero_one_stat={}
        for i in self.heroid2name:
            self.hero_one_stat[self.heroid2name[i]]=[0,0,0]
        self.synergy = dict()
        self.synergy['wins'] = np.zeros((self.heroes_released, self.heroes_released))
        self.synergy['games'] = np.zeros((self.heroes_released, self.heroes_released))
        self.synergy['winrate'] = np.zeros((self.heroes_released, self.heroes_released))
        self.counter = dict()
        self.counter['wins'] = np.zeros((self.heroes_released, self.heroes_released))
        self.counter['games'] = np.zeros((self.heroes_released, self.heroes_released))
        self.counter['winrate'] = np.zeros((self.heroes_released, self.heroes_released))
        self.synergy["wins"].dtype="int"        
        self.synergy["games"].dtype="int"        
        self.counter["wins"].dtype="int"
        self.counter["games"].dtype="int"

        fname="matches_list_ranking_2e6_0915.csv"
        total_csv=read_csv(fname)
        winsyn={}
        wincnt={}
        print("总比赛数",len(total_csv.values))
        for row_amatch in total_csv.values:
            self.radiant_wincount,self.dire_wincount=0,0
            radiant_win, radiant_heroes, dire_heroes = row_amatch[1], row_amatch[2], row_amatch[3]
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
                        self.synergy['games'][radiant_heroes[i] - 1, radiant_heroes[j] - 1] += 1#每一场比赛会获得组合增量为20+20,实际组合增量为10+10 因为x,y y,x等效
                        self.synergy['games'][dire_heroes[i] - 1, dire_heroes[j] - 1] += 1
                        if radiant_win:#这里i,j j,i视为一样+1
                            self.synergy['wins'][radiant_heroes[i] - 1, radiant_heroes[j] - 1] += 1#或者标记+1
                        else:
                            self.synergy['wins'][dire_heroes[i] - 1, dire_heroes[j] - 1] += 1#获胜标记+1
                    self.counter['games'][radiant_heroes[i] - 1, dire_heroes[j] - 1] += 1#对抗组合+1 
                    self.counter['games'][dire_heroes[i] - 1, radiant_heroes[j] - 1] += 1#对抗组合+1 50 实际增量25
                    if radiant_win:#这里比较关键,注意self.counter会出现i,j 和 j,i的情况 r赢p[ij]+1 d赢p[ji]+1 表示英雄a遇到b的胜场+1 表示英雄b遇到a的胜场+1 两者加起来也是两者遇到的总场数两者获胜概率加起来也是1
                        self.counter['wins'][radiant_heroes[i] - 1, dire_heroes[j] - 1] += 1
                    else:
                        self.counter['wins'][dire_heroes[i] - 1, radiant_heroes[j] - 1] += 1        
            for enum,i in enumerate(radiant_heroes+dire_heroes):
                self.hero_one_stat[self.heroid2name[str(i)]][0]+=1
                if radiant_win and enum<5:
                    self.hero_one_stat[self.heroid2name[str(i)]][1]+=1
                elif radiant_win==False and enum>=5:
                    self.hero_one_stat[self.heroid2name[str(i)]][1]+=1

        sort_dictitem=self.hero_one_stat.items()
        k=list(sorted(sort_dictitem,key=lambda x:x[1][0],reverse=True))
        print (k[:35])
        # print (self.hero_one_stat)
        compute_total_syn=0
        compute_total_cnt=0
        for i in range(self.heroes_released):
            for j in range(self.heroes_released):
                if i!=j:#一个英雄不可能和自己同一边同一边的那个数据的ganme,winrate,win的值都为0 i>j去重
                    #也不可能和自己对抗注意这里的序号ij意义和上面updatedic的ij意义不同
                    if self.synergy['games'][i, j] != 0:
                        self.synergy['winrate'][i, j] = round(self.synergy['wins'][i, j]/float(self.synergy['games'][i, j]),3)
                        compute_total_syn+=1
                            # print ("hero",i,j,synergy['winrate'][i, j])
                    if self.counter['games'][i, j] != 0:
                        compute_total_cnt+=1
                        self.counter['winrate'][i, j] = round(self.counter['wins'][i, j]/float(self.counter['games'][i, j]),3)

        for i in range(129):
            for j in range(129):
                if i>j:
                    if str(i+1) in heroes_released_filt and str(j+1) in heroes_released_filt:
                        t,k=str(i+1),str(j+1)
                        combi2=",".join([self.heroid2name[t],self.heroid2name[k]])
                        if combi2 not in winsyn:
                            combi_data=[self.synergy["wins"][i,j],self.synergy["games"][i,j],self.synergy["winrate"][i,j],self.counter["wins"][i,j],self.counter["games"][i,j],self.counter["winrate"][i,j]]
                            winsyn[combi2]=combi_data
        sorter_2hero=winsyn.items()
        a=sorted(sorter_2hero,key=lambda x:x[1][0],reverse=True)
        b=sorted(sorter_2hero,key=lambda x:x[1][1],reverse=True)
        c=sorted([i for i in sorter_2hero if i[1][1]>50],key=lambda x:x[1][2],reverse=True)
        print (len(c))
        d=sorted(sorter_2hero,key=lambda x:x[1][3],reverse=True)
        e=sorted(sorter_2hero,key=lambda x:x[1][4],reverse=True)
        f=sorted([i for i in sorter_2hero if i[1][1]>50],key=lambda x:x[1][5],reverse=True)
        sort_view_num=20
        update_append=True
        print(list(sorter_2hero)[:sort_view_num])
        # print (a)
        table_tag=sort_view_num*"|"
        table_sp="|-|"
        a_part_view="|".join([",".join([i[0],",".join([str(k) for k in i[1]])]) for i in list(a)[:20]])
        b_part_view="|".join([",".join([i[0],",".join([str(k) for k in i[1]])]) for i in list(b)[:20]])
        c_part_view="|".join([",".join([i[0],",".join([str(k) for k in i[1]])]) for i in list(c)[:20]])
        d_part_view="|".join([",".join([i[0],",".join([str(k) for k in i[1]])]) for i in list(d)[:20]])
        e_part_view="|".join([",".join([i[0],",".join([str(k) for k in i[1]])]) for i in list(e)[:20]])
        f_part_view="|".join([",".join([i[0],",".join([str(k) for k in i[1]])]) for i in list(f)[:20]])
        print (a_part_view)
        if update_append==True:
            with open("view_win.md","a+",encoding='utf-8') as f:
                f.seek(0)
                list_write=[table_tag]+[table_sp]+["|一边胜场:"+a_part_view+"|","|一边盘数:"+b_part_view+"|","|一边胜率:"+c_part_view+"|","|对位胜场:"+d_part_view+"|","|对位盘数:"+e_part_view+"|","|对位胜率:"+f_part_view+"|"]
                k=[i+"\n" for i in list_write]
                f.writelines(k)
                print("---"*20)
        def subsequences(self):
            return
        def conver2mdtable(self):
            return
#### 0是wins 1是games 2是winrate 
class HERO(object):
    """docstring for HERO"""
    def __init__(self, arg):
        super(HERO, self).__init__()
        self.arg = arg
        
if __name__ == '__main__':
    instance=ViewHandleOneData(1)