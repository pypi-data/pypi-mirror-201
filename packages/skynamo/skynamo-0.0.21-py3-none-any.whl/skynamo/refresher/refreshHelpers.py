from ..shared.helpers import getStringWithOnlyValidPythonVariableCharacters

def getNameOfModelClassOnWhichToAddCustomFieldFromFormDefinition(formDef):
	formType=formDef['type']
	formId=formDef['id']
	formName=formDef['name']
	instanceClassName=getStringWithOnlyValidPythonVariableCharacters(formName)+f'_f{formId}'
	if formType in ['Order','CreditRequest','Quote']:
		instanceClassName=formType
	elif formId==-3:
		instanceClassName='Product'
	elif formId==-1:
		instanceClassName='Customer'
	return instanceClassName

def isCustomForm(instanceClassName):
	if '_f' in instanceClassName:
		return True
	return False


