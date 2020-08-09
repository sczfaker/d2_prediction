from two_class_syntax import B
class A(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		self.instance=B()
		self.instance.arg = 125
		self.instance.q()
		self.arg = 125
if __name__ == '__main__':
	A(10)