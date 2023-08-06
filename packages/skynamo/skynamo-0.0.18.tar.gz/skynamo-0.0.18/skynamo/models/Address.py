class Address:
	def __init__(self,street:str='',city:str='',state:str='',zip:str=''):
		self.street=street
		self.city=city
		self.state=state
		self.zip=zip

	def populateFromJsonValue(self,jsonValue):
		##split on newline
		lines=jsonValue.split('\n')
		for i in range(4):
			if i<len(lines):
				if i==0:
					self.street=lines[i]
				elif i==1:
					self.city=lines[i]
				elif i==2:
					self.state=lines[i]
				elif i==3:
					self.zip=lines[i]

	def getJsonReadyValue(self):
		return f'{self.street}\n{self.city}\n{self.state}\n{self.zip}'