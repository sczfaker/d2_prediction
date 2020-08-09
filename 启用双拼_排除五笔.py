from itertools import combinations
p="abcdefghijklmnopqrstuvwxyz"
pronounce=["","","",""]
#音节
class ClassName(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
		self.set_landuage =[i for i in combinations(arg,2)][:]#set和list有什么区别,dict 音形肯定是最快的
		print (len(self.set_landuage))
	def yi(self):#伪随机
		return
	def real_random(self):#真随机
		return
	def railway_system(self):
		dij=["汉口","武昌","汉阳","钟祥","东莞","东莞东"]
		return
	def filter_style(self):
		return
ddc=ClassName(p)
print(ddc.set_landuage)