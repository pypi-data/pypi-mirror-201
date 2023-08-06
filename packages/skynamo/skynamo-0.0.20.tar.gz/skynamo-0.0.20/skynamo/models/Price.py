from datetime import datetime
from ..shared.helpers import getDateTimeObjectFromSkynamoDateTimeStr

class Price:
	def __init__(self,json:dict):
		self.price_list_id:int=json['price_list_id']
		self.price_list_name:str=json['price_list_name']
		self.product_id:int=json['product_id']
		self.product_code:str=json['product_code']
		self.product_name:str=json['product_name']
		self.price:float=json['price']
		self.order_unit_id:int=json['order_unit_id']
		self.order_unit_name:str=json['order_unit_name']
		self.last_modified_time:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['last_modified_time'])
		if 'tax_rate_id' in json:
			self.tax_rate_id:int=json['tax_rate_id']