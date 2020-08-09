"击杀奖励,可靠金钱,不可靠金钱"
type_of_gold=['reliable','unreliable']
first_blood_time=150
sum_of_procession=0
gold_assit_range=1300
comeback_relation=[0,1]
assit_hero_num=[0,1,2,3,4,5]
dead_hero_level=range(1,25)
poor_relation=[1,2,3,4,5]
# rank_relation=[1,2,3,4,5,6,7,8,9,10]
base_num=[1,2,4,5.6,7.0]
pro_rank=[[1],[1.3,0.7],[1.3,1,0.7],[1.3,1.1,0.9,0.7],[1.3,1.15,1,0.85,0.7]]


def get_kill_money(num_of_assit_hero,rank_me,rank_dead,comback,dead_procession,level_of_dead,state):
	assert num_of_assit_hero>=rank_me
	assert num_of_assit_hero>=0
	assert rank_dead>=0
	assert rank_me>=0
	assert level_of_dead>=1 and level_of_dead<=25
	poor_coe=1.2-0.15*rank_dead
	pro_coe=pro_rank[num_of_assit_hero][rank_me]
	ut=(126/base_num[num_of_assit_hero])+(4.5-0.9*num_of_assit_hero)*level_of_dead+comback*(dead_procession*0.026+70)/(num_of_assit_hero+1)
	utt=pro_coe*poor_coe*ut
	#print (poor_coe)
	#print (pro_coe)
	return utt
# lostmoney=50+pro/40
# buyback=100 +pro/13
# buyback_cooldown=8*60
# buyback_punishment=[0,25]
# reborn_time=4*level+buyback_punishment[0]
print (110+8*25)
for i in range(5):
	for j in range(2):
			print ("你在你们阵营中排名(1-5)的:"+str(j),end="<=>")
			print ("阵亡英雄在对方阵营中排名(1-5)的:"+str(i),end=":")
			print (110+8*25+get_kill_money(2,j,i,0,0,24,0))
# test_fuc()
t=5#财产综合
t=4#等级
g_1=100+t/13
lost=50+t/40


num,dead_exp,state=1,1,1
x=1
e_1=400+200*(x-1)#大杀特杀后终结的经验奖励
dead_exp
e_2=(40*0.14*dead_exp)/num
# e_3=





"385" "150"
"200"
"100+x+8*level"
"level*4"
""
"1.每次击杀 发生的财产分为 击杀周围所有英雄拿到的助攻钱(等于 f*d*0.026+70+4.5-0.9*x+126/参与人数) + 人头钱(100+x+8*level"


"""
596.2
560.425
524.65
488.875
453.1
"""
"""
590.8
555.7
520.5999999999999
485.5
450.4
"""