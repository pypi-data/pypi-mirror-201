class OrderUnit:
	def __init__(self,name:str,multiplier:int=1,active:bool=True):
		self.id=None
		self.name=name
		self.multiplier=multiplier
		self.active=active
	def getJsonReadyValue(self):
		return self.__dict__