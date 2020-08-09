
a=[1,2,3,4,5,6,7]
b=[3,4,5,11]
c=set(a).difference(set(b))
print (c)
aset=set(a)
bset=set(b)

#discard

print (aset.discard(set({1,2})))
print (aset)

#intersection
print (aset.intersection(bset))



dictd={1:(1,2),50:("a",50),3:(1,-1),5:(3,-100)}
c=dictd.items()
dddd=sorted(c,key=lambda x:x[1][1])


dddd=list(dddd)
lll=["|".join([str(i[0]),"|".join([str(k) for k in i[1]])]) for i in dddd]
print (lll)
# print (dddd)
# print (123,str(c))
# for i in str(c):
# 	print (i)
# for j in c:
# 	print (j)
# print (list(c))


k=[i for i in dictd]
print (k)
""

# with open("matchid_file_2020-10-03.txt","r+",encoding="utf-8") as f:
	# x=set(f.readlines())
# print (len(x))

#union
print (aset.union(bset))