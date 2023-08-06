from ..shared.helpers import getDateTimeObjectFromSkynamoDateTimeStr
from datetime import datetime

class Warehouse:
	def __init__(self,json:dict):
		self.id:int=json['id']
		self.name:str=json['name']
		self.order_email:str=json['order_email']
		self.credit_request_email:str=json['credit_request_email']
		self.quote_email:str=json['quote_email']
		self.active:bool=json['active']
		self.last_modified_time:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['last_modified_time'])