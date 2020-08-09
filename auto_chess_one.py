# -*- coding:utf-8 -*-
from itertools import combinations
import sys,io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
from json import load,loads,dump
#"月骑|精灵|骑士|2"
#"巫妖|亡灵|法师|5"
#"死亡先知|亡灵|术士|5"

class Chess_Simulate(object):
	"""docstring for ClassName"""
	def __init__(self):
		self.chess_game_hero={}
		self.hero=["船长|人类|战士|4","美杜莎|娜迦|猎人|4","光之守卫|人类|法师|4","炼金|地精|术士|4","dk|骑士|人类|龙|4","利爪|野兽|德鲁伊|4","巨魔战将|巨魔|战士|4","末日守卫|恶魔|战士|4","死灵|亡灵|术士|4","巫医|巨魔|术士|1","剑圣|兽人|战士|2","影魔|恶魔|术士|3","火枪|矮人|猎人|2","幻影|精灵|刺客|3","斯拉克|娜迦|刺客|2","剃刀|元素|法师|3","火女|人类|法师|3","死亡骑士|亡灵|骑士|2","全能|人类|骑士|3","灵魂守卫|恶魔|恶魔猎手|3","沙王|虫|刺客|3","剧毒|野兽|术士|3","狼人|人类|野兽|战士|3","毒龙|龙|刺客|3","变体精灵|元素|刺客|2","冰女|人类|法师|1","混沌|恶魔|骑士|2","兽王|兽人|猎人|2","撕拉达|娜迦|战士|3","伐木机|地精|工匠|2","仙女|精灵|法师2","先知|精灵|德鲁伊|2","大树|精灵|德鲁伊|3","小小|元素|战士|1","发条|地精|工匠|1","海民|野兽|战士|1","小黑|亡灵|猎人|1","蓝胖|食人魔|法师|2","小鹿|野兽|德鲁伊|1","斧王|兽人战士1","赏金|地精|刺客|1","蝙蝠|巨魔|骑士|2","修补匠|地精|工匠|1","暗影萨满|巨魔|萨满|1|","敌法|精灵|恶魔猎手|1","陈|兽人|牧师|4","死灵龙|亡灵|龙|猎人|3","军团|人类|骑士|3","全能|人类|骑士|3","斧王|兽人|战士|1","仙女|精灵|巫师|1","巫医|巨魔|术士|1","马尔斯|神|战士|1","裂魂人|牛头人|刺客|1","冰龙|亡灵|龙|法师|1","游侠|亡灵|猎人|1","风行|精灵|猎人|4","恶魔巫师|恶魔|巫师|2","混沌骑士|恶魔|骑士|2","熊猫酒仙|熊猫人|武僧|2","月女|精灵|猎人|2","戴泽|巨魔|牧师|2","神域|神|牧师|2","神牛|牛头人|萨满|4","蜘蛛|虫|猎人|4","墨客|恶魔|巫师|4","拉比克|神|巫师|3","干扰者|兽人|萨满|5","祈求者|精灵|法师|5","大圣|野兽|武僧|5","圣堂|||5","矮人飞机|||5","神灵|巨魔|战士|5","双头龙|龙|法师|5","帝景工程师|地精|工匠|5","电眼绝收|地精|骑士|5","潮汐|娜迦|猎人|5","谜团|元素|术士|5","宙斯|神|法师|5","流浪剑客|恶魔|战士|5","痛苦女王|恶魔|刺客|5"]
	def convert2dic(self):
		for i in self.hero:
			one_hero_list=i.split("|")
			print (one_hero_list)
			if len(one_hero_list)==5:
				level,occupation,speice,name=one_hero_list[-1],one_hero_list[-2],one_hero_list[-3:-5],one_hero_list[0]
			elif len(one_hero_list)==4:
				level,occupation,speice,name=one_hero_list[-1],one_hero_list[-2],one_hero_list[-3],one_hero_list[0]
			if len(one_hero_list) in [4,5]:
				if name not in self.chess_game_hero:
					self.chess_game_hero[name]={"名称":name,"occupation":occupation,"species":speice,"lvl":level}
		print (len(self.chess_game_hero))
		sort_level=sorted(self.chess_game_hero.items(),key=lambda x:x[1]["lvl"])
		count_2,count_3,count_4,count_5=0,0,0,0
		for i in sort_level:
			if i[1]["lvl"]=="2":
				print (i[0],i[1]["lvl"])
				count_2+=1
			elif i[1]["lvl"]=="3":
				print (i[0],i[1]["lvl"])
				count_3+=1
			elif i[1]["lvl"]=="4":
				print (i[0],i[1]["lvl"])
				count_4+=1
			elif i[1]["lvl"]=="5":
				pass
			# 	print (i[0],i[1]["等级"])
			# 	count_5+=1
		print (count_2,count_3,count_4,count_5,"总数对吧")
		with open ("chess_hero_dict.json","w+",encoding="utf-8") as f:
			dump(self.chess_game_hero,f)
	def proba_table(self):
		level_k_list={"random_pick_1":{"1":100,"2":0,"3":0,"4":0,"5":0},"random_pick_2":{"1":70,"2":30,"3":0,"4":0,"5":0},"random_pick_3":{"1":60,"2":35,"3":5,"4":0,"5":0},"random_pick_4":{"1":50,"2":35,"3":15,"4":0,"5":0},"random_pick_5":{"1":40,"2":35,"3":23,"4":2,"5":0},"random_pick_6":{"1":33,"2":30,"3":30,"4":7,"5":0},"random_pick_7":{"1":30,"2":30,"3":30,"4":10,"5":0},"random_pick_8":{"1":24,"2":30,"3":30,"4":15,"5":1},"random_pick_9":{"1":22,"2":30,"3":25,"4":20,"5":3},"random_pick_10":{"1":19,"2":25,"3":25,"4":25,"5":6}}
		level_next_list={"1-2":0,"2-3":0,"3-4":0,"4-5":0,"5-6":0,"6-7":0,"7-8":0,"8-9":0,"9-10":0,"10-11":0,"11-12":0}
		hypo={"1":{},"2":{},"3":{},"4":{},"5":{}}
		current={}
	def income_and_cost(self,**args):
		one_turn_cost={"Buy":{"times":0},"Sell":{},"upgrade":{},"ban":{}}
	def detail_TIPS(self):
		accrual="10"
		
		return
if __name__ == '__main__':
	UPDATE_BASIC=True
	if UPDATE_BASIC==True:
		instance=Chess_Simulate()
		instance.convert2dic()

# thdict={}
# for i in range(2,11):
	# thdict[i]={}
# print (thdict)



# combo={1:[],2:[],3:[],6:[],9:[]}
# print (combo)

# un_occupations=["猎人hunter",\
# "战士warrior","骑士knight","矮人dwarf","好斗goblin","发明家artisan","法师wiz\
# zard","萨满shaman",,"刺客assasin","恶魔\
# demon","恶魔猎手demonhunter","术士warlock",""]
# race=["人类human","亡灵deadghost","德鲁伊druidism","野兽beast","兽人orc","元素element","巨魔troll"]
# true_com_occpuations={}
# for i in un_occupations:
# 	true_com_occpuations[i]=[]
# def com_occpuations():
# 	for i in hero:
# 		if i.find("猎人")!=-1:
# 			true_com_occpuations["猎人hunter"].append(i[:i.find("|")])
# 		if i.find("人类")!=-1:
# 			true_com_occpuations["人类human"].append(i[:i.find("|")])
# 		if i.find("亡灵")!=-1:
# 			true_com_occpuations["亡灵deadghost"].append(i[:i.find("|")])
# 		if i.find("德鲁伊")!=-1:
# 			true_com_occpuations["德鲁伊druidism"].append(i[:i.find("|")])
# 		if i.find("战士")!=-1:
# 			true_com_occpuations["战士warrior"].append(i[:i.find("|")])
# 		if i.find("骑士")!=-1:
# 			true_com_occpuations["骑士knight"].append(i[:i.find("|")])
# 		if i.find("矮人")!=-1:
# 			true_com_occpuations["矮人dwarf"].append(i[:i.find("|")])
# 		if i.find("地精")!=-1:
# 			true_com_occpuations["地精goblin"].append(i[:i.find("|")])
# 		if i.find("工匠")!=-1:
# 			true_com_occpuations["工匠artisan"].append(i[:i.find("|")])
# 		if i.find("萨满")!=-1:
# 			true_com_occpuations["萨满shaman"].append(i[:i.find("|")])
# 		if i.find("野兽")!=-1:
# 			true_com_occpuations["野兽beast"].append(i[:i.find("|")])
# 		if i.find("兽人")!=-1:
# 			true_com_occpuations["兽人orc"].append(i[:i.find("|")])
# 		if i.find("元素")!=-1:
# 			true_com_occpuations["元素element"].append(i[:i.find("|")])
# 		if i.find("刺客")!=-1:
# 			true_com_occpuations["刺客assasin"].append(i[:i.find("|")])
# 		if i.find("恶魔")!=-1:
# 			true_com_occpuations["恶魔demon"].append(i[:i.find("|")])
# 		if i.find("恶魔猎手")!=-1:
# 			true_com_occpuations["恶魔猎手demonhunter"].append(i[:i.find("|")])
# 		if i.find("巨魔")!=-1:
# 			true_com_occpuations["巨魔troll"].append(i[:i.find("|")])
# 		if i.find("术士")!=-1:
# 			true_com_occpuations["术士warlock"].append(i[:i.find("|")])
# 		if i.find("法师")!=-1:
# 			true_com_occpuations["法师wizzard"].append(i[:i.find("|")])
# com_occpuations()
# def getoutpopulation(n):
# 	li=[]
# 	if n<=6:
# 		for i in hero:
# 			if int(i[-1])<=3:
# 				li.append(i[:i.find("|")])
# 	if n==7:
# 		for i in hero:
# 			if int(i[-1])<=4:
# 				li.append(i[:i.find("|")])
# 	if n>7:
# 		for i in hero:
# 			if int(i[-1])<=5:
# 				li.append(i[:i.find("|")])

# 	return li



# # c=0
# # for i in thdict:
# # 	if i==6:
# # 		forcom=getoutpopulation(i)
# # 	    # for choice in combinations(forcom,i):
# # 	    	# if c==100:
# # 	    	# 	break
# # 	    	# for j in choice:
# # 	    	# # 	getherooc(j)
# # 	    	# c+=1


# def getherooc(h):
# 	for i in true_com_occpuations:
# 		if h in true_com_occpuations[i]:
# 			if h not in tmp_com[singlecom]:
# 				tmp_com[singlecom][i]=1
# 			else:
# 				tmp_com[singlecom][i]+=1




# com9=[]
# forcom=getoutpopulation(8)
# c=500
# for i in combinations(forcom,10):
# 	c+=1
# 	if c==520:
# 		break
# 	com9.append(i)
# com_strength={}
# com_strength["输出能力"]={}
# tmp_com={}
# for singlecom in com9:
# 	tmp_com[singlecom]={}
# 	for i in singlecom:
# 		getherooc(i)
# print (tmp_com)
# print(tmp_com)
# c=0
# for i in tmp_com:
# 	c+=1
# 	print (str(c),end=":")
# 	print (i,end="")
# 	print (tmp_com[i])

# def select_userful_com(com8):
# 	pass
