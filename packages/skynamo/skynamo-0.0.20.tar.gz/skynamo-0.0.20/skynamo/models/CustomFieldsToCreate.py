from typing import Literal

class CustomFieldsToCreate:
	def __init__(self):
		self.fields_to_add=[]
##fieldtypes=Text, Number, SingleSelect, MultiSelect, NestedSingleSelect, NestedMultiSelect, Address, UserSingleSelect, UserMultiSelect
	def addCustomerCustomField(self,name:str,type:Literal['Text','Number','SingleSelect','MultiSelect','NestedSingleSelect','NestedMultiSelect','Address']):
		self.fields_to_add.append({'name':name,'type':type,'form_id':-1})
	def addProductCustomField(self,name:str,type:Literal['Text','Number','SingleSelect','MultiSelect','NestedSingleSelect','NestedMultiSelect','Address']):
		self.fields_to_add.append({'name':name,'type':type,'form_id':-3})
	def addFormCustomField(self,formId:int,name:str,type:Literal['Text','Number','SingleSelect','MultiSelect','NestedSingleSelect','NestedMultiSelect','Address']):
		self.fields_to_add.append({'name':name,'type':type,'form_id':formId})