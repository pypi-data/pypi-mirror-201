from typing import Union

class LineItem:
	def __init__(self,product_code:str,quantity:float,unit_name:str,multiplier:int,unit_price:float,list_price:Union[None,float]=None,tax_rate_value:Union[float,None]=None,tax_rate_id:Union[int,None]=None):
		self.product_code=product_code
		self.quantity=quantity
		self.unit_price:float=unit_price
		self.list_price=list_price
		self.unit_name=unit_name
		self.multiplier:Union[None,float]=multiplier
		self.tax_rate_value=tax_rate_value
		self.tax_rate_id=tax_rate_id
		self.product_name:Union[str,None]=None

	def getJsonReadyValue(self):
		return self.__dict__