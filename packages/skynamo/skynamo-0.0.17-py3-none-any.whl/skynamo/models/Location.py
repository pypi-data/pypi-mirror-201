from typing import Union
class Location:
	def __init__(self,latitude=0.0,longitude=0.0,accuracy=0.0,is_approximate=False):
		self.latitude=latitude
		self.longitude=longitude
		self.accuracy=accuracy
		self.is_approximate=is_approximate
	def getJsonReadyValue(self):
		if self.latitude==0.0 and self.longitude==0.0:
			return None
		return {'latitude':self.latitude,'longitude':self.longitude,'accuracy':self.accuracy,'is_approximate':self.is_approximate}
