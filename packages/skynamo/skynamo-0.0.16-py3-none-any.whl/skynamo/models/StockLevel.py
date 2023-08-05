from datetime import datetime
from skynamo.shared.helpers import getDateTimeObjectFromSkynamoDateTimeStr
from typing import Union

class StockLevel:
	def __init__(self,json:dict):
		self.product_id:int=json['product_id']
		self.product_code:str=json['product_code']
		self.product_name:str=json['product_name']
		self.order_unit_id:int=json['order_unit_id']
		self.order_unit_name:str=json['order_unit_name']
		self.warehouse_id:int=0
		if 'warehouse_id' in json:
			self.warehouse_id:int=json['warehouse_id']
		self.warehouse_name:str='Null warehouse'
		if 'warehouse_name' in json:
			self.warehouse_name:str=json['warehouse_name']
		self.level:int=json['level']
		self.label:Union[None,str]=None
		if 'label' in json:
			self.label:Union[None,str]=json['label']
		self.last_modified_time:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['last_modified_time'])