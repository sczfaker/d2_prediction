
from random import choice
import numpy as np

sor=[i for i in range(1,130)]
backuplist=sor[:]
test_set=[]


a=np.zeros((50, 50))
b=np.zeros((50, 50))
c=np.zeros((50, 50))

for i in range(50):
	alist=[]
	for j in range(10):
		pick_one=choice(k)
		alist.append(pick_one)
		backuplist.remove(pick_one)
	test_set.append(alist)
	backuplist=sor[:]


print (test_set)