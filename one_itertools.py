from itertools import combinations
from random import shuffle
x=combinations([1,2,3,4],2)
print (list(x))
for i in shuffle(x):
	print (i)