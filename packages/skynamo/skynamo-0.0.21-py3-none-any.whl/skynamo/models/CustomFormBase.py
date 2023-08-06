from datetime import datetime
from skynamo.shared.helpers import getDateTimeObjectFromSkynamoDateTimeStr

class CustomFormBase:
	def __init__(self,json:dict):
		self.id:int=json['id']
		self.date:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['date'])
		self.customer_id:int=json['customer_id']
		self.customer_code:str=json['customer_code']
		self.customer_name:str=json['customer_name']
		self.user_id:int=json['user_id']
		self.user_name:str=json['user_name']
		self.interaction_id:int=json['interaction_id']
		self.form_id:int=json['form_id']
		self.form_name:str=json['form_name']