from typing import Union,Literal,List,Dict
from datetime import datetime
from skynamo.models.Address import Address
from skynamo.shared.helpers import getDateTimeObjectFromSkynamoDateTimeStr
from skynamo.models.Location import Location

class Customer:
	def __init__(self,json:dict):
		self.id:int=json['id']
		self.code:str=json['code']
		self.name:str=json['name']
		self.active:bool=json['active']
		self.location:Location=Location(**json['location'])
		self.price_list_id:Union[int,None]=None
		if 'price_list_id' in json:
			self.price_list_id=json['price_list_id']

		self.price_list_name:Union[str,None]=None
		if 'price_list_name' in json:
			self.price_list_name=json['price_list_name']
		self.assigned_users:List[int]=json['assigned_users']
		self.default_discount:float=json['default_discount']
		self.default_warehouse_id:Union[int,None]=None
		if 'default_warehouse_id' in json:
			self.default_warehouse_id=json['default_warehouse_id']
		self.default_warehouse_name:Union[str,None]=None
		if 'default_warehouse_name' in json:
			self.default_warehouse_name=json['default_warehouse_name']
		self.row_version:int=json['version']
		self.last_modified_time:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['last_modified_time'])
		self.create_date:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['create_date'])


