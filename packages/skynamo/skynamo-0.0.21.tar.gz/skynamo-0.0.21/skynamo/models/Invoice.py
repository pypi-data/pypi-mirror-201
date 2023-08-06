from typing import Literal,Union,List
from datetime import datetime
from ..shared.helpers import getDateTimeObjectFromSkynamoDateTimeStr
from .InvoiceItem import InvoiceItem

class Invoice:
	def __init__(self,json:dict={}):
		self.id:int=json['id']
		self.date:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['date'])
		self.customer_id:int=json['customer_id']
		self.customer_code:str=json['customer_code']
		self.reference:Union[str,None]=None
		if 'reference' in json:
			self.reference=json['reference']
		self.row_version:int=json['row_version']
		self.last_modified_time:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['last_modified_time'])
		self.status:Union[None,Literal['Draft','Authorized','Delivered','Outstanding','Paid','Deleted']]=None
		if 'status' in json:
			self.status=json['status']
		self.due_date:Union[None,datetime]=None
		if 'due_date' in json:
			self.due_date=getDateTimeObjectFromSkynamoDateTimeStr(json['due_date'])
		self.external_id:Union[None,str]=None
		if 'external_id' in json:
			self.external_id=json['external_id']
		self.tax_inclusion:Union[None,Literal['Included','Excluded']]=None
		if 'tax_inclusion' in json:
			self.tax_inclusion=json['tax_inclusion']
		self.total_tax_amount:Union[None,float]=None
		if 'tax' in json:
			self.total_tax_amount=json['tax']
		self.outstanding_balance:Union[None,float]=None
		if 'outstanding_balance' in json:
			self.outstanding_balance=json['outstanding_balance']
		self.items:List[InvoiceItem]=[]
		for item in json['items']:
			inputToInvoiceItem={'product_id':item['product_id'],'product_code':item['product_code'],'quantity':item['quantity'],'totalLineValue':item['value']}
			if 'tax_amount' in item:
				inputToInvoiceItem['tax_amount']=item['tax_amount']
			self.items.append(InvoiceItem(**inputToInvoiceItem))