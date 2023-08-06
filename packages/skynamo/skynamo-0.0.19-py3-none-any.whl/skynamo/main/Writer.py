from skynamo.writer.WriterBase import WriterBase
from skynamo.writer.writeHelpers import getWriteOperationToUpdateObject,getBodyForWriteOperation,getWriteOperationToPutObject
from skynamo.writer.WriteOperationCls import WriteOperation

from skynamo.models.Location import Location
from skynamo.models.OrderUnit import OrderUnit
from skynamo.models.LineItem import LineItem
from skynamo.models.Address import Address

from .Customer import Customer
from .Product import Product
from .Order import Order
from .Quote import Quote
from .CreditRequest import CreditRequest
from typing import Union,Literal,List,Dict
from datetime import datetime

class Writer(WriterBase):
	def __init__(self):
		super().__init__()
		self.writeOperations=[]
	## add update operations dependent on custom fields
	def addCustomerUpdate(self,customer:Customer,fieldsToUpdate:List[str]):
		fieldsToUpdate.append('active')
		self.writeOperations.append(getWriteOperationToUpdateObject(customer,fieldsToUpdate))
	def addCustomerReplace(self,customer:Customer):
		self.writeOperations.append(getWriteOperationToPutObject(customer))
	
	def addProductUpdate(self,product:Product,fieldsToUpdate:List[str]):
		fieldsToUpdate.append('active')
		self.writeOperations.append(getWriteOperationToUpdateObject(product,fieldsToUpdate))
	def addProductReplace(self,product:Product):
		self.writeOperations.append(getWriteOperationToPutObject(product))
	## add create operations dependent on custom fields
	def addCustomerCreate(self,code:str,name:str,##|requiredCustomerCustomFields|##,
						active:bool=True,location:Union[Location,None]=None,
						price_list_id:Union[int,None]=None,price_list_name:Union[str,None]=None,assigned_users:List[int]=[],
						default_discount:float=0.0,default_warehouse_id:Union[int,None]=None,default_warehouse_name:Union[str,None]=None,
						##|optionalCustomerCustomFields|##
						):
		self.writeOperations.append(WriteOperation("customers", "post", getBodyForWriteOperation(locals())))
	
	def addProductCreateWithSingleUnit(self,code:str,name:str,##|requiredProductCustomFields|##,
										unit_name:str='Unit',active:bool=True,##|optionalProductCustomFields|##
										):
		argsDict=locals()
		del argsDict['unit_name']
		body=getBodyForWriteOperation(argsDict)
		body['order_units']=[{'name':unit_name,'multiplier':1,'active':True}]
		self.writeOperations.append(WriteOperation("products", "post", body))

	def addProductCreateWithMultipleOrderUnits(self,code:str,name:str,order_units:List[OrderUnit],##|requiredProductCustomFields|##,
									active:bool=True,##|optionalProductCustomFields|##
										):
		self.writeOperations.append(WriteOperation("products", "post", getBodyForWriteOperation(locals())))

	def addOrderCreate(self,customer_id:int,date:datetime,user_id:int,items:List[LineItem],##|requiredOrderCustomFields|##,
						warehouse_id:Union[int,None]=None,prices_include_vat:Union[bool,None]=None,discount:Union[None,float]=None,
						##|optionalOrderCustomFields|##
						):
		self.writeOperations.append(WriteOperation("orders", "post", getBodyForWriteOperation(locals())))
	def addQuoteCreate(self,customer_id:int,date:datetime,user_id:int,items:List[LineItem],##|requiredQuoteCustomFields|##,
						warehouse_id:Union[int,None]=None,prices_include_vat:Union[bool,None]=None,discount:Union[None,float]=None,
						##|optionalQuoteCustomFields|##
						):
		self.writeOperations.append(WriteOperation("quotes", "post", getBodyForWriteOperation(locals())))
	def addCreditRequestCreate(self,customer_id:int,date:datetime,user_id:int,items:List[LineItem],##|requiredCreditRequestCustomFields|##,
						warehouse_id:Union[int,None]=None,prices_include_vat:Union[bool,None]=None,discount:Union[None,float]=None,
						##|optionalCreditRequestCustomFields|##
						):
		self.writeOperations.append(WriteOperation("creditrequests", "post", getBodyForWriteOperation(locals())))

