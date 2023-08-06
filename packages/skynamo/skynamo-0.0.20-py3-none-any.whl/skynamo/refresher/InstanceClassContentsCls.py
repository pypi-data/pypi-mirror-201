from ..shared.helpers import writeToInstanceSpecificFile,clearInstanceSpecificFolder
import os
from .refreshHelpers import getNameOfModelClassOnWhichToAddCustomFieldFromFormDefinition,isCustomForm
from .CustomFieldArg import getListCustomFieldArgs,CustomFieldArg
from typing import List,Dict

def getStringContentOfClassInMainFolder(className:str):
	if className[-3:]!='.py':
		className+='.py'
	sharedPath = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
	mainPath=sharedPath.replace('/refresher','/main')
	with open(f'{mainPath}/{className}', "r") as read_file:
		return read_file.read()

class InstanceClassContents:
	def __init__(self):
		self.writerContent=getStringContentOfClassInMainFolder('Writer')
		self.readerContent=getStringContentOfClassInMainFolder('Reader')
		self.orderContent=getStringContentOfClassInMainFolder('Order')
		self.quoteContent=getStringContentOfClassInMainFolder('Quote')
		self.creditrequestContent=getStringContentOfClassInMainFolder('CreditRequest')
		self.productContent=getStringContentOfClassInMainFolder('Product')
		self.customerContent=getStringContentOfClassInMainFolder('Customer')

		self.__customFormBaseContent=getStringContentOfClassInMainFolder('CustomForm')
		self.customFormsContent={}
		self.modelNameToCustomFieldPropTypes={}

	def write(self):
		self.addCustomFieldPropTypesToRelevantClassContents()
		clearInstanceSpecificFolder('code')
		writeToInstanceSpecificFile('code/Writer.py',self.writerContent)
		writeToInstanceSpecificFile('code/Reader.py',self.readerContent)
		writeToInstanceSpecificFile('code/Order.py',self.orderContent)
		writeToInstanceSpecificFile('code/Quote.py',self.quoteContent)
		writeToInstanceSpecificFile('code/CreditRequest.py',self.creditrequestContent)
		writeToInstanceSpecificFile('code/Product.py',self.productContent)
		writeToInstanceSpecificFile('code/Customer.py',self.customerContent)
		for customFormName,customFormContent in self.customFormsContent.items():
			writeToInstanceSpecificFile(f'code/{customFormName}.py',customFormContent)

	def addCustomFieldPropTypesToRelevantClassContents(self):
		standardClasses=['Order','Quote','CreditRequest','Product','Customer']
		for i,modelClassName in enumerate(standardClasses):
			classContent=self.__getattribute__(f'{modelClassName.lower()}Content')
			customFieldArgsWithPropTypes={}
			if modelClassName in self.modelNameToCustomFieldPropTypes:
				customFieldArgsWithPropTypes=self.modelNameToCustomFieldPropTypes[modelClassName]
			classContent+=f'\t\tself._customFieldPropTypes:Dict[str,str]={customFieldArgsWithPropTypes}\r'
			self.__updateClassContents(modelClassName,classContent)
		for customFormName,customFormContent in self.customFormsContent.items():
			customFieldArgsWithPropTypes=self.modelNameToCustomFieldPropTypes[customFormName]
			customFormContent+=f'\t\tself._customFieldPropTypes:Dict[str,str]={customFieldArgsWithPropTypes}\r'
			self.customFormsContent[customFormName]=customFormContent

	def addFormDefinitionToRelevantClassContents(self,formDef:dict):
		formId=formDef['id']
		formName=formDef['name']
		if formName in ['Dropbox','SkynamoServices']:
			return
		customFieldArgs=getListCustomFieldArgs(formDef)
		modelClassName=getNameOfModelClassOnWhichToAddCustomFieldFromFormDefinition(formDef)
		self.__addCustomFieldsToRelevantModelClassContents(customFieldArgs,modelClassName,formId)
		self.__addCustomFieldsToWriterIfApplicable(customFieldArgs,modelClassName)
		self.__addCustomFormGetMethodsToReader(modelClassName)

	def __addCustomFieldsToRelevantModelClassContents(self,customFieldArgs:List[CustomFieldArg],modelClassName:str,formId:str):
		modelClassString=self.__customFormBaseContent.replace(f'class CustomForm(',f'class {modelClassName}(')
		if not(isCustomForm(modelClassName)):
			modelClassString=self.__getattribute__(f'{modelClassName.lower()}Content')
		customFieldArgsWithPropTypes={}
		for customFieldArg in customFieldArgs:
			modelClassString+=f'\t\tself.{customFieldArg.argName}:Union[{customFieldArg.argType},None]=None\r'
			customFieldArgsWithPropTypes[customFieldArg.argName]=customFieldArg.argType
		if modelClassName not in self.modelNameToCustomFieldPropTypes:
			self.modelNameToCustomFieldPropTypes[modelClassName]={}
		for key in customFieldArgsWithPropTypes:
			self.modelNameToCustomFieldPropTypes[modelClassName][key]=customFieldArgsWithPropTypes[key]
		self.__updateClassContents(modelClassName,modelClassString)

	def __updateClassContents(self,modelClassName:str,modelClassString:str):
		if not(isCustomForm(modelClassName)):
			self.__setattr__(f'{modelClassName.lower()}Content',modelClassString)
		else:
			self.customFormsContent[modelClassName]=modelClassString

	def __addCustomFieldsToWriterIfApplicable(self,customFieldArgs:List[CustomFieldArg],modelClassName:str):
		if not(isCustomForm(modelClassName)):
			requiredCustomFieldsArgsAsString=[]
			optionalCustomFieldsArgsAsString=[]
			for customFieldArg in customFieldArgs:
				if customFieldArg.required:
					requiredCustomFieldsArgsAsString.append(f'{customFieldArg.argName}:{customFieldArg.argType}')
				else:
					propType=f'Union[{customFieldArg.argType},None]'
					if customFieldArg.argType=='None':
						propType='None'
					optionalCustomFieldsArgsAsString.append(f'{customFieldArg.argName}:{propType}=None')
			placeHolder=f'##|required{modelClassName}CustomFields|##'
			replacement=placeHolder
			if len(requiredCustomFieldsArgsAsString)>0:
				replacement=','+replacement
			self.writerContent=self.writerContent.replace(placeHolder,','.join(requiredCustomFieldsArgsAsString)+replacement)
			placeHolder=f'##|optional{modelClassName}CustomFields|##'
			replacement=placeHolder
			if len(optionalCustomFieldsArgsAsString)>0:
				replacement=','+replacement
			self.writerContent=self.writerContent.replace(placeHolder,','.join(optionalCustomFieldsArgsAsString)+replacement)

	def __addCustomFormGetMethodsToReader(self,modelClassName:str):
		if isCustomForm(modelClassName):
			importString=f'from .{modelClassName} import {modelClassName}\r'
			importPlaceHolder='##|customImports|##'
			self.readerContent=self.readerContent.replace(importPlaceHolder,importString+importPlaceHolder)
			getMethodString=f'\tdef get{modelClassName}(self,forceRefresh=False):\r'
			getMethodString+=f'\t\trefreshJsonFilesLocallyIfOutdated(["completedforms"],forceRefresh)\r'
			getMethodString+=f'\t\tresult:List[{modelClassName}]=getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation("completedforms"),{modelClassName})\r'
			getMethodString+=f'\t\treturn result\r'
			self.readerContent+=getMethodString