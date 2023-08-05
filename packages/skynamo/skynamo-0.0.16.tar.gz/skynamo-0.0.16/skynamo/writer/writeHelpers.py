from datetime import datetime
from typing import Literal,Union,List

from .WriteOperationCls import WriteOperation

def isBasicType(fieldValue):
	return isinstance(fieldValue,str) or isinstance(fieldValue,bool) or isinstance(fieldValue,int) or isinstance(fieldValue,float) or isinstance(fieldValue,list) or isinstance(fieldValue,dict) or fieldValue==None

def getJsonReadyFieldValue(fieldValue):
	if isinstance(fieldValue,datetime):
		return fieldValue.strftime('%Y-%m-%dT%H:%M:%S')
	elif isBasicType(fieldValue)==False:
		return fieldValue.getJsonReadyValue()
	elif isinstance(fieldValue,list):
		for i in range(len(fieldValue)):
			if isBasicType(fieldValue[i])==False:
				fieldValue[i]=fieldValue[i].getJsonReadyValue()
	return fieldValue

def getCustomFieldIdIfFieldIsCustomField(fieldName:str):
	## if format of "f{digit}_c{customFieldDigit}_*" or "c{customFieldDigit}_*", return customFieldDigit else return None
	fieldName=fieldName.split('_')[0]
	if len(fieldName)>1:
		fieldName=fieldName[1:]
		if fieldName.isdigit():
			return int(fieldName)
		else:
			fieldName=fieldName.split('_')[0]
			if len(fieldName)>1:
				fieldName=fieldName[1:]
				if fieldName.isdigit():
					return int(fieldName)
	return None


def addPatchedFieldToBodyIfAllowed(body:dict,fieldName:str,fieldValue,object:object):
	if fieldName in ['id','row_version','version','create_date','last_modified_time','tax']:
		raise Exception(f'Field {fieldName} cannot be patched')
	if fieldName not in object.__dict__:
		raise Exception(f'Field {fieldName} is not a valid {type(object).__name__} field')
	customFieldId=getCustomFieldIdIfFieldIsCustomField(fieldName)
	jsonReadyFieldValue=getJsonReadyFieldValue(fieldValue)
	if customFieldId!=None:
		if 'custom_fields' not in body:
			body['custom_fields']=[]
		body['custom_fields'].append({'id':customFieldId,'value':jsonReadyFieldValue})
	else:
		body[fieldName]=jsonReadyFieldValue

def getWriteOperationToUpdateObject(object:object,fieldsToPatch:List[str],httpMethod:Literal['patch','put','post']='patch'):
	body={'id':object.id}#type:ignore
	for fieldName in fieldsToPatch:
		fieldValue=object.__dict__[fieldName]
		if fieldValue==None:
			raise Exception(f'Error in field: {fieldName}, it is set to null. If you want to remove a value for customers or products, you need to do writer.addReplaceCustomer() or writer.addReplaceProdct()')
		addPatchedFieldToBodyIfAllowed(body,fieldName,object.__dict__[fieldName],object)
	import json
	print(json.dumps(body))
	return WriteOperation(type(object).__name__.lower()+'s', httpMethod, body)

def getWriteOperationToPutObject(object:object,httpMethod:Literal['patch','put','post']='put'):
	body=object.__dict__.copy()
	for fieldToNotUpdate in ['row_version','version','create_date','last_modified_time']:
		if fieldToNotUpdate in body:
			del body[fieldToNotUpdate]
	convertToSkynamoApiReadyValues(body)
	return WriteOperation(type(object).__name__.lower()+'s', httpMethod, body)

def addToCustomFieldsIfCustomField(key:str,body:dict):
	## if format of "f{digit}_c{customFieldDigit}_*" or "c{customFieldDigit}_*", add to custom fields
	customFieldId=getCustomFieldIdIfFieldIsCustomField(key)
	if customFieldId!=None:
		body['custom_fields'].append({'id':customFieldId,'value':body[key]})
		return True
	else:
		return False

def convertToSkynamoApiReadyValues(body:dict):
	keysToDelete=[]
	body['custom_fields']=[]
	for key in body:
		if body[key]==None:
			keysToDelete.append(key)
		else:
			if type(body[key])==datetime:
				body[key]=body[key].strftime('%Y-%m-%dT%H:%M:%S')
			elif isBasicType(body[key])==False:
				body[key]=body[key].getJsonReadyValue()
			elif isinstance(body[key],list):
				for i in range(len(body[key])):
					if isBasicType(body[key][i])==False:
						body[key][i]=body[key][i].getJsonReadyValue()
					elif isinstance(body[key][i],dict):
						convertToSkynamoApiReadyValues(body[key][i])
			elif isinstance(body[key],dict):
				convertToSkynamoApiReadyValues(body[key])

			isCustomField=addToCustomFieldsIfCustomField(key,body)
			if isCustomField:
				keysToDelete.append(key)
	for key in keysToDelete:
		del body[key]
	if len(body['custom_fields'])==0:
		del body['custom_fields']

def getBodyForWriteOperation(locals):
	body=locals
	del body['self']
	convertToSkynamoApiReadyValues(body)
	return body

def addWarehouseAndLabelToStockLevelUpdateIfPresent(item:dict,warehouse_id:int,label:Union[None,str]):
	if warehouse_id:
		item['warehouse_id'] = warehouse_id
	if label:
		item['label'] = label