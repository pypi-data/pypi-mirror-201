from typing import Union

class InvoiceItem:
	def __init__(self,product_code:str,quantity:float,totalLineValue:float,tax_amount:Union[None,float]=None,product_id:Union[None,int]=None):
		self.product_id=product_id
		self.product_code:str=product_code
		self.quantity:float=quantity
		self.totalLineValue:float=totalLineValue
		self.tax_amount:Union[None,float]=tax_amount

	def getJsonReadyValue(self):
		res={
			'product_id':self.product_id,
			'product_code':self.product_code,
			'quantity':self.quantity,
			'value':self.totalLineValue
		}
		if self.tax_amount != None:
			res['tax_amount']=self.tax_amount
		return res