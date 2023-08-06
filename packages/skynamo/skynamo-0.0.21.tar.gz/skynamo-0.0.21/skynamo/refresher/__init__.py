import os
from ..reader.sync import SyncDataTypesFromSkynamo,getSynchedDataTypeFileLocation
import json
from .InstanceClassContentsCls import InstanceClassContents

def deleteExistingCodeAndEnsureRequiredFoldersExist():
	## remove skynamoInstanceDataClasses subfolders and files
	if os.path.exists('skynamo_data'):
		if os.path.exists('skynamo_data/code'):
			for root, dirs, files in os.walk('skynamo_data/code', topdown=False):
				for name in files:
					os.remove(os.path.join(root, name))
				for name in dirs:
					os.rmdir(os.path.join(root, name))
		else:
			os.mkdir('skynamo_data/code')
		if not(os.path.exists('skynamo_data/cache')):
			os.mkdir('skynamo_data/cache')
	else:
		os.mkdir('skynamo_data')
		os.mkdir('skynamo_data/code')
		os.mkdir('skynamo_data/cache')

def refreshCustomFormsAndFields():
	deleteExistingCodeAndEnsureRequiredFoldersExist()
	SyncDataTypesFromSkynamo(['formdefinitions'])
	formsJson={}
	with open(getSynchedDataTypeFileLocation('formdefinitions'), "r") as read_file:
		formsJson=json.load(read_file)
	instanceClassContents=InstanceClassContents()
	for formDefId in formsJson['items']:
		formDef=formsJson['items'][formDefId]
		if formDef['active']==True:
			instanceClassContents.addFormDefinitionToRelevantClassContents(formDef)
	instanceClassContents.write()

