from .WriteOperationCls import WriteOperation
from .writeHelpers import getWriteOperationToUpdateObject,getBodyForWriteOperation,addWarehouseAndLabelToStockLevelUpdateIfPresent
from .execute import executeWrites
from typing import Union,Literal,Union
from ..models.Invoice import Invoice
from ..models.InvoiceItem import InvoiceItem
from datetime import datetime
from typing import List
from ..models.CustomFieldsToCreate import CustomFieldsToCreate
from ..models.Warehouse import Warehouse
from ..models.TaxRate import TaxRate
from ..models.PriceList import PriceList
from ..models.VisitFrequency import VisitFrequency


class WriterBase:
	def __init__(self):
		self.writeOperations:List[WriteOperation]=[]
	def apply(self):
		res= executeWrites(self.writeOperations)
		self.writeOperations=[]
		return res
	##unchanging update operations
	def addStockLevelUpdate(self,product_id:int,order_unit_id:int,level:int,warehouse_id:int=0,label:Union[None,str]=None):
		item={'product_id': product_id, 'order_unit_id': order_unit_id, 'level': level}
		addWarehouseAndLabelToStockLevelUpdateIfPresent(item,warehouse_id,label)
		self.writeOperations.append(WriteOperation("stocklevels", "post", item))

	def addStockLevelUpdateUsingProductCodeAndUnitName(self,product_code:str,order_unit_name:str,level:int,warehouse_id:int=0,label:Union[None,str]=None):
		item={'product_code': product_code, 'order_unit_name': order_unit_name, 'level': level}
		addWarehouseAndLabelToStockLevelUpdateIfPresent(item,warehouse_id,label)
		self.writeOperations.append(WriteOperation("stocklevels", "post", item))

	def addPriceUpdate(self,product_id:int,order_unit_id:int,price:float,price_list_id:int,tax_rate_id:Union[None,int]=None):
		item= {'product_id': product_id, 'order_unit_id': order_unit_id, 'price': price, 'price_list_id': price_list_id}
		if tax_rate_id!=None:
			item['tax_rate_id']=tax_rate_id
		self.writeOperations.append(WriteOperation("prices", "post",item))

	def addPriceUpdateUsingProductCodeAndUnitName(self,product_code:str,order_unit_name:str,price:float,price_list_id:int,tax_rate_id:Union[None,int]=None):
		item= {'product_code': product_code, 'order_unit_name': order_unit_name, 'price': price, 'price_list_id': price_list_id}
		if tax_rate_id!=None:
			item['tax_rate_id']=tax_rate_id
		self.writeOperations.append(WriteOperation("prices", "post",item))

	def addInvoiceUpdate(self,invoice:Invoice,fieldsToUpdate:List[str]):
		self.writeOperations.append(getWriteOperationToUpdateObject(invoice,fieldsToUpdate))
	##unchanging create operations
	def addInvoiceCreate(self,date:datetime,customer_code:str,items:List[InvoiceItem],reference='',status:Union[None,Literal['Draft','Authorized','Delivered','Outstanding','Paid','Deleted']]=None,due_date:Union[None,datetime]=None,taxIsIncludedInLineValues=True,outstanding_balance:Union[None,float]=None):
		body=getBodyForWriteOperation(locals())
		del body['taxIsIncludedInLineValues']
		if not(taxIsIncludedInLineValues):
			for item in body['items']:
				taxAmount=0
				if 'tax_amount' in item:
					taxAmount=item['tax_amount']
				item['value']=item['value']+taxAmount
		self.writeOperations.append(WriteOperation("invoices", "post", body))

	def addScheduledVisitCreate(self,assigned_user_name:str,customer_code:str,due_date:datetime,end_time:Union[datetime,None]=None,comment:Union[None,str]=None):
		body=getBodyForWriteOperation(locals())
		if end_time==None:
			body['all_day']=True
		self.writeOperations.append(WriteOperation("scheduledvisits", "post", body))

	def addCustomFieldCreations(self,customFieldsToCreate:CustomFieldsToCreate):
		self.writeOperations.append(WriteOperation("integrations", "post", {'action':'AddCustomFields','fields_to_add':customFieldsToCreate.fields_to_add},canBeCombinedWithOtherWritesInAList=False))
	## warehouses
	def addWarehouseCreate(self,name:str,order_email:str='',credit_request_email:str='',quote_email:str='',active:bool=True):
		body=getBodyForWriteOperation(locals())
		self.writeOperations.append(WriteOperation("warehouses", "post", body))

	def addWarehouseUpdate(self,warehouse:Warehouse,fieldsToUpdate:List[Literal['name','order_email','credit_request_email','quote_email','active']]):
		body={'id':warehouse.id,'name':warehouse.name}
		for field in fieldsToUpdate:
			body[field]=getattr(warehouse,field)
		self.writeOperations.append(WriteOperation("warehouses", "patch", body))
	## taxes
	def addTaxRateCreate(self,name:str,rate:float,active:bool=True):
		if rate<0 or rate>100:
			raise ValueError('rate must be between 0 and 100')
		body=getBodyForWriteOperation(locals())
		self.writeOperations.append(WriteOperation("taxrates", "post", body))
	def addTaxRateUpdate(self,taxrate:TaxRate,fieldsToUpdate:List[Literal['name','rate','active']]):
		body={'id':taxrate.id,'name':taxrate.name}
		for field in fieldsToUpdate:
			body[field]=getattr(taxrate,field)
		self.writeOperations.append(WriteOperation("taxrates", "patch", body))
	## pricelists
	def addPriceListCreate(self,name:str,prices_include_vat:bool,active:bool=True):
		body=getBodyForWriteOperation(locals())
		self.writeOperations.append(WriteOperation("pricelists", "post", body))
	def addPriceListUpdate(self,pricelist:PriceList,fieldsToUpdate:List[Literal['name','prices_include_vat','active']]):
		body={'id':pricelist.id,'name':pricelist.name}
		for field in fieldsToUpdate:
			body[field]=getattr(pricelist,field)
		self.writeOperations.append(WriteOperation("pricelists", "patch", body))
	## visitfrequencies
	def addVisitFrequencyCreate(self,customer_id:int,user_name:str,numberOfCyclesPerPeriod:int,numberOfVisitsRequiredPerCycle:int,period:Literal['Week','Month','Year']):
		body=getBodyForWriteOperation(locals())
		## replace numberOfCyclesPerPeriod with cycle and replace numberOfVisitsRequiredPerCycle with frequency
		body['cycle']=body['numberOfCyclesPerPeriod']
		body['frequency']=body['numberOfVisitsRequiredPerCycle']
		del body['numberOfCyclesPerPeriod']
		del body['numberOfVisitsRequiredPerCycle']
		self.writeOperations.append(WriteOperation("visitfrequencies", "post", body))
	
	def addVisitFrequencyUpdate(self,visitFrequency:VisitFrequency,fieldsToUpdate:List[Literal['customer_id','user_name','numberOfCyclesPerPeriod','numberOfVisitsRequiredPerCycle','period']]):
		body={'id':visitFrequency.id}
		for field in fieldsToUpdate:
			body[field]=getattr(visitFrequency,field)
		## replace numberOfCyclesPerPeriod with cycle and replace numberOfVisitsRequiredPerCycle with frequency
		if 'numberOfCyclesPerPeriod' in body:
			body['cycle']=body['numberOfCyclesPerPeriod']
			del body['numberOfCyclesPerPeriod']
		if 'numberOfVisitsRequiredPerCycle' in body:
			body['frequency']=body['numberOfVisitsRequiredPerCycle']
			del body['numberOfVisitsRequiredPerCycle']
		self.writeOperations.append(WriteOperation("visitfrequencies", "patch", body))

