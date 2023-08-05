from ..shared.helpers import getStringWithOnlyValidPythonVariableCharacters
from typing import List

class CustomFieldArg:
	def __init__(self,customField:dict,formPrefix:str):
		customFieldType=customField['type']
		customFieldId=customField['id']
		customFieldName=getStringWithOnlyValidPythonVariableCharacters(customField['name'])
		customPropName=f'{formPrefix}c{customFieldId}_{customFieldName}'
		argType='None'
		if customFieldType=='Text Field':
			argType='str'
		elif customFieldType=='Number Field':
			argType='float'
		elif customFieldType=='Date Time Field':
			argType='datetime'
		elif customFieldType=='Single Value Enumeration Field':
			if customField['enumeration_values']!=[]:
				commaSeparatedOptions=_getCommaSeperatedEnums(customField['enumeration_values'])
				argType=f'Literal[{commaSeparatedOptions}]'
		elif customFieldType=='Multi Value Enumeration Field':
			if customField['enumeration_values']!=[]:
				commaSeparatedOptions=_getCommaSeperatedEnums(customField['enumeration_values'])
				argType=f'List[Literal[{commaSeparatedOptions}]]'
		elif customFieldType=='Single Value Hierarchical Enumeration Field':
			if customField['enumeration_values']!=[]:
				commaSeparatedOptions=_getCommaSeperatedEnumsForNestedEnums(customField['enumeration_values'])
				argType=f'Literal[{commaSeparatedOptions}]'
		elif customFieldType=='Multi Value Hierarchical Enumeration Field':
			if customField['enumeration_values']!=[]:
				commaSeparatedOptions=_getCommaSeperatedEnumsForNestedEnums(customField['enumeration_values'])
				argType=f'List[Literal[{commaSeparatedOptions}]]'
		elif customFieldType=='Address Field':
			argType='Address'
		elif customFieldType=='Single Value Lookup Entity Field':
			argType='int'
		elif customFieldType=='Multi Value Lookup Entity Field':
			argType='List[int]'
		self.argType:str=argType
		self.argName:str=customPropName
		self.required:bool=customField['required']

def _getFormPrefix(formDef):
	formType=formDef['type']
	formPrefix=''
	formId=formDef['id']
	if formType in ['Order','CreditRequest','Quote']:
		formPrefix=f'f{formId}_'
	return formPrefix

def _getCommaSeperatedEnums(enumerationValues:List[dict]):
	commaSeparatedOptions=''
	for enum in enumerationValues:
		option=enum["label"]
		##remove non-ascii characters
		option=option.encode('ascii', 'ignore').decode('ascii')
		commaSeparatedOptions+=f'"{option}",'
	return commaSeparatedOptions[:-1]

def _getCommaSeperatedEnumsForNestedEnums(enumValues:List[dict]):
	commaSeparatedOptions=''
	parentToChildEnumValues={}
	for enum in enumValues:
		
		if 'parent_id' not in enum:
			parentToChildEnumValues[enum['id']]={'label':enum['label'],'children':[]}
		else:
			parentToChildEnumValues[enum['parent_id']]['children'].append(enum)
	for parentEnumId in parentToChildEnumValues:
		for childEnum in parentToChildEnumValues[parentEnumId]['children']:
			parentOption=parentToChildEnumValues[parentEnumId]['label']
			childOption=childEnum['label']
			##remove non-ascii characters
			parentOption=parentOption.encode('ascii', 'ignore').decode('ascii')
			childOption=childOption.encode('ascii', 'ignore').decode('ascii')

			commaSeparatedOptions+=f'"{parentOption} - {childOption}",'
	return commaSeparatedOptions[:-1]

def getListCustomFieldArgs(formDef):
	customFields=formDef['custom_fields']
	skippedCustomFieldTypes=['Images Field','Signature Field','Sketch Field','Divider Field','Label Field']
	listOfCustomFieldArgs:List[CustomFieldArg]=[]
	formPrefix=_getFormPrefix(formDef)
	for customField in customFields:
		customFieldType=customField['type']
		if customFieldType in skippedCustomFieldTypes:
			continue
		listOfCustomFieldArgs.append(CustomFieldArg(customField,formPrefix))
	return listOfCustomFieldArgs