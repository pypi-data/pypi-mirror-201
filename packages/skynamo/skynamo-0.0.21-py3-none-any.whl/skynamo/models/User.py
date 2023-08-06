class User:
	def __init__(self,json:dict):
		self.id:int=json['id']
		self.user_name:str=json['user_name']
		self.display_name:str=json['display_name']
		self.email:str=json['email']
		self.is_verified:bool=json['is_verified']
		self.active:bool=json['active']
		if 'access' in json:
			self.access:str=json['access']
