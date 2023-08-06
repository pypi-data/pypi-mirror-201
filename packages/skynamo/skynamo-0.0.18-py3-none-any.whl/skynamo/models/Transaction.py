from typing import Union,List
from datetime import datetime
from ..shared.helpers import getDateTimeObjectFromSkynamoDateTimeStr
from .LineItem import LineItem

class Transaction:
	def __init__(self,json:dict):
		self.id:int=json['id']
		self.date:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['date'])
		self.customer_id:int=json['customer_id']
		self.customer_code:str=json['customer_code']
		self.customer_name:str=json['customer_name']
		self.reference:Union[str,None]=json['reference']
		self.interaction_id:int=json['interaction_id']
		self.discount_percentage:float=json['discount']
		self.discount_amount:float=json['discount_amount']
		self.total_amount:float=json['total_amount']
		self.prices_include_vat:Union[bool,None]=json['prices_include_vat']
		self.warehouse_id:Union[int,None]=json['warehouse_id']
		self.warehouse_name:Union[str,None]=json['warehouse_name']
		self.email_recipients:Union[str,None]=json['email_recipients']
		self.last_modified_time:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['last_modified_time'])
		self.items:List[LineItem]=[]
		for item in json['items']:
			inputDict={'multiplier':1,'product_code':item['product_code'],'quantity':item['quantity'],'unit_name':item['order_unit_name'],'unit_price':item['unit_price'],'list_price':item['list_price'],'tax_rate_value':item['tax_rate_value'],'tax_rate_id':item['tax_rate_id']}
			lineItem=LineItem(**inputDict)
			lineItem.multiplier=None
			lineItem.product_name=item['product_name']
			self.items.append(lineItem)

		## the following properties are populated from completed forms after the object is created:
		self.user_id:int=0
		self.user_name:str=''

