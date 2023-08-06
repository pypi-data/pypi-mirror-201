from typing import Union
class OrderUnit:
	def __init__(self,name:str,multiplier:int=1,active:bool=True,id:Union[int,None]=None):
		self.id=id
		self.name=name
		self.multiplier=multiplier
		self.active=active
	def getJsonReadyValue(self):
		return self.__dict__