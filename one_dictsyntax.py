from json import load,dump,loads,dumps

with open ("hero_id_name.json","r+") as f:
    hero_dict=load(f)
x=list(hero_dict.items())
for i in x:
	t=int(i[0])
	c=i[1]
	hero_dict.update({t:c})
	hero_dict.pop(i[0])
# for i in range(129):
# 	t=str(i)
# 	try:
# 		hero_dict.pop(t)
# 	except:
# 		continue

a=dumps(hero_dict)
with open ("hero_id_name_id.json","w+") as f:
	f.write(a)
x=7
from delorean import Delorean
d = Delorean()
dd = d.shift('Asia/Shanghai')
print(dd)
dddc = d.shift('Asia/Tokyo')


s="['dajhwjkewk','wkehkk',{1231,3},True]"
k=eval(s)
print (k)
single_player={}
a={1:3,4:5}
b={3:5,2:7}
print (a.update(b))
print (a)



t="eda.dzm.ab"
print (t.endswith(".dzm.ab"))

#字符串通过eval转换成列表 前提是字符串本身就是列表的格式
c="[1,2,3,4]"
print (eval(c))




a={"1":2,3:4}

print ("values:",a.values())
ccc=a.values()
ddd=b.values()
for i,j in zip(ccc,ddd):
	print (i,j)


with open("team_and_player.json","r+",encoding="utf-8") as f:
    dict_player_id=load(f)
single_player={}
k=[j for i in dict_player_id for j in dict_player_id[i]]

# print (k)